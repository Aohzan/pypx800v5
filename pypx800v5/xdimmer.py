"""IPX800V5 X-Dimmer."""
from .extension import Extension
from .const import DEFAULT_TRANSITION, VALUE_OFF, VALUE_ON, VALUE_TOGGLE
from .ipx800 import IPX800

API_PATH = "ebx/xdimmer"
EXT_TYPE = "xdimmer"

KEY_STATUS_ONOFF = "ioOn"
KEY_SET_ONOFF = "ioOn"
KEY_STATUS_LEVEL = "anaPosition"
KEY_SET_LEVEL = "anaCommand"
KEY_SET_TRANSITION = "anaSpeedTransition"


class XDimmer(Extension):
    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        super().__init__(ipx, EXT_TYPE, ext_number, output_number)

    @property
    async def status(self) -> bool:
        """Return the current X-Dimmer status."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_STATUS_ONOFF][self._output_number - 1] == "on"

    @property
    async def level(self) -> int:
        """Return the current X-Dimmer level."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_STATUS_LEVEL][self._output_number - 1]

    async def _update_request(self, key, value, transition, key_state=None) -> None:
        """Make an request to update state of a XDimmer output."""
        current_state = await self._ipx._request_api(API_PATH)
        data = {
            key: current_state[self._ext_number - 1][key_state if key_state else key],
            KEY_SET_TRANSITION: transition
        }
        data[key][self._output_number - 1] = value
        await self._ipx._request_api(f"{API_PATH}/{self._ext_id}", data=data, method="PUT")

    async def on(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-Dimmer."""
        await self._update_request(KEY_SET_ONOFF, VALUE_ON, transition)

    async def off(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-Dimmer."""
        await self._update_request(KEY_SET_ONOFF, VALUE_OFF, transition)

    async def toggle(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-Dimmer."""
        await self._update_request(KEY_SET_ONOFF, VALUE_TOGGLE, transition)

    async def set_level(self, level: int, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-Dimmer on a specific level."""
        await self._update_request(KEY_SET_LEVEL, level, transition, key_state=KEY_STATUS_LEVEL)
