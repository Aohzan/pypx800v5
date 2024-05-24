"""IPX800V5 X-PWM."""

from .const import DEFAULT_TRANSITION
from .const import EXT_XPWM as ext_type
from .extension import Extension
from .ipx800 import IPX800

VALUE_ON = 100
VALUE_OFF = 0


class XPWM(Extension):
    """Represent a X-PWM output channel."""

    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number, output_number)
        self.ana_state_id = self._config["anaCommand_id"][output_number - 1]
        self.ana_command_id = self._config["anaCommand_id"][output_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current X-PWM status."""
        return await self._ipx.get_ana(self.ana_state_id) > 0

    @property
    async def level(self) -> int:
        """Return the current X-PWM level."""
        return int(await self._ipx.get_ana(self.ana_state_id))

    async def on(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM."""
        await self._ipx.update_ana(self.ana_command_id, VALUE_ON)

    async def off(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-PWM."""
        await self._ipx.update_ana(self.ana_command_id, VALUE_OFF)

    async def toggle(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-PWM."""
        if self.status:
            await self._ipx.update_ana(self.ana_command_id, VALUE_OFF)
        else:
            await self._ipx.update_ana(self.ana_command_id, VALUE_ON)

    async def set_level(self, level: int, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM on a specific level."""
        if not 0 <= level <= 100:
            raise ValueError("Level must be between 0 and 100")
        await self._ipx.update_ana(self.ana_command_id, level)
