"""IPX800V5 X-4VR."""
from .const import DEFAULT_TRANSITION, EXT_X4VR, TYPE_ANA, TYPE_IO
from .extension import Extension
from .ipx800 import IPX800


class X4VR(Extension):
    def __init__(self, ipx: IPX800, ext_number: int, output_number: int):
        super().__init__(ipx, EXT_X4VR, ext_number, output_number)
        self._mode = self._config["mode"]

        self.ana_position_id = self._config["anaPosition_id"][output_number - 1]
        self.ana_command_id = self._config["anaCommand_id"][output_number - 1]
        self.io_command_up_id = self._config["ioCommandUp_id"][output_number - 1]
        self.io_command_down_id = self._config["ioCommandDown_id"][output_number - 1]
        self.io_command_stop_id = self._config["ioCommandStop_id"][output_number - 1]
        self.io_command_bso_up_id = self._config["ioCommandBsoUp_id"][output_number - 1]
        self.io_command_bso_down_id = self._config["ioCommandBsoDown_id"][
            output_number - 1
        ]

    @property
    async def status(self) -> bool:
        """Return the current cover status."""
        return await self._ipx.get_ana(self.ana_position_id) < 100

    @property
    async def level(self) -> int:
        """Return the current cover level."""
        return 100 - int(await self._ipx.get_ana(self.ana_position_id))

    async def open(self) -> None:
        """Open cover."""
        await self._ipx.update_io(self.io_command_up_id, True)

    async def close(self) -> None:
        """Close cover."""
        await self._ipx.update_io(self.io_command_down_id, True)

    async def stop(self) -> None:
        """Stop cover."""
        await self._ipx.update_io(self.io_command_stop_id, True)

    async def set_level(self, level: int) -> None:
        """Set cover level."""
        await self._ipx.update_ana(self.ana_command_id, 100 - level)

    async def open_bso(self) -> None:
        """Set cover impulse down."""
        await self._ipx.update_io(self.io_command_bso_up_id, True)

    async def close_bso(self) -> None:
        """Set cover impulse up."""
        await self._ipx.update_io(self.io_command_bso_down_id, True)
