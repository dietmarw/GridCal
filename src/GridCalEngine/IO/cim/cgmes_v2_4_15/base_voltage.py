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
from GridCalEngine.IO.cim.cgmes_v2_4_15.identified_object import IdentifiedObject
from GridCalEngine.IO.cim.cgmes_v2_4_15.conducting_equipment import ConductingEquipment
from GridCalEngine.IO.cim.cgmes_v2_4_15.voltage_level import VoltageLevel
from GridCalEngine.IO.cim.cgmes_v2_4_15.transformer_end import TransformerEnd
from GridCalEngine.IO.cim.cgmes_v2_4_15.topological_node import TopologicalNode


class BaseVoltage(IdentifiedObject):
	def __init__(self, rdfid='', tpe='BaseVoltage'):
		IdentifiedObject.__init__(self, rdfid, tpe)

		self.nominalVoltage: float = 0.0
		self.ConductingEquipment: ConductingEquipment | None = None
		self.VoltageLevel: VoltageLevel | None = None
		self.TransformerEnds: TransformerEnd | None = None
		self.TopologicalNode: TopologicalNode | None = None

		self.register_property(
			name='nominalVoltage',
			class_type=float,
			multiplier=UnitMultiplier.k,
			unit=UnitSymbol.V,
			description='Electrical voltage, can be both AC and DC.',
			profiles=[]
		)
		self.register_property(
			name='ConductingEquipment',
			class_type=ConductingEquipment,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Base voltage of this conducting equipment.  Use only when there is no voltage level container used and only one base voltage applies.  For example, not used for transformers.',
			profiles=[]
		)
		self.register_property(
			name='VoltageLevel',
			class_type=VoltageLevel,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The voltage levels having this base voltage.',
			profiles=[]
		)
		self.register_property(
			name='TransformerEnds',
			class_type=TransformerEnd,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Transformer ends at the base voltage.  This is essential for PU calculation.',
			profiles=[]
		)
		self.register_property(
			name='TopologicalNode',
			class_type=TopologicalNode,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The topological nodes at the base voltage.',
			profiles=[]
		)
