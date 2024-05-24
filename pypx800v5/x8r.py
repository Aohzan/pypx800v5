"""IPX800V5 X-8R."""

from .const import EXT_X8R as ext_type
from .extension import Extension
from .ipx800 import IPX800


class X8R(Extension):
    """Represent an X-8R relay."""

    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number, output_number)
        self.io_state_id = self._config["ioOutputState_id"][output_number - 1]
        self.io_command_id = self._config["ioOutput_id"][output_number - 1]
        self.io_longpush_id = self._config["ioLongPush_id"][output_number - 1]

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
