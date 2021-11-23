"""IPX800V5 X-THL."""
from .extension import Extension
from .ipx800 import IPX800

API_PATH = "ebx/xthl"
EXT_TYPE = "xthl"

KEY_TEMP = "anaTemp"
KEY_HUM = "anaHum"
KEY_LUM = "anaLum"


class XTHL(Extension):
    """Representing an X-THL extension."""

    def __init__(self, ipx: IPX800, ext_number: int):
        super().__init__(ipx, EXT_TYPE, ext_number)

    @property
    async def temp(self) -> float:
        """Get temperature of the X-THL."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_TEMP]

    @property
    async def hum(self) -> float:
        """Get humidity level of the X-THL."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_HUM]

    @property
    async def lum(self) -> int:
        """Get luminosity level of the X-THL."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_LUM]
