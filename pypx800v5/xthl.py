"""IPX800V5 X-THL."""

from .const import EXT_XTHL as ext_type
from .extension import Extension
from .ipx800 import IPX800


class XTHL(Extension):
    """Representing an X-THL extension."""

    def __init__(self, ipx: IPX800, ext_number: int):
        """Init the extension."""
        super().__init__(ipx, ext_type, ext_number)
        self._api_path = f"ebx/xthl/{self._ext_id}"
        self.temp_key = "anaTemp"
        self.hum_key = "anaHum"
        self.lum_key = "anaLum"
        self.temp_state_id = self._config["anaTemp_id"]
        self.hum_state_id = self._config["anaHum_id"]
        self.lum_state_id = self._config["anaLum_id"]

    @property
    async def temperature(self) -> float:
        """Get temperature of the X-THL."""
        response = await self._ipx._request_api(self._api_path)
        return float(response[self.temp_key])

    @property
    async def humidity(self) -> float:
        """Get humidity level of the X-THL."""
        response = await self._ipx._request_api(self._api_path)
        return float(response[self.hum_key])

    @property
    async def luminosity(self) -> int:
        """Get luminosity level of the X-THL."""
        response = await self._ipx._request_api(self._api_path)
        return int(response[self.lum_key])
