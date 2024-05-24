"""IPX800V5 X-4FP."""

from enum import Enum

from .const import EXT_X4FP as ext_type
from .extension import Extension
from .ipx800 import IPX800


class X4FPMode(Enum):
    """Preset modes of a X-4FP."""

    COMFORT = "Comfort"
    COMFORT_1 = "Comfort_1"
    COMFORT_2 = "Comfort_2"
    ECO = "Eco"
    ANTIFREEZE = "AntiFreeze"
    STOP = "Stop"


class X4FP(Extension):
    """Represent a X-4FP zone."""

    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number, output_number)
        self.io_comfort_id = self._config["ioComfort_id"][output_number - 1]
        self.io_eco_id = self._config["ioEco_id"][output_number - 1]
        self.io_anti_freeze_id = self._config["ioAntiFreeze_id"][output_number - 1]
        self.io_stop_id = self._config["ioStop_id"][output_number - 1]
        self.io_comfort_1_id = self._config["ioComfort_1_id"][output_number - 1]
        self.io_comfort_2_id = self._config["ioComfort_2_id"][output_number - 1]

    async def mode(self) -> X4FPMode:
        """Return the current mode enabled, you can pass current states if you have them, otherwyse it will request it."""
        states = await self._ipx.get_ext_states(ext_type, self._ext_id)
        for mode in X4FPMode:
            if states[f"io{mode.value}"][self._io_number - 1]["on"] is True:  # type: ignore
                return mode
        return None  # type: ignore

    async def set_mode(self, mode: X4FPMode) -> None:
        """Set comfort mode."""
        await self._ipx.update_io(
            self._config[f"io{mode.value}_id"][self._io_number - 1],  # type: ignore
            True,
        )
