"""IPX800V5 Tempo."""

from .const import OBJECT_TEMPO as obj_type
from .ipx800 import IPX800
from .object import Object


class Tempo(Object):
    """Represent an IPX800 tempo object."""

    def __init__(self, ipx: IPX800, obj_number: int):
        """Init the object."""
        super().__init__(ipx, obj_type, obj_number)
        self.io_state_id = self._config["ioOut_id"]
        self.io_enabled_id = self._config["ioEnable_id"]
        self.ana_time_id = self._config["anaTime1_id"]

    @property
    async def time(self) -> int:
        """Return the tempo delay time."""
        return int(await self._ipx.get_ana(self.ana_time_id))

    @property
    async def enabled(self) -> bool:
        """Return if the tempo is enabled."""
        return await self._ipx.get_io(self.io_enabled_id)

    @property
    async def status(self) -> bool:
        """Return the current status."""
        return await self._ipx.get_io(self.io_state_id)

    async def on(self) -> None:
        """Enable the tempo."""
        await self._ipx.update_io(self.io_enabled_id, True)

    async def off(self) -> None:
        """Disable the tempo."""
        await self._ipx.update_io(self.io_enabled_id, False)

    async def set_time(self, time: int) -> None:
        """Update tempo time."""
        params = {"anaTime1": time}
        await self._ipx._request_api(
            f"object/timer/{self._obj_id}",
            method="PUT",
            data=params,
        )
