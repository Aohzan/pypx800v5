"""IPX800V5 X-8R."""
from .extension import Extension
from .const import VALUE_OFF, VALUE_ON, VALUE_TOGGLE
from .ipx800 import IPX800

API_PATH = "ebx/x8r"
EXT_TYPE = "x8r"

KEY_STATUS_ONOFF = "ioOutputState"
KEY_SET_ONOFF = "ioOutput"


class X8R(Extension):
    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        super().__init__(ipx, EXT_TYPE, ext_number, output_number)

    @property
    async def status(self) -> bool:
        """Return the current X-8R status."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_STATUS_ONOFF][self._output_number - 1] == "on"

    async def _update_request(self, key, value) -> None:
        """Make an request to update state of a X-8R output."""
        current_state = await self._ipx._request_api(API_PATH)
        data = {
            key: current_state[self._ext_number - 1][key],
        }
        data[key][self._output_number - 1] = value
        await self._ipx._request_api(f"{API_PATH}/{self._ext_id}", data=data, method="PUT")

    async def on(self) -> None:
        """Turn on a X-8R."""
        await self._update_request(KEY_SET_ONOFF, VALUE_ON)

    async def off(self) -> None:
        """Turn off a X-8R."""
        await self._update_request(KEY_SET_ONOFF, VALUE_OFF)

    async def toggle(self) -> None:
        """Toggle a X-8R."""
        await self._update_request(KEY_SET_ONOFF, VALUE_TOGGLE)
