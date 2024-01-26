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
from GridCalEngine.IO.cim.cgmes_v2_4_15.base_voltage import BaseVoltage
from GridCalEngine.IO.cim.cgmes_v2_4_15.terminal import Terminal
from GridCalEngine.IO.cim.cgmes_v2_4_15.sv_status import SvStatus


class ConductingEquipment(Equipment):
	def __init__(self, rdfid='', tpe='ConductingEquipment'):
		Equipment.__init__(self, rdfid, tpe)

		self.BaseVoltage: BaseVoltage | None = None
		self.Terminals: Terminal | None = None
		self.SvStatus: SvStatus | None = None

		self.register_property(
			name='BaseVoltage',
			class_type=BaseVoltage,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='All conducting equipment with this base voltage.  Use only when there is no voltage level container used and only one base voltage applies.  For example, not used for transformers.',
			profiles=[]
		)
		self.register_property(
			name='Terminals',
			class_type=Terminal,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Conducting equipment have terminals that may be connected to other conducting equipment terminals via connectivity nodes or topological nodes.',
			profiles=[]
		)
		self.register_property(
			name='SvStatus',
			class_type=SvStatus,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The status state variable associated with this conducting equipment.',
			profiles=[]
		)
