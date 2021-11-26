"""IPX800V5 Base Extension."""
from pypx800v5.const import IPX

from .ipx800 import IPX800


class Extension:
    def __init__(
        self, ipx: IPX800, ext_type: str, ext_number: int, io_number: int = None
    ):
        self._ipx = ipx
        self._ext_type = ext_type
        self._ext_number = ext_number
        self._ext_id = (
            ipx.get_ext_id(ext_type, ext_number) if ext_type is not IPX else None
        )
        self._io_number = io_number

    #     self._command_id = None
    #     self._state_id = None

    # @property
    # def state_id(self) -> str:
    #     return self._state_id

    # @property
    # def command_id(self) -> str:
    #     return self._command_id
