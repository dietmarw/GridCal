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
from GridCalEngine.IO.cim.cgmes_v2_4_15.season_day_type_schedule import SeasonDayTypeSchedule
from GridCalEngine.IO.cim.cgmes_v2_4_15.conform_load_group import ConformLoadGroup


class ConformLoadSchedule(SeasonDayTypeSchedule):
	def __init__(self, rdfid='', tpe='ConformLoadSchedule'):
		SeasonDayTypeSchedule.__init__(self, rdfid, tpe)

		self.ConformLoadGroup: ConformLoadGroup | None = None

		self.register_property(
			name='ConformLoadGroup',
			class_type=ConformLoadGroup,
			multiplier=UnitMultiplier.none,
			unit=UnitSymbol.none,
			description='The ConformLoadGroup where the ConformLoadSchedule belongs.',
			profiles=[]
		)
