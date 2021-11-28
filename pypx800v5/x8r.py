"""IPX800V5 X-8R."""
from .const import TYPE_IO
from .extension import Extension
from .ipx800 import IPX800

API_PATH = "ebx/x8r"
EXT_TYPE = "x8r"

KEY_STATUS_ONOFF = "ioOutputState"
KEY_SET_ONOFF = "ioOutput"


class X8R(Extension):
    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        super().__init__(ipx, EXT_TYPE, ext_number, output_number)
        self.io_state_id = self._config["ioOutputState_id"][output_number - 1]
        self.io_command_id = self._config["ioOutput_id"][output_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current X-8R status."""
        return await self._ipx.get_io(self.io_state_id)

    async def on(self) -> None:
        """Turn on a X-8R."""
        await self._ipx.update_io(self.io_command_id, True)

    async def off(self) -> None:
        """Turn off a X-8R."""
        await self._ipx.update_io(self.io_command_id, False)

    async def toggle(self) -> None:
        """Toggle a X-8R."""
        await self._ipx.update_io(self.io_command_id, True, "toggle")
