"""IPX800V5 Counter."""

from .const import OBJECT_COUNTER as obj_type
from .ipx800 import IPX800
from .object import Object


class Counter(Object):
    """Represent an IPX800 counter object."""

    def __init__(self, ipx: IPX800, obj_number: int):
        """Init the object."""
        super().__init__(ipx, obj_type, obj_number)
        self.ana_state_id = self._config["anaOut_id"]
        self.ana_command_id = self._config["anaSetValue_id"]
        self.ana_step_id = self._config["anaPulseValue_id"]
        self.io_step_id = self._config["ioSet_id"]

    @property
    async def step(self) -> float:
        """Return the step configured."""
        return float(await self._ipx.get_ana(self.ana_step_id))

    @property
    async def value(self) -> float:
        """Return the current counter value."""
        return float(await self._ipx.get_ana(self.ana_state_id))

    async def set_value(self, value: float) -> None:
        """Set target temperature."""
        await self._ipx.update_ana(self.ana_command_id, value)
        await self._ipx.update_io(self.io_step_id, True, "toggle")
