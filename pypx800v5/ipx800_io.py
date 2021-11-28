"""IPX800V5 control."""
from .const import IPX, TYPE_ANA, TYPE_IO
from .extension import Extension
from .ipx800 import IPX800


class IPX800IO():
    def __init__(
        self, ipx: IPX800, io_number: int = None
    ):
        self._ipx = ipx
        self._config = ipx.ipx_config
        self._io_number = io_number


class IPX800Relay(IPX800IO):
    def __init__(self, ipx: IPX800, output_number: int):
        super().__init__(ipx, output_number)
        self.io_state_id = self._config["ioRelayState_id"][output_number - 1]
        self.io_command_id = self._config["ioRelays_id"][output_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current IPX800 relay status."""
        return await self._ipx.get_io(self.io_state_id)

    async def on(self) -> None:
        """Turn on a IPX800 relay."""
        await self._ipx.update_io(self.io_command_id, True)

    async def off(self) -> None:
        """Turn off a IPX800 relay."""
        await self._ipx.update_io(self.io_command_id, False)

    async def toggle(self) -> None:
        """Toggle a IPX800 relay."""
        await self._ipx.update_io(self.io_command_id, True, "toggle")


class IPX800DigitalInput(IPX800IO):
    def __init__(self, ipx: IPX800, input_number: int):
        super().__init__(ipx, input_number)
        self.io_state_id = self._config["ioDInput_id"][input_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current IPX800 digital input status."""
        return await self._ipx.get_io(self.io_state_id)


class IPX800AnalogInput(IPX800IO):
    def __init__(self, ipx: IPX800, input_number: int):
        super().__init__(ipx, input_number)
        self.ana_state_id = self._config["ana_IPX_Input"][input_number - 1]

    @property
    async def status(self) -> float:
        """Return the current IPX800 analog input status."""
        return await self._ipx.get_ana(self.ana_state_id)
