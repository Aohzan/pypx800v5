"""IPX800V5 Base Object."""
from pypx800v5.const import API_CONFIG_ID

from .ipx800 import IPX800


class Object:
    def __init__(self, ipx: IPX800, obj_type: str, obj_number: int):
        self._ipx = ipx
        self._obj_type = obj_type
        self._obj_number = obj_number
        self._config = ipx.get_obj_config(obj_type, obj_number)
        self._obj_id = self._config[API_CONFIG_ID]
