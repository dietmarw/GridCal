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
from GridCalEngine.IO.cim.cgmes.cgmes_v3_0_0.devices.phase_tap_changer_non_linear import PhaseTapChangerNonLinear
from GridCalEngine.IO.cim.cgmes.cgmes_enums import cgmesProfile, UnitSymbol


class PhaseTapChangerAsymmetrical(PhaseTapChangerNonLinear):
	def __init__(self, rdfid='', tpe='PhaseTapChangerAsymmetrical'):
		PhaseTapChangerNonLinear.__init__(self, rdfid, tpe)

		self.windingConnectionAngle: float = None

		self.register_property(
			name='windingConnectionAngle',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.deg,
			description='''Measurement of angle in degrees.''',
			profiles=[]
		)
