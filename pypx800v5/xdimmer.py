"""IPX800V5 X-Dimmer."""

from .const import DEFAULT_TRANSITION
from .const import EXT_XDIMMER as ext_type
from .extension import Extension
from .ipx800 import IPX800


class XDimmer(Extension):
    """Represent an X-Dimmer light."""

    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number, output_number)
        self.io_state_id = self._config["ioOn_id"][output_number - 1]
        self.io_command_id = self._config["ioOn_id"][output_number - 1]
        self.ana_state_id = self._config["anaPosition_id"][output_number - 1]
        self.ana_command_id = self._config["anaCommand_id"][output_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current X-Dimmer status."""
        return await self._ipx.get_io(self.io_state_id)

    @property
    async def level(self) -> int:
        """Return the current X-Dimmer level."""
        return int(await self._ipx.get_ana(self.ana_state_id))

    async def on(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-Dimmer."""
        await self._ipx.update_io(self.io_command_id, True)

    async def off(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-Dimmer."""
        await self._ipx.update_io(self.io_command_id, False)

    async def toggle(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-Dimmer."""
        await self._ipx.update_io(self.io_command_id, True, "toggle")

    async def set_level(self, level: int, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-Dimmer on a specific level."""
        if not 0 <= level <= 100:
            raise ValueError("Level must be between 0 and 100")
        await self._ipx.update_ana(self.ana_command_id, level)
