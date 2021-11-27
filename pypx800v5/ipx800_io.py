"""IPX800V5 control."""
from .const import IPX, TYPE_ANA, TYPE_IO
from .extension import Extension
from .ipx800 import IPX800


class IPX800Relay(Extension):
    def __init__(self, ipx: IPX800, output_number: int):
        super().__init__(ipx, IPX, 0, output_number)
        self.io_state_id = ipx.get_output_id(IPX, 0, TYPE_IO, output_number)
        self.io_command_id = ipx.get_command_id(IPX, 0, TYPE_IO, output_number)

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


class IPX800DigitalInput(Extension):
    def __init__(self, ipx: IPX800, input_number: int):
        super().__init__(ipx, IPX, 0, input_number)
        self.io_state_id = ipx.get_input_id(IPX, 0, TYPE_IO, input_number)

    @property
    async def status(self) -> bool:
        """Return the current IPX800 digital input status."""
        return await self._ipx.get_io(self.io_state_id)


class IPX800AnalogInput(Extension):
    def __init__(self, ipx: IPX800, input_number: int):
        super().__init__(ipx, IPX, 0, input_number)
        self.ana_state_id = ipx.get_input_id(IPX, 0, TYPE_ANA, input_number)

    @property
    async def status(self) -> bool:
        """Return the current IPX800 analog input status."""
        return await self._ipx.get_ana(self.ana_state_id)
