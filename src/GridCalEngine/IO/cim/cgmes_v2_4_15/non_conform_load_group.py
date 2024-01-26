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
from GridCalEngine.IO.cim.cgmes_v2_4_15.load_group import LoadGroup
from GridCalEngine.IO.cim.cgmes_v2_4_15.non_conform_load import NonConformLoad
from GridCalEngine.IO.cim.cgmes_v2_4_15.non_conform_load_schedule import NonConformLoadSchedule


class NonConformLoadGroup(LoadGroup):
	def __init__(self, rdfid='', tpe='NonConformLoadGroup'):
		LoadGroup.__init__(self, rdfid, tpe)

		self.EnergyConsumers: NonConformLoad | None = None
		self.NonConformLoadSchedules: NonConformLoadSchedule | None = None

		self.register_property(
			name='EnergyConsumers',
			class_type=NonConformLoad,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='Group of this ConformLoad.',
			profiles=[]
		)
		self.register_property(
			name='NonConformLoadSchedules',
			class_type=NonConformLoadSchedule,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The NonConformLoadSchedules in the NonConformLoadGroup.',
			profiles=[]
		)
