"""IPX800V5 Counter."""
from .const import OBJECT_COUNTER
from .ipx800 import IPX800
from .object import Object


class Counter(Object):
    def __init__(self, ipx: IPX800, obj_number: int):
        super().__init__(ipx, OBJECT_COUNTER, obj_number)
        self.ana_state_id = self._config["anaOut_id"]
        self.ana_command_id = self._config["anaSetValue_id"]

    @property
    async def value(self) -> int:
        """Return the current counter value."""
        return int(await self._ipx.get_ana(self.ana_state_id))

    async def set_value(self, value: int) -> None:
        """Set target temperature."""
        await self._ipx.update_ana(self.ana_command_id, value)
