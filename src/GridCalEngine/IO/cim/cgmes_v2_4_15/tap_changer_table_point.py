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


class TapChangerTablePoint(object):
	def __init__(self, rdfid='', tpe='TapChangerTablePoint'):

		self.b: float = 0.0
		self.g: float = 0.0
		self.r: float = 0.0
		self.ratio: float = 0.0
		self.step: int = 0
		self.x: float = 0.0

		self.register_property(
			name='b',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
		self.register_property(
			name='g',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
		self.register_property(
			name='r',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
		self.register_property(
			name='ratio',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='A floating point number. The range is unspecified and not limited.',
			profiles=[]
		)
		self.register_property(
			name='step',
			class_type=int,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The tap step.',
			profiles=[]
		)
		self.register_property(
			name='x',
			class_type=float,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Percentage on a defined base.   For example, specify as 100 to indicate at the defined base.',
			profiles=[]
		)
