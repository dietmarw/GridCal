from typing import Union, Any, List

from GridCalEngine.Devices.Parents.editable_device import EditableDevice, DeviceType, SubObjectType
from GridCalEngine.Devices.Aggregation.investments_group import InvestmentsGroup


class Investment(EditableDevice):
    """
    Investment
    """

    def __init__(self,
                 idtag: Union[str, None] = None,
                 device_idtag: Union[str, None] = None,
                 name="Investment",
                 code='',
                 CAPEX=0.0,
                 OPEX=0.0,
                 status: bool = True,
                 group: InvestmentsGroup = None,
                 template_src: Union[DeviceType.Transformer2WDevice, DeviceType.LineDevice] = None,
                 comment: str = ""):
        """
        Investment object formed by CAPEX, OPEX, status (on/off) and possible template
        :param idtag: String. Element unique identifier
        :param name: String. Contingency name
        :param code: String. Contingency code name
        :param CAPEX: Float. Capital expenditures
        :param OPEX: Float. Operating expenditures
        :param status: If true the investment activates when applied, otherwise is deactivated
        :param group: InvestmentGroup. Investment group
        :param template_src: DeviceType. Possible templates of each component
        :param comment: Comment
        """

        EditableDevice.__init__(self,
                                idtag=idtag,
                                code=code,
                                name=name,
                                device_type=DeviceType.InvestmentDevice,
                                comment=comment)

        # Contingency type
        self.device_idtag = device_idtag
        self.CAPEX = CAPEX
        self.OPEX = OPEX
        self._group: InvestmentsGroup = group
        self.status: bool = status

        self.register(key='device_idtag', units='', tpe=str, definition='Unique ID')
        self.register(key='CAPEX', units='M€', tpe=float,
                      definition='Capital expenditures. This is the initial investment.')
        self.register(key='OPEX', units='M€', tpe=float,
                      definition='Operation expenditures. Maintenance costs among other recurrent costs.')
        self.register(key='status', units='', tpe=bool,
                      definition='If true the investment activates when applied, otherwise is deactivated.')
        self.register(key='group', units='', tpe=DeviceType.InvestmentsGroupDevice, definition='Investment group')

        if template_src is not None:
            if template_src.device_type == DeviceType.Transformer2WDevice:
                self.template = template_src.possible_transformer_types.data
            elif template_src.device_type == DeviceType.SequenceLineDevice:
                self.template = template_src.possible_sequence_line_types.data
            elif template_src.device_type == DeviceType.UnderGroundLineDevice:
                self.template = template_src.possible_underground_line_types.data
            elif template_src.device_type == DeviceType.OverheadLineTypeDevice:
                self.template = template_src.possible_tower_types.data
            else:
                raise Exception(f'Templates for {template_src.type} not recognized')
        else:
            self.template = None

        self.register(key='template', units='', tpe=SubObjectType.ObjectsList,
                          definition='Possible templates of each component')

    @property
    def group(self) -> InvestmentsGroup:
        """
        Group of investments
        :return:
        """
        return self._group

    @group.setter
    def group(self, val: InvestmentsGroup):
        self._group = val

    @property
    def category(self):
        """
        Display the group category
        :return:
        """
        return self.group.category

    @category.setter
    def category(self, val):
        # The category is set through the group, so no implementation here
        pass

    # @property
    # def template(self):
    #     """
    #     Template of component
    #     :return:
    #     """
    #     return self.template
    #
    # @template.setter
    # def template(self, val):
    #     self.template = val
