"""IPX800V5 Base Extension."""
from .ipx800 import IPX800


class Extension():
    def __init__(self, ipx: IPX800, ext_type: str, ext_number: int, output_number: int):
        self._ipx = ipx
        self._ext_type = ext_type
        self._ext_number = ext_number
        self._ext_id = ipx.get_ext_id(ext_type, ext_number)
        self._output_number = output_number
