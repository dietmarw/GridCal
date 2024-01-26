# GridCal
# Copyright (C) 2015 - 2023 Santiago Peñate Vera
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
from GridCalEngine.IO.base.units import UnitMultiplier, UnitSymbol
from GridCalEngine.IO.cim.cgmes_v2_4_15.cgmes_enums import cgmesProfile
from GridCalEngine.IO.cim.cgmes_v2_4_15.equipment import Equipment
from GridCalEngine.IO.cim.cgmes_v2_4_15.control_area_generating_unit import ControlAreaGeneratingUnit
from GridCalEngine.IO.cim.cgmes_v2_4_15.rotating_machine import RotatingMachine
from GridCalEngine.IO.cim.cgmes_v2_4_15.gross_to_net_active_power_curve import GrossToNetActivePowerCurve


class GeneratingUnit(Equipment):
	def __init__(self, rdfid='', tpe='GeneratingUnit'):
		Equipment.__init__(self, rdfid, tpe)

		self.genControlSource: GeneratorControlSource = None
		self.governorSCD: float = 0.0
		self.initialP: float = 0.0
		self.longPF: float = 0.0
		self.maximumAllowableSpinningReserve: float = 0.0
		self.maxOperatingP: float = 0.0
		self.minOperatingP: float = 0.0
		self.nominalP: float = 0.0
		self.ratedGrossMaxP: float = 0.0
		self.ratedGrossMinP: float = 0.0
		self.ratedNetMaxP: float = 0.0
		self.shortPF: float = 0.0
		self.startupCost: float = 0.0
		self.variableCost: float = 0.0
		self.totalEfficiency: float = 0.0
		self.ControlAreaGeneratingUnit: ControlAreaGeneratingUnit | None = None
		self.RotatingMachine: RotatingMachine | None = None
		self.GrossToNetActivePowerCurves: GrossToNetActivePowerCurve | None = None
		self.normalPF: float = 0.0

		self.register_property(
			name='genControlSource',
			class_type=GeneratorControlSource,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The source of controls for a generating unit.',
			profiles=[]
		)
		self.register_property(
			name='governorSCD',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
		self.register_property(
			name='initialP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='longPF',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='A floating point number. The range is unspecified and not limited.',
			profiles=[]
		)
		self.register_property(
			name='maximumAllowableSpinningReserve',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='maxOperatingP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='minOperatingP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='nominalP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='ratedGrossMaxP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='ratedGrossMinP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='ratedNetMaxP',
			class_type=float,
			multiplier=UnitMultiplier.M,
			unit=UnitSymbol.W,
			description='Product of RMS value of the voltage and the RMS value of the in-phase component of the current.',
			profiles=[]
		)
		self.register_property(
			name='shortPF',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='A floating point number. The range is unspecified and not limited.',
			profiles=[]
		)
		self.register_property(
			name='startupCost',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=Currency.EUR,
			description='Amount of money.',
			profiles=[]
		)
		self.register_property(
			name='variableCost',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=Currency.EUR,
			description='Amount of money.',
			profiles=[]
		)
		self.register_property(
			name='totalEfficiency',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
		self.register_property(
			name='ControlAreaGeneratingUnit',
			class_type=ControlAreaGeneratingUnit,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='ControlArea specifications for this generating unit.',
			profiles=[]
		)
		self.register_property(
			name='RotatingMachine',
			class_type=RotatingMachine,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='A synchronous machine may operate as a generator and as such becomes a member of a generating unit.',
			profiles=[]
		)
		self.register_property(
			name='GrossToNetActivePowerCurves',
			class_type=GrossToNetActivePowerCurve,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='A generating unit may have a gross active power to net active power curve, describing the losses and auxiliary power requirements of the unit.',
			profiles=[]
		)
		self.register_property(
			name='normalPF',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='A floating point number. The range is unspecified and not limited.',
			profiles=[]
		)
