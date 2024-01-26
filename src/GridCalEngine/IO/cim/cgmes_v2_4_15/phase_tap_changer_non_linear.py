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
from GridCalEngine.IO.cim.cgmes_v2_4_15.phase_tap_changer import PhaseTapChanger


class PhaseTapChangerNonLinear(PhaseTapChanger):
	def __init__(self, rdfid='', tpe='PhaseTapChangerNonLinear'):
		PhaseTapChanger.__init__(self, rdfid, tpe)

		self.voltageStepIncrement: float = 0.0
		self.xMax: float = 0.0
		self.xMin: float = 0.0

		self.register_property(
			name='voltageStepIncrement',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
		self.register_property(
			name='xMax',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.ohm,
			description='Reactance (imaginary part of impedance), at rated frequency.',
			profiles=[]
		)
		self.register_property(
			name='xMin',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.ohm,
			description='Reactance (imaginary part of impedance), at rated frequency.',
			profiles=[]
		)
