"""IPX800V5 X-400."""

from .const import EXT_X400 as ext_type
from .const import X400_FUNC_CT
from .extension import Extension
from .ipx800 import IPX800


class X400(Extension):
    """Represent a X-400 input, connected through a X-Bridge.

    The X-400 function is set on the IPX800: X-400 CT for current clamps
    or X-400 Ana for analog sensors.
    """

    def __init__(self, ipx: IPX800, ext_number: int, input_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number, input_number)
        self.function = self._config["func"]
        self.ana_value_id = self._config["anaOutputVal_id"][input_number - 1]

    @property
    def is_current_clamp(self) -> bool:
        """Return True if the X-400 measures currents (X-400 CT)."""
        return self.function == X400_FUNC_CT

    @property
    async def value(self) -> float:
        """Return the current in amperes (X-400 CT) or the ADC value (X-400 Ana)."""
        return float(await self._ipx.get_ana(self.ana_value_id))
