"""IPX800V5 X-PWM."""
from .extension import Extension
from .const import DEFAULT_TRANSITION, VALUE_ON
from .ipx800 import IPX800

API_PATH = "ebx/xpwm"
EXT_TYPE = "xpwm"

KEY_STATUS_ONOFF = "anaCommand"
KEY_SET_ONOFF = "anaCommand"
KEY_STATUS_LEVEL = "anaCommand"
KEY_SET_LEVEL = "anaCommand"
KEY_SET_TRANSITION = "anaSpeedTransition"

VALUE_ON = 100
VALUE_OFF = 0


class XPWM(Extension):
    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        super().__init__(ipx, EXT_TYPE, ext_number, output_number)

    @property
    async def status(self) -> bool:
        """Return the current X-PWM status."""
        response = await self._ipx._request_api(API_PATH)
        return response[self._ext_number - 1][KEY_STATUS_ONOFF][self._output_number - 1] > 0

    @property
    async def level(self) -> int:
        """Return the current X-PWM level."""
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
        """Turn on a X-PWM."""
        await self._update_request(KEY_SET_ONOFF, VALUE_ON, transition)

    async def off(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn off a X-PWM."""
        await self._update_request(KEY_SET_ONOFF, VALUE_OFF, transition)

    async def toggle(self, transition: int = DEFAULT_TRANSITION) -> None:
        """Toggle a X-PWM."""
        if self.status:
            await self._update_request(KEY_SET_ONOFF, VALUE_OFF, transition)
        else:
            await self._update_request(KEY_SET_ONOFF, VALUE_ON, transition)

    async def set_level(self, level: int, transition: int = DEFAULT_TRANSITION) -> None:
        """Turn on a X-PWM on a specific level."""
        await self._update_request(KEY_SET_LEVEL, level, transition, key_state=KEY_STATUS_LEVEL)
