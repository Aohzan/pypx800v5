"""IPX800V5 X-010V."""

from .const import EXT_X010V as ext_type
from .extension import Extension
from .ipx800 import IPX800


class X010V(Extension):
    """Represent a X-010V output."""

    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number, output_number)
        self.io_state_id = self._config["ioOn_id"][output_number - 1]
        self.io_command_id = self._config["ioOn_id"][output_number - 1]
        self.ana_level_id = self._config["anaLevel_id"][output_number - 1]
        self.ana_command_id = self._config["anaCommand_id"][output_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current output status."""
        return await self._ipx.get_io(self.io_state_id)

    @property
    async def level(self) -> int:
        """Return the current output level from 0 to 100."""
        return int(await self._ipx.get_ana(self.ana_level_id))

    async def on(self) -> None:
        """Turn on the ouput."""
        await self._ipx.update_io(self.io_command_id, True)

    async def off(self) -> None:
        """Turn off the ouput."""
        await self._ipx.update_io(self.io_command_id, False)

    async def toggle(self) -> None:
        """Toggle the ouput."""
        await self._ipx.update_io(self.io_command_id, True, "toggle")

    async def set_level(self, level: int) -> None:
        """Set the output level between 0 and 100."""
        if not 0 <= level <= 100:
            raise ValueError("Level must be between 0 and 100")
        await self._ipx.update_ana(self.ana_command_id, level)
