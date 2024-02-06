# GridCal
# Copyright (C) 2015 - 2024 Santiago Peñate Vera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import pandas as pd
from matplotlib import pyplot as plt
from GridCalEngine.enumerations import DeviceType, BuildStatus, ExternalGridMode
from GridCalEngine.Core.Devices.Injections.injection_template import LoadLikeTemplate
from GridCalEngine.Core.Devices.profile import Profile


class ExternalGrid(LoadLikeTemplate):

    def __init__(self, name='External grid', idtag=None, code='', active=True, substituted_device_id: str = '',
                 Vm=1.0, Va=0.0, P=0.0, Q=0.0,
                 mttf=0.0, mttr=0.0, mode: ExternalGridMode = ExternalGridMode.PQ,
                 capex=0, opex=0, build_status: BuildStatus = BuildStatus.Commissioned):
        """
        External grid device
        In essence, this is a slack-enforcer device
        :param name:
        :param idtag:
        :param code:
        :param active:
        :param substituted_device_id:
        :param Vm:
        :param Va:
        :param P:
        :param Q:
        :param mttf:
        :param mttr:
        :param mode:
        :param capex:
        :param opex:
        :param build_status:
        """

        LoadLikeTemplate.__init__(self,
                                  name=name,
                                  idtag=idtag,
                                  code=code,
                                  bus=None,
                                  cn=None,
                                  active=active,
                                  P=P,
                                  Q=Q,
                                  Cost=0,
                                  mttf=mttf,
                                  mttr=mttr,
                                  capex=capex,
                                  opex=opex,
                                  build_status=build_status,
                                  device_type=DeviceType.ExternalGridDevice)

        self.mode = mode

        self.substituted_device_id = substituted_device_id

        # Impedance in equivalent MVA
        self.Vm = Vm
        self.Va = Va
        self.Vm_prof = Profile(default_value=Vm)
        self.Va_prof = Profile(default_value=Va)

        self.register(key='mode', units='', tpe=ExternalGridMode,
                      definition='Operation mode of the external grid (voltage or load)')
        self.register(key='substituted_device_id', units='', tpe=str,
                      definition='idtag of the device that was substituted by this external grid equivalent')
        self.register(key='Vm', units='p.u.', tpe=float, definition='Active power', profile_name='Vm_prof')
        self.register(key='Va', units='radians', tpe=float, definition='Reactive power', profile_name='Va_prof')

    def get_properties_dict(self, version=3):
        """
        Get json dictionary
        :return:
        """

        d = {'id': self.idtag,
             'type': 'external_grid',
             'phases': 'ps',
             'name': self.name,
             'bus': self.bus.idtag,
             'active': self.active,
             'Vm': self.Vm,
             'Va': self.Va,
             'P': self.P,
             'Q': self.Q,
             'Cost': self.Cost}

        if self.active_prof is not None:
            d['active_profile'] = self.active_prof.tolist()
            d['Vm_prof'] = self.Vm_prof.tolist()
            d['Va_prof'] = self.Va_prof.tolist()
            d['P_prof'] = self.P_prof.tolist()
            d['Q_prof'] = self.Q_prof.tolist()
            d['Cost_prof'] = self.Cost_prof.tolist()

        return d

    def get_profiles_dict(self, version=3):
        """

        :return:
        """
        if self.active_prof is not None:
            active_profile = self.active_prof.tolist()
            Vm_prof = self.Vm_prof.tolist()
            Va_prof = self.Va_prof.tolist()
            P_prof = self.P_prof.tolist()
            Q_prof = self.Q_prof.tolist()
        else:
            active_profile = list()
            Vm_prof = list()
            Va_prof = list()
            P_prof = list()
            Q_prof = list()

        return {'id': self.idtag,
                'active': active_profile,
                'vm': Vm_prof,
                'va': Va_prof,
                'P': P_prof,
                'Q': Q_prof}

    def plot_profiles(self, time=None, show_fig=True):
        """
        Plot the time series results of this object
        :param time: array of time values
        :param show_fig: Show the figure?
        """

        if time is not None:
            fig = plt.figure(figsize=(12, 8))

            ax_1 = fig.add_subplot(211)
            ax_2 = fig.add_subplot(212)

            if self.mode == ExternalGridMode.VD:
                y1 = self.Vm_prof.toarray()
                title_1 = 'Voltage module'
                units_1 = 'p.u'

                y2 = self.Va_prof.toarray()
                title_2 = 'Voltage angle'
                units_2 = 'radians'

            elif self.mode == ExternalGridMode.PQ:
                y1 = self.P_prof.toarray()
                title_1 = 'Active Power'
                units_1 = 'MW'

                y2 = self.Q_prof.toarray()
                title_2 = 'Reactive power'
                units_2 = 'MVAr'

            else:
                raise Exception('Unrecognised external grid mode: ' + str(self.mode))

            ax_1.set_title(title_1, fontsize=14)
            ax_1.set_ylabel(units_1, fontsize=11)
            df = pd.DataFrame(data=y1, index=time, columns=[self.name])
            df.plot(ax=ax_1)

            df = pd.DataFrame(data=y2, index=time, columns=[self.name])
            ax_2.set_title(title_2, fontsize=14)
            ax_2.set_ylabel(units_2, fontsize=11)
            df.plot(ax=ax_2)

            plt.legend()
            fig.suptitle(self.name, fontsize=20)

            if show_fig:
                plt.show()
