"""IPX800V5 X-THL."""
from .extension import Extension
from .ipx800 import IPX800

API_PATH = "ebx/xthl"
EXT_TYPE = "xthl"


class XTHL(Extension):
    """Representing an X-THL extension."""

    def __init__(self, ipx: IPX800, ext_number: int):
        super().__init__(ipx, EXT_TYPE, ext_number)
        self._api_path = f"{API_PATH}/{self._ext_id}"
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
