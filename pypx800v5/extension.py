"""IPX800V5 Base Extension."""

from .ipx800 import IPX800


class Extension:
    """Represent a IPX800's base extension."""

    def __init__(
        self, ipx: IPX800, ext_type: str, ext_number: int, io_number: int | None = None
    ):
        """Init the ipx base extension."""
        self._ipx = ipx
        self._ext_type = ext_type
        self._ext_number = ext_number
        self._name = ipx.get_ext_name(ext_type, ext_number)
        self._config = ipx.get_ext_config(ext_type, ext_number)
        self._ext_id = ipx.get_ext_id(ext_type, ext_number)
        self._io_number = io_number

    @property
    def name(self) -> str:
        """Return the name set in the config."""
        return self._name
