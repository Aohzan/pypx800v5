"""IPX800V5 Access Control."""

from .const import OBJECT_ACCESS_CONTROL as obj_type
from .ipx800 import IPX800
from .object import Object


class AccessControl(Object):
    """Represent an IPX800 access control object."""

    def __init__(self, ipx: IPX800, obj_number: int):
        """Init the object."""
        super().__init__(ipx, obj_type, obj_number)
        self.io_out_id = self._config["ioOut_id"]
        self.io_fault_id = self._config["ioFault_id"]
        self.str_last_code_id = self._config["bindCurrentCode_id"]
        self.str_codes_ids = self._config["strPoolCode_id"]

    @property
    async def success(self) -> bool:
        """Return if Access Control has a success input code."""
        return await self._ipx.get_io(self.io_out_id)

    @property
    async def fault(self) -> bool:
        """Return if Access Control has a fault input code."""
        return await self._ipx.get_io(self.io_fault_id)

    @property
    async def last_code(self) -> str:
        """Return the last code entered."""
        return await self._ipx.get_str(self.str_last_code_id)

    @property
    async def codes(self) -> list:
        """Return the list of accepted codes."""
        codes = []
        for code_id in self.str_codes_ids:
            codes.append(await self._ipx.get_str(code_id))
        return codes
