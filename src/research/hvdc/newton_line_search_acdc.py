# Copyright (c) 1996-2015 PSERC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE_MATPOWER file.

# Copyright 1996-2015 PSERC. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# Copyright (c) 2016-2017 by University of Kassel and Fraunhofer Institute for Wind Energy and
# Energy System Technology (IWES), Kassel. All rights reserved. Use of this source code is governed
# by a BSD-style license that can be found in the LICENSE file.

# The file has been modified from Pypower.
# The function mu() has been added to the solver in order to provide an optimal iteration control
#
# Copyright (c) 2018 Santiago Peñate Vera
#
# This file retains the BSD-Style license


from numpy import array, angle, exp, linalg, r_, Inf, conj, diag, asmatrix, asarray, zeros_like, zeros, complex128, \
empty, float64, int32, arange
from scipy.sparse import csr_matrix as sparse, hstack, vstack
from scipy.sparse.linalg import spsolve, splu
import numpy as np
from GridCal.Engine import *
from matplotlib import pyplot as plt
import pandas as pd
import os
import time
import scipy
scipy.ALLOW_THREADS = True

np.set_printoptions(precision=4, linewidth=100000)


def determine_branch_indices(circuit):
    """
    VSC Control modes:

    in the paper's scheme:
    from -> DC
    to   -> AC

    |   Mode    |   const.1 |   const.2 |   type    |
    -------------------------------------------------
    |   1       |   theta   |   Vac     |   I       |
    |   2       |   Pf      |   Qac     |   I       |
    |   3       |   Pf      |   Vac     |   I       |
    -------------------------------------------------
    |   4       |   Vdc     |   Qac     |   II      |
    |   5       |   Vdc     |   Vac     |   II      |
    -------------------------------------------------
    |   6       | Vdc droop |   Qac     |   III     |
    |   7       | Vdc droop |   Vac     |   III     |
    -------------------------------------------------

    Indices where each control goes:

     Device      |  Ipf	Iqz	Ivf	Ivt	Iqt   (caIpf is Ish from the paper, Ipf makes more sense sine Pf is what is being ccontrolled)
    ------------------------------------
    VSC 1	     |  0	1	0	1	0   |   AC voltage control (voltage “to”)
    VSC 2	     |  1	1	0	0	1   |   Active and reactive power control
    VSC 3	     |  1	1	0	1	0   |   Active power and AC voltage control
    VSC 4	     |  0	0	1	0	1   |   Dc voltage and Reactive power flow control
    VSC 5	     |  0	0	1	1	0   |   Ac and Dc voltage control
    ------------------------------------
    Transformer 0|	0	0	0	0	0   |   Fixed transformer
    Transformer 1|	1	0	0	0	0   |   Phase shifter → controls power
    Transformer 2|	0	0	1	0	0   |   Control the voltage at the “from” side
    Transformer 3|	0	0	0	1	0   |   Control the voltage at the “to” side
    Transformer 4|	1	0	1	0	0   |   Control the power flow and the voltage at the “from” side
    Transformer 5|	1	0	0	1	0   |   Control the power flow and the voltage at the “to” side
    ------------------------------------


    """

    # indices in the global branch scheme
    idx_pf = list()  # what the paper calls Ish
    idx_qz = list()
    idx_vf = list()
    idx_vt = list()
    idx_qt = list()

    for k, tpe in enumerate(circuit.control_mode):

        f = circuit.F[k]
        t = circuit.T[k]

        if tpe == TransformerControlType.fixed:
            pass

        elif tpe == TransformerControlType.angle:
            idx_pf.append(k)

        elif tpe == TransformerControlType.v_from:
            idx_vf.append(f)

        elif tpe == TransformerControlType.v_to:
            idx_vt.append(t)

        elif tpe == TransformerControlType.angle_v_from:
            idx_pf.append(k)
            idx_vf.append(f)

        elif tpe == TransformerControlType.angle_v_to:
            idx_pf.append(k)
            idx_vt.append(t)

        elif tpe == ConverterControlType.theta_vac:
            idx_qz.append(k)
            idx_vt.append(t)

        elif tpe == ConverterControlType.pf_qac:
            idx_qz.append(k)
            idx_pf.append(k)
            idx_qt.append(k)

        elif tpe == ConverterControlType.pf_vac:
            idx_qz.append(k)
            idx_pf.append(k)
            idx_vt.append(t)

        elif tpe == ConverterControlType.vdc_qac:
            idx_vf.append(f)
            idx_qt.append(k)

        elif tpe == ConverterControlType.vdc_vac:
            idx_vf.append(f)
            idx_vt.append(t)

        elif tpe == 0:
            pass

        else:
            raise Exception('Unknown control type:' + str(tpe))

    return idx_pf, idx_qz, idx_vf, idx_vt, idx_qt


def compile_y2(circuit, m, theta, Beq, If):
    """

    :param circuit:
    :param m:
    :param theta:
    :param Beq:
    :param If:
    :return:
    """

    # form the connectivity matrices with the states applied -------------------------------------------------------
    br_states_diag = sp.diags(circuit.branch_active)
    Cf = br_states_diag * circuit.C_branch_bus_f
    Ct = br_states_diag * circuit.C_branch_bus_t

    # compute G-switch
    Gsw = circuit.G0 * np.power(If / circuit.Inom, 2.0)

    # SHUNT --------------------------------------------------------------------------------------------------------
    Yshunt_from_devices = circuit.C_bus_shunt * (circuit.shunt_admittance * circuit.shunt_active / circuit.Sbase)

    # form the admittance matrices ---------------------------------------------------------------------------------

    ys = 1.0 / (circuit.R + 1.0j * circuit.X)  # Y1
    # vsc_m2 = 0.8660254037844386 * vsc_m  # sqrt(3)/2 * m

    # compose the primitives
    Yff = ys
    Yft = -ys / (m * np.exp(1.0j * theta))
    Ytf = -ys / (m * np.exp(-1.0j * theta))
    Ytt = Gsw + (ys + 1.0j * Beq) / (m * m)

    # compose the matrices
    Yf = sp.diags(Yff) * Cf + sp.diags(Yft) * Ct
    Yt = sp.diags(Ytf) * Cf + sp.diags(Ytt) * Ct
    Ybus = sp.csc_matrix(Cf.T * Yf + Ct.T * Yt) + sp.diags(Yshunt_from_devices)

    return Ybus, Yf, Yt


# def compute_g(V, S0, m, theta, Beq, If, Pset, Qset,
#               pqpv, pq, idx_pf, idx_qz, idx_vf, idx_vt, idx_qt):
#     """
#
#     :param V:
#     :param S0:
#     :param m:
#     :param theta:
#     :param Beq:
#     :param If:
#     :param pqpv:
#     :param pq:
#     :param idx_pf:
#     :param idx_qz:
#     :param idx_vf:
#     :param idx_vt:
#     :param idx_qt:
#     :return:
#     """
#
#     Ybus, Yf, Yt = compile_y2(circuit=nc, m=m, theta=theta, Beq=Beq, If=If)
#
#     S_calc = V * np.conj(Ybus * V)
#
#     # equation (6)
#     gs = S_calc - S0
#
#     If = Yf * V
#     It = Yt * V
#     Vf = nc.C_branch_bus_f * V
#     Vt = nc.C_branch_bus_t * V
#     Sf = Vf * np.conj(If)  # eq. (8)
#     St = Vt * np.conj(It)  # eq. (9)
#
#     gp = gs.real[pqpv]  # eq. (12)
#     gq = gs.imag[pq]  # eq. (13)
#
#     # controls that the specified power flow is met
#     # Applicable to:
#     # - VSC devices where the power flow is set, this is types 2 and 3
#     # - Transformer devices where the power flow is set (is it?, apparently it only depends on the value of theta)
#     gsh = Sf.real[idx_pf] - Pset[idx_pf]  # eq. (14)
#
#     # controls that 'Beq' absorbs the reactive power.
#     # Applicable to:
#     # - All the VSC converters (is it?)
#     gqz = Sf.imag[idx_qz]  # eq. (15)
#
#     # Controls that 'ma' modulates to control the "voltage from" module.
#     # Applicable to:
#     # - Transformers that control the "from" voltage side
#     # - VSC that control the "from" voltage side, this is types 4 and 5
#     gvf = gs.imag[idx_vf]  # eq. (16)
#
#     # Controls that 'ma' modulates to control the "voltage to" module.
#     # Applicable to:
#     # - Transformers that control the "to" voltage side
#     # - VSC that control the "from" voltage side, this is types 1, 3, 5 and 7
#     gvt = gs.imag[idx_vt]  # eq. (17)
#
#     # controls that the specified reactive power flow is met, this is Qf=0
#     # Applicable to:
#     # - All VSC converters (is it?)  this is types 2, 4, 6
#     gqt = St.imag[idx_qt] - Qset[idx_qt]  # eq. (18)
#
#     # return the complete mismatch function
#     return np.r_[gp, gq, gsh, gqz, gvf, gvt, gqt]
#

def dSbus_dV(Ybus, V, I):
    """
    Computes partial derivatives of power injection w.r.t. voltage.
    :param Ybus: Admittance matrix
    :param V: Bus voltages array
    :param I: Bus current injections array
    :return:
    """
    '''
    Computes partial derivatives of power injection w.r.t. voltage.

    Returns two matrices containing partial derivatives of the complex bus
    power injections w.r.t voltage magnitude and voltage angle respectively
    (for all buses). If C{Ybus} is a sparse matrix, the return values will be
    also. The following explains the expressions used to form the matrices::

        Ibus = Ybus * V - I

        S = diag(V) * conj(Ibus) = diag(conj(Ibus)) * V

    Partials of V & Ibus w.r.t. voltage magnitudes::
        dV/dVm = diag(V / abs(V))
        dI/dVm = Ybus * dV/dVm = Ybus * diag(V / abs(V))

    Partials of V & Ibus w.r.t. voltage angles::
        dV/dVa = j * diag(V)
        dI/dVa = Ybus * dV/dVa = Ybus * j * diag(V)

    Partials of S w.r.t. voltage magnitudes::
        dS/dVm = diag(V) * conj(dI/dVm) + diag(conj(Ibus)) * dV/dVm
               = diag(V) * conj(Ybus * diag(V / abs(V)))
                                        + conj(diag(Ibus)) * diag(V / abs(V))

    Partials of S w.r.t. voltage angles::
        dS/dVa = diag(V) * conj(dI/dVa) + diag(conj(Ibus)) * dV/dVa
               = diag(V) * conj(Ybus * j * diag(V))
                                        + conj(diag(Ibus)) * j * diag(V)
               = -j * diag(V) * conj(Ybus * diag(V))
                                        + conj(diag(Ibus)) * j * diag(V)
               = j * diag(V) * conj(diag(Ibus) - Ybus * diag(V))

    For more details on the derivations behind the derivative code used
    in PYPOWER information, see:

    [TN2]  R. D. Zimmerman, "AC Power Flows, Generalized OPF Costs and
    their Derivatives using Complex Matrix Notation", MATPOWER
    Technical Note 2, February 2010.
    U{http://www.pserc.cornell.edu/matpower/TN2-OPF-Derivatives.pdf}

    @author: Ray Zimmerman (PSERC Cornell)
    '''

    ib = range(len(V))

    Ibus = Ybus * V - I

    diagV = sparse((V, (ib, ib)))
    diagIbus = sparse((Ibus, (ib, ib)))
    diagVnorm = sparse((V / np.abs(V), (ib, ib)))

    dS_dVm = diagV * conj(Ybus * diagVnorm) + conj(diagIbus) * diagVnorm
    dS_dVa = 1.0j * diagV * conj(diagIbus - Ybus * diagV)

    return dS_dVm, dS_dVa


def Jacobian(Ybus, V, Ibus, pq, pvpq):
    """
    Computes the system Jacobian matrix
    Args:
        Ybus: Admittance matrix
        V: Array of nodal voltages
        Ibus: Array of nodal current injections
        pq: Array with the indices of the PQ buses
        pvpq: Array with the indices of the PV and PQ buses

    Returns:
        The system Jacobian matrix
    """
    dS_dVm, dS_dVa = dSbus_dV(Ybus, V, Ibus)  # compute the derivatives

    J11 = dS_dVa[array([pvpq]).T, pvpq].real
    J12 = dS_dVm[array([pvpq]).T, pq].real
    J21 = dS_dVa[array([pq]).T, pvpq].imag
    J22 = dS_dVm[array([pq]).T, pq].imag

    J = vstack([hstack([J11, J12]),
                hstack([J21, J22])], format="csr")

    return J


def split_x(x, pq, pvpq, idx_pf, idx_qz, idx_vf, idx_vt, idx_qt):
    """

    :param x:
    :param pq:
    :param pvpq:
    :param idx_pf:
    :param idx_qz:
    :param idx_vf:
    :param idx_vt:
    :param idx_qt:
    :return:
    """
    a = 0
    b = len(pvpq)
    va= x[a:b]

    a = b
    b += len(pq)
    vm = x[a:b]

    a = b
    b += len(idx_pf)
    theta1 = x[a:b]

    a = b
    b += len(idx_qz)
    Beq1 = x[a:b]  # Beq for Qflow = 0

    a = b
    b += len(idx_vf)
    m1 = x[a:b]  # m controlling Vf

    a = b
    b += len(idx_vt)
    m2 = x[a:b]  # m controlling Vt

    a = b
    b += len(idx_qt)
    Beq2 = x[a:b]  # Beq for Qflow = Qset

    return va, vm, theta1, Beq1, m1, m2, Beq2


def gx_function(x, args):
    """

    :param x:
    :param args:
    :return:
    """
    nc, pq, pvpq, idx_pf, idx_qz, idx_vf, idx_vt, idx_qt, Yf, Yt, S0, Pset, Qset, If, va_, vm_, m_, theta_, Beq_ = args

    va = va_.copy()
    vm = vm_.copy()
    m = m_.copy()
    theta = theta_.copy()
    Beq = Beq_.copy()

    # update the variables
    va1, vm1, theta1, Beq1, m1, m2, Beq2 = split_x(x, pq, pvpq, idx_pf, idx_qz, idx_vf, idx_vt, idx_qt)
    va[pvpq] = va1
    vm[pq] = vm1
    theta[idx_pf] = theta1
    Beq[idx_qz] = Beq1
    m[idx_vf] = m1
    m[idx_vt] = m2
    Beq[idx_qt] = Beq2

    # compose the voltage
    V = vm * np.exp(1.0j * va)

    # compute branch flows
    If = Yf * V
    It = Yt * V
    Vf = nc.C_branch_bus_f * V
    Vt = nc.C_branch_bus_t * V
    Sf = Vf * np.conj(If)  # eq. (8)
    St = Vt * np.conj(It)  # eq. (9)

    # compute admittances as a function of the branch variables
    Ybus, Yf, Yt = compile_y2(circuit=nc, m=m, theta=theta, Beq=Beq, If=If)

    # compute the new mismatch (g)
    S_calc = V * np.conj(Ybus * V)  # compute Bus power injections
    gs = S_calc - S0  # equation (6)
    gp = gs.real[pvpq]  # eq. (12)
    gq = gs.imag[pq]  # eq. (13)
    gsh = Sf.real[idx_pf] - Pset[idx_pf]  # eq. (14) controls that the specified power flow is met
    gqz = Sf.imag[idx_qz]  # eq. (15) controls that 'Beq' absorbs the reactive power.
    gvf = gs.imag[idx_vf]  # eq. (16) Controls that 'ma' modulates to control the "voltage from" module.
    gvt = gs.imag[idx_vt]  # eq. (17) Controls that 'ma' modulates to control the "voltage to" module.
    gqt = St.imag[idx_qt] - Qset[idx_qt]  # eq. (18) controls that the specified reactive power flow is met
    g = np.r_[gp, gq, gsh, gqz, gvf, gvt, gqt]  # complete mismatch function

    return g


def numerical_jacobian(f, x, args, dx=1e-8):
    """
    Compute the numerical Jacobian of a function
    :param f: function to evaluate
    :param x: "point" at which to evaluate the jacobian
    :param args: Extra arguments to pass to the function
    :param dx: tolerance
    :return: Jacobian matrix
    """
    n = len(x)
    f0 = f(x, args)
    jac = np.zeros((n, n))
    for j in range(n):  # through columns to allow for vector addition
        Dxj = (np.abs(x[j]) * dx if x[j] != 0 else dx)
        x_plus = [(xi if k != j else xi + Dxj) for k, xi in enumerate(x)]
        f1 = f(x_plus, args)
        col = (f1 - f0) / Dxj
        jac[:, j] = col
    return jac


def nr_acdc(nc: AcDcSnapshotCircuit):
    """

    :param nc:
    :return:
    """
    # compute the indices of the converter/transformer variables from their control strategies
    idx_pf, idx_qz, idx_vf, idx_vt, idx_qt = determine_branch_indices(circuit=nc)

    # initialize the variables
    V = nc.Vbus
    S0 = nc.Sbus
    Pset = nc.Pset / nc.Sbase
    Qset = nc.Qset / nc.Sbase
    pq = nc.pq.copy()
    pvpq_orig = np.r_[nc.pv, pq]

    # the elements of PQ that exist in the control indices Ivf and Ivt must be passed from the PQ to the PV list
    # otherwise those variables would be in two sets of equations
    i_ctrl_v = np.unique(np.r_[idx_vf, idx_vt])
    for val in pq:
        if val in i_ctrl_v:
            pq = pq[pq != val]

    # compose the new pvpq indices à la NR
    pv = np.unique(np.r_[i_ctrl_v, nc.pv])
    pv.sort()
    pvpq = np.r_[pv, pq]
    npqpv = len(pvpq)
    tolerance = 1e-6
    max_iter = 4

    # initialize variables
    va = np.angle(V)
    vm = np.abs(V)
    m = nc.m.copy()
    theta = nc.theta.copy()
    Beq = nc.Beq.copy() * 0
    Ybus, Yf, Yt = compile_y2(circuit=nc, m=m, theta=theta, Beq=Beq, If=nc.Inom)

    # compute branch flows
    If = Yf * V
    It = Yt * V
    Vf = nc.C_branch_bus_f * V
    Vt = nc.C_branch_bus_t * V
    Sf = Vf * np.conj(If)  # eq. (8)
    St = Vt * np.conj(It)  # eq. (9)

    # compute admittances as a function of the branch variables
    Ybus, Yf, Yt = compile_y2(circuit=nc, m=m, theta=theta, Beq=Beq, If=If)

    # compute the mismatch (g)
    S_calc = V * np.conj(Ybus * V)  # compute Bus power injections
    gs = S_calc - S0  # equation (6)
    gp = gs.real[pvpq]  # eq. (12)
    gq = gs.imag[pq]  # eq. (13)
    gsh = Sf.real[idx_pf] - Pset[idx_pf]  # eq. (14) controls that the specified power flow is met
    gqz = Sf.imag[idx_qz]  # eq. (15) controls that 'Beq' absorbs the reactive power.
    gvf = gs.imag[idx_vf]  # eq. (16) Controls that 'ma' modulates to control the "voltage from" module.
    gvt = gs.imag[idx_vt]  # eq. (17) Controls that 'ma' modulates to control the "voltage to" module.
    gqt = St.imag[idx_qt] - Qset[idx_qt]  # eq. (18)  controls that the specified reactive power flow is met
    g = np.r_[gp, gq, gsh, gqz, gvf, gvt, gqt]  # return the complete mismatch function

    # compose the initial x value
    x = np.r_[va[pvpq], vm[pq], theta[idx_pf], Beq[idx_qz], m[idx_vf], m[idx_vt], Beq[idx_qt]]

    # compute the error
    ff = np.r_[gs[pvpq_orig].real, gs[pq].imag]  # concatenate to form the mismatch function
    norm_f = 0.5 * ff.dot(ff)
    iterations = 0

    # compose equation names
    eq_names = ['gp' + str(k) for k in pvpq] \
               + ['gq' + str(k) for k in pq] \
               + ['gsh' + str(k) for k in idx_pf] \
               + ['gqz' + str(k) for k in idx_qz] \
               + ['gvf' + str(k) for k in idx_vf] \
               + ['gvt' + str(k) for k in idx_vt] \
               + ['gqf' + str(k) for k in idx_qt]

    var_names = ['va' + str(k) for k in pvpq] \
                + ['vm' + str(k) for k in pq] \
                + ['Ɵ' + str(k) for k in idx_pf] \
                + ['Beq' + str(k) for k in idx_qz] \
                + ['m' + str(k) for k in idx_vf] \
                + ['m' + str(k) for k in idx_vt] \
                + ['Beq' + str(k) for k in idx_qt]

    while norm_f > tolerance and iterations < max_iter:
        print('-' * 200)

        # compute the numerical Jacobian
        J = numerical_jacobian(gx_function,
                               x,
                               args=(nc, pq, pvpq, idx_pf, idx_qz, idx_vf, idx_vt, idx_qt,
                                     Yf, Yt, S0, Pset, Qset, If,
                                     va, vm, m, theta, Beq))

        print('J:')
        print(pd.DataFrame(data=J, columns=var_names, index=eq_names))
        print('x:')
        print(pd.DataFrame(data=x, index=var_names, columns=['']).transpose())

        print('g:')
        print(pd.DataFrame(data=g, index=var_names, columns=['']).transpose())

        # solve the increments
        dx = np.linalg.solve(J, g)

        print('dx:')
        print(pd.DataFrame(data=dx, index=var_names, columns=['']).transpose())

        # update the point
        x -= dx

        # update the variables
        va1, vm1, theta1, Beq1, m1, m2, Beq2 = split_x(x, pq, pvpq, idx_pf, idx_qz, idx_vf, idx_vt, idx_qt)
        va[pvpq] = va1
        vm[pq] = vm1
        theta[idx_pf] = theta1
        Beq[idx_qz] = Beq1
        m[idx_vf] = m1
        m[idx_vt] = m2
        Beq[idx_qt] = Beq2

        # compose the voltage
        V = vm * np.exp(1.0j * va)

        # compute branch flows
        If = Yf * V
        It = Yt * V
        Vf = nc.C_branch_bus_f * V
        Vt = nc.C_branch_bus_t * V
        Sf = Vf * np.conj(If)  # eq. (8)
        St = Vt * np.conj(It)  # eq. (9)

        # compute admittances as a function of the branch variables
        Ybus, Yf, Yt = compile_y2(circuit=nc, m=m, theta=theta, Beq=Beq, If=If)

        # compute the new mismatch (g)
        S_calc = V * np.conj(Ybus * V)  # compute Bus power injections
        gs = S_calc - S0  # equation (6)
        gp = gs.real[pvpq]  # eq. (12)
        gq = gs.imag[pq]  # eq. (13)
        gsh = Sf.real[idx_pf] - Pset[idx_pf]  # eq. (14) controls that the specified power flow is met
        gqz = Sf.imag[idx_qz]  # eq. (15) controls that 'Beq' absorbs the reactive power.
        gvf = gs.imag[idx_vf]  # eq. (16) Controls that 'ma' modulates to control the "voltage from" module.
        gvt = gs.imag[idx_vt]  # eq. (17) Controls that 'ma' modulates to control the "voltage to" module.
        gqt = St.imag[idx_qt] - Qset[idx_qt]  # eq. (18) controls that the specified reactive power flow is met
        g = np.r_[gp, gq, gsh, gqz, gvf, gvt, gqt]  # complete mismatch function

        # compute the error
        ff = np.r_[gs[pvpq_orig].real, gs[pq].imag]  # concatenate to form the mismatch function
        norm_f = 0.5 * ff.dot(ff)
        print('error:\n', norm_f)

        iterations += 1

    print('END', '-' * 200)
    print('V:\n', V)
    print('Sf:\n', Sf)
    print('error:', norm_f)

    return norm_f, V, m, theta, Beq

########################################################################################################################
#  MAIN
########################################################################################################################
if __name__ == "__main__":

    np.set_printoptions(linewidth=10000)
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    fname = '/home/santi/Documentos/GitHub/GridCal/Grids_and_profiles/grids/LineHVDCGrid.gridcal'
    grid = FileOpen(fname).open()

    ####################################################################################################################
    # Compile
    ####################################################################################################################
    nc_ = compile_acdc_snapshot_circuit(grid)

    res = nr_acdc(nc=nc_)

