"""Process"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ...modeling.parameters.conversion import Conversion
from ...utils.decorators import timer
from .operation import Operation

logger = logging.getLogger("energia")

if TYPE_CHECKING:
    from ..spatial.location import Location
    from ..temporal.periods import Periods


class Process(Operation):
    """
    Process converts one Resource to another Resource at some Location

    :param label: An optional label for the component. Defaults to None.
    :type label: str, optional
    :param citations: An optional citation or description for the component. Defaults to None.
    :type citations: str | list[str] | dict[str, str | list[str]], optional

    :ivar model: The model to which the component belongs.
    :vartype model: Model
    :ivar name: Set when the component is assigned as a Model attribute.
    :vartype name: str

    :ivar constraints: List of constraints associated with the component.
    :vartype constraints: list[str]
    :ivar domains: List of domains associated with the component.
    :vartype domains: list[Domain]
    :ivar aspects: Aspects associated with the component with domains.
    :vartype aspects: dict[Aspect, list[Domain]]
    :ivar conversion: Operational conversion associated with the operation. Defaults to None.
    :vartype conversion: Conversion, optional
    :ivar _conv: True if the operational conversion has been set. Defaults to False.
    :vartype _conv: bool
    :ivar fab: Material conversion associated with the operation. Defaults to None.
    :vartype fab: Conversion, optional
    :ivar _fab_balanced: True if the material conversion has been balanced. Defaults to False.
    :vartype _fab_balanced: bool
    :ivar locations: Locations at which the process is balanced. Defaults to [].
    :vartype locations: list[Location]
    :ivar charges: If the Process is Storage charging. Defaults to None.
    :vartype charges: Storage, optional
    :ivar discharges: If the Process is Storage discharging. Defaults to None.
    :vartype discharges: Storage, optional
    """

    def __init__(self, *args, label: str = "", citations: str = "", **kwargs):

        Operation.__init__(self, *args, label=label, citations=citations, **kwargs)

        # at which locations the process is balanced
        # Note that we do not need a conversion at every temporal scale.
        # once balanced at a location for a particular time,
        # if time != horizon, the individual streams are summed up anyway
        self.locations: list[Location] = []

        self.operate_conversion = Conversion(
            operation=self,
            aspect='operate',
            add="produce",
            sub="expend",
            attr_type="operate_conversion",
        )
        self.capacity_conversion = Conversion(
            operation=self,
            aspect='capacity',
            add="dispose",
            sub="use",
            attr_type="capacity_conversion",
            use_max_time=True,
        )

    @property
    def production(self) -> Conversion:
        """Production Conversion"""
        return self.operate_conversion

    @property
    def construction(self) -> Conversion:
        """Capacity Conversion"""
        return self.capacity_conversion

    @property
    def spaces(self) -> list[Location]:
        """Locations at which the process is balanced"""
        return self.locations
