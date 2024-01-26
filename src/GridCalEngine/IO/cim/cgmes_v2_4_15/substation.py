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
from GridCalEngine.IO.cim.cgmes_v2_4_15.equipment_container import EquipmentContainer
from GridCalEngine.IO.cim.cgmes_v2_4_15.dc_converter_unit import DCConverterUnit
from GridCalEngine.IO.cim.cgmes_v2_4_15.sub_geographical_region import SubGeographicalRegion
from GridCalEngine.IO.cim.cgmes_v2_4_15.voltage_level import VoltageLevel


class Substation(EquipmentContainer):
	def __init__(self, rdfid='', tpe='Substation'):
		EquipmentContainer.__init__(self, rdfid, tpe)

		self.DCConverterUnit: DCConverterUnit | None = None
		self.Region: SubGeographicalRegion | None = None
		self.VoltageLevels: VoltageLevel | None = None

		self.register_property(
			name='DCConverterUnit',
			class_type=DCConverterUnit,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='None',
			profiles=[]
		)
		self.register_property(
			name='Region',
			class_type=SubGeographicalRegion,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The SubGeographicalRegion containing the substation.',
			profiles=[]
		)
		self.register_property(
			name='VoltageLevels',
			class_type=VoltageLevel,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The voltage levels within this substation.',
			profiles=[]
		)
