"""IPX800V5 control."""

from .ipx800 import IPX800


class IPX800IO:
    """Represent the IPX800 base io."""

    def __init__(self, ipx: IPX800, io_number: int | None = None):
        """Init the ipx base io."""
        self._ipx = ipx
        self._config = ipx.ipx_config
        self._io_number = io_number


class IPX800Relay(IPX800IO):
    """Represent an IPX800 relay."""

    def __init__(self, ipx: IPX800, output_number: int):
        """Init the ipx io."""
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


class IPX800OpenColl(IPX800IO):
    """Represent an IPX800 Open Collector relay."""

    def __init__(self, ipx: IPX800, output_number: int):
        """Init the ipx io."""
        super().__init__(ipx, output_number)
        self.io_state_id = self._config["ioCollOutputState_id"][output_number - 1]
        self.io_command_id = self._config["ioCollOutput_id"][output_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current IPX800 open collector status."""
        return await self._ipx.get_io(self.io_state_id)

    async def on(self) -> None:
        """Turn on a IPX800 open collector."""
        await self._ipx.update_io(self.io_command_id, True)

    async def off(self) -> None:
        """Turn off a IPX800 open collector."""
        await self._ipx.update_io(self.io_command_id, False)

    async def toggle(self) -> None:
        """Toggle a IPX800 open collector."""
        await self._ipx.update_io(self.io_command_id, True, "toggle")


class IPX800DigitalInput(IPX800IO):
    """Represent an IPX800 digital input."""

    def __init__(self, ipx: IPX800, input_number: int):
        """Init the ipx io."""
        super().__init__(ipx, input_number)
        self.io_state_id = self._config["ioDInput_id"][input_number - 1]

    @property
    async def status(self) -> bool:
        """Return the current IPX800 digital input status."""
        return await self._ipx.get_io(self.io_state_id)


class IPX800AnalogInput(IPX800IO):
    """Represent an IPX800 analog input."""

    def __init__(self, ipx: IPX800, input_number: int):
        """Init the ipx io."""
        super().__init__(ipx, input_number)
        self.ana_state_id = self._config["ana_IPX_Input"][input_number - 1]

    @property
    async def status(self) -> float:
        """Return the current IPX800 analog input status."""
        return await self._ipx.get_ana(self.ana_state_id)


class IPX800OptoInput(IPX800IO):
    """Represent an IPX800 Opto input."""

    def __init__(self, ipx: IPX800, input_number: int):
        """Init the ipx io."""
        super().__init__(ipx, input_number)
        self.io_state_id = self._config["ioCollInput_id"][input_number - 1]

    @property
    async def status(self) -> float:
        """Return the current IPX800 opto input status."""
        return await self._ipx.get_io(self.io_state_id)
