"""Get information and control a GCE IPX800v5."""
from asyncio import TimeoutError
from socket import gaierror

from aiohttp import ClientError, ClientSession
from async_timeout import timeout

from .const import *
from .exceptions import (
    IPX800CannotConnectError,
    IPX800InvalidAuthError,
    IPX800RequestError,
)


class IPX800:
    """Class representing the IPX800 and its API."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 80,
        request_timeout: int = 5,
        session: ClientSession = None,
    ) -> None:
        """Init a IPX800 V5 API."""
        self.host = host
        self.port = port
        self._api_key = api_key
        self._request_timeout = request_timeout
        self._base_api_url = f"http://{host}:{port}/api/"

        self._api_version = ""
        self._ipx_config = {}  # type: dict
        self._extensions_config = []  # type: list
        self._objects_config = []  # type: list

        self._session = session
        self._close_session = False

        if self._session is None:
            self._session = ClientSession()
            self._close_session = True

    @property
    def api_version(self) -> str:
        """Return the API version."""
        return self._api_version

    @property
    def ipx_config(self) -> dict:
        """Get the config of the IPX."""
        return self._ipx_config

    @property
    def extensions_config(self) -> list:
        """Get the config of connected extensions."""
        return self._extensions_config

    @property
    def objects_config(self) -> list:
        """Get the config of connected extensions."""
        return self._objects_config

    async def _request_api(
        self, path, data: dict = None, params: dict = None, method: str = "GET"
    ) -> dict:
        """Make a request to get the IPX800 JSON API."""
        params_with_api = {"ApiKey": self._api_key}
        if params is not None:
            params_with_api.update(params)

        try:
            with timeout(self._request_timeout):
                response = await self._session.request(  # type: ignore
                    method=method,
                    url=self._base_api_url + path,
                    params=params_with_api,
                    json=data,
                )

            if response.status == 401:
                raise IPX800InvalidAuthError()

            if response.status >= 200 and response.status <= 206:
                content = await response.json()
                response.close()
                return content

            content = await response.json()
            raise IPX800RequestError(
                "IPX800 API request error %s: %s", response.status, content
            )

        except TimeoutError as exception:
            raise IPX800CannotConnectError(
                "Timeout occurred while connecting to IPX800."
            ) from exception
        except (ClientError, gaierror) as exception:
            raise IPX800CannotConnectError(
                "Error occurred while communicating with the IPX800."
            ) from exception

    async def ping(self) -> bool:
        """Return True if the IPX800 answer to API request."""
        try:
            result = await self._request_api("system/ipx")
            return result.get("errorStatus") == 0
        except IPX800CannotConnectError:
            pass
        return False

    async def init_config(self) -> bool:
        """Init the full config of the IPX."""
        print("Init the IPX800V5 configuration.")
        await self.get_ipx_info()
        await self.get_ipx_config()
        await self.get_extensions_config()
        await self.get_objects_config()
        return True

    async def get_ipx_info(self) -> dict:
        """Get IPX config."""
        infos = await self._request_api("system/ipx/info")
        self._api_version = infos["apiVersion"]
        # TODO More properties
        return infos

    async def global_get(self) -> dict:
        """Get all values from the IPX800 API."""
        values = {x["_id"]: x for x in await self._request_api("core/io")}
        values.update({x["_id"]: x for x in await self._request_api("core/ana")})
        return values

    # Get configs from PX API
    async def get_ipx_config(self) -> None:
        """Get IPX config."""
        self._ipx_config = await self._request_api(
            "system/ipx", params={"option": "filter_id"}
        )

    async def get_extensions_config(self) -> None:
        """Update the list of connected extensions."""
        extensions_config = []
        for type_extension in EXTENSIONS:
            try:
                for extension in await self._request_api(
                    f"ebx/{type_extension}", params={"option": "filter_id"}
                ):
                    extensions_config.append(
                        {
                            API_CONFIG_TYPE: type_extension,
                            API_CONFIG_ID: extension["_id"],
                            API_CONFIG_NAME: extension["name"],
                            API_CONFIG_PARAMS: extension,
                        }
                    )
            except IPX800RequestError:
                print("Error to get %s extensions" % type_extension)
        self._extensions_config = extensions_config

    async def get_objects_config(self) -> None:
        """Update the list of configured objects."""
        objects_config = []
        for type_object in OBJECTS:
            try:
                for extension in await self._request_api(
                    f"object/{type_object}", params={"option": "filter_id"}
                ):
                    objects_config.append(
                        {
                            API_CONFIG_TYPE: type_object,
                            API_CONFIG_ID: extension["_id"],
                            API_CONFIG_NAME: extension["name"],
                            API_CONFIG_PARAMS: extension,
                        }
                    )
            except IPX800RequestError:
                print("Error to get %s object" % type_object)
        self._objects_config = objects_config

    # Get ext or obj configs
    def get_ext_config(self, ext_type: str, ext_number: int) -> dict:
        """Return the extension config."""
        extensions = [
            x for x in self.extensions_config if x[API_CONFIG_TYPE] == ext_type
        ]
        return extensions[ext_number - 1][API_CONFIG_PARAMS]

    def get_ext_id(self, ext_type: str, ext_number: int) -> int:
        """Return the unique extension id generated by the IPX."""
        extensions = [
            x for x in self.extensions_config if x[API_CONFIG_TYPE] == ext_type
        ]
        return extensions[ext_number - 1][API_CONFIG_ID]

    async def get_ext_states(self, ext_type: str, ext_id: int) -> dict:
        """Return all values of extension."""
        return await self._request_api(f"core/{ext_type}/{ext_id}")

    def get_obj_config(self, obj_type: str, obj_number: int) -> dict:
        """Return the extension config."""
        extensions = [x for x in self.objects_config if x[API_CONFIG_TYPE] == obj_type]
        return extensions[obj_number - 1][API_CONFIG_PARAMS]

    def get_obj_id(self, obj_type: str, obj_number: int) -> str:
        """Return the unique object id generated by the IPX."""
        objs = [x for x in self.objects_config if x[API_CONFIG_TYPE] == obj_type]
        return objs[obj_number - 1][API_CONFIG_ID]

    # Get/Update commands

    async def get_io(self, id: int) -> bool:
        """Get IO status on the IPX."""
        response = await self._request_api(f"core/io/{id}")
        return response["on"]

    async def get_ana(self, id: int) -> float:
        """Get an Analog status on the IPX."""
        response = await self._request_api(f"core/ana/{id}")
        return response["value"]

    async def update_io(self, id: int, value: bool, command: str = "on") -> None:
        """Update an IO on the IPX."""
        await self._request_api(f"core/io/{id}", method="PUT", data={command: value})

    async def update_ana(self, id: int, value) -> None:
        """Update an Analog on the IPX."""
        if type(value) not in [int, float]:
            raise IPX800RequestError("Ana value need to be a int or a float type.")
        await self._request_api(f"core/ana/{id}", method="PUT", data={"value": value})

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit."""
        await self.close()
