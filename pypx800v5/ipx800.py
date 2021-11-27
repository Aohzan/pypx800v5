"""Get information and control a GCE IPX800v5."""
import asyncio
import socket

import aiohttp
import async_timeout

from .const import *
from .exceptions import (
    Ipx800CannotConnectError,
    Ipx800InvalidAuthError,
    Ipx800RequestError,
)


class IPX800:
    """Class representing the IPX800 and its API."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 80,
        request_timeout: int = 5,
        session: aiohttp.client.ClientSession = None,
    ) -> None:
        """Init a IPX800 V5 API."""
        self.host = host
        self.port = port
        self._api_key = api_key
        self._request_timeout = request_timeout
        self._base_api_url = f"http://{host}:{port}/api/"

        self._api_version = ""
        self._ipx_config = {}
        self._extensions_config = []

        self._session = session
        self._close_session = False

        if self._session is None:
            self._session = aiohttp.ClientSession()
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
    def extensions_config(self) -> dict:
        """Get the config of connected extensions."""
        return self._extensions_config

    async def _request_api(
        self, path, data: dict = None, params: dict = None, method: str = "GET"
    ) -> dict:
        """Make a request to get the IPX800 JSON API."""
        params_with_api = {"ApiKey": self._api_key}
        if params is not None:
            params_with_api.update(params)

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.request(
                    method=method,
                    url=self._base_api_url + path,
                    params=params_with_api,
                    json=data,
                )

            if response.status == 401:
                raise Ipx800InvalidAuthError()

            if response.status >= 200 and response.status <= 206:
                content = await response.json()
                response.close()
                return content

            content = await response.json()
            raise Ipx800RequestError(
                "IPX800 API request error, error code", response.status
            )

        except asyncio.TimeoutError as exception:
            raise Ipx800CannotConnectError(
                "Timeout occurred while connecting to IPX800."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Ipx800CannotConnectError(
                "Error occurred while communicating with the IPX800."
            ) from exception

    async def ping(self) -> bool:
        """Return True if the IPX800 answer to API request."""
        try:
            result = await self._request_api("system/ipx")
            return result.get("errorStatus") == 0
        except Ipx800CannotConnectError:
            pass
        return False

    async def init_config(self) -> bool:
        """Init the full config of the IPX."""
        print("Init the IPX800V5 configuration.")
        await self.get_ipx_info()
        await self.get_ipx_config()
        await self.get_extensions_config()

    async def get_ipx_info(self) -> dict:
        """Get IPX config."""
        infos = await self._request_api("system/ipx/info")
        self._api_version = infos["apiVersion"]
        # TODO More properties
        return infos

    async def get_ipx_config(self) -> dict:
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
                            EXT_CONFIG_TYPE: type_extension,
                            EXT_CONFIG_ID: extension["_id"],
                            EXT_CONFIG_NAME: extension["name"],
                            EXT_CONFIG_PARAMS: extension,
                        }
                    )
            except Ipx800RequestError:
                print("Error to get %s extensions" % type_extension)
        self._extensions_config = extensions_config

    async def global_get(self) -> dict:
        """Get all values from the IPX800 API."""
        values = await self._request_api("core/io")
        values.update(self._request_api("core/ana"))
        return values

    def get_ext_id(self, ext_type, ext_number) -> str:
        """Return the unique extension id generated by the IPX."""
        extensions = [
            x for x in self.extensions_config if x["type"] == ext_type]
        return extensions[ext_number - 1]["id"]
        # TODO Raise error if extension not existing ? or return empty str

    def get_output_id(
        self, ext_type, ext_number, output_type, output_number=None
    ) -> str:
        """Return the unique id of output."""
        id_key = (
            MAPPING_IO_OUTPUT_ID[ext_type]
            if output_type == TYPE_IO
            else MAPPING_ANA_OUTPUT_ID[ext_type]
        )
        if ext_type == IPX:
            return self._ipx_config[id_key][output_number - 1]
        extensions = [
            x for x in self.extensions_config if x["type"] == ext_type]
        if output_number is None:
            return extensions[ext_number - 1][EXT_CONFIG_PARAMS][id_key]
        return extensions[ext_number - 1][EXT_CONFIG_PARAMS][id_key][output_number - 1]

    def get_input_id(
        self, ext_type, ext_number, output_type, output_number=None
    ) -> str:
        """Return the unique id of output."""
        id_key = (
            MAPPING_IO_INPUT_ID[ext_type]
            if output_type == TYPE_IO
            else MAPPING_ANA_INPUT_ID[ext_type]
        )
        if ext_type == IPX:
            return self._ipx_config[id_key][output_number - 1]
        extensions = [
            x for x in self.extensions_config if x["type"] == ext_type]
        if output_number is None:
            return extensions[ext_number - 1][EXT_CONFIG_PARAMS][id_key]
        return extensions[ext_number - 1][EXT_CONFIG_PARAMS][id_key][output_number - 1]

    def get_xthl_ids(
            self, ext_number) -> list:
        """Return the unique id of X-THL inputs in temp,hum,lum order."""
        extensions = [
            x for x in self.extensions_config if x["type"] == EXT_XTHL]
        params = extensions[ext_number - 1][EXT_CONFIG_PARAMS]
        return [params["anaTemp_id"], params["anaHum_id"], params["anaLum_id"]]

    def get_command_id(
        self, ext_type, ext_number, command_type, command_number=None
    ) -> str:
        """Return the unique id of command."""
        id_key = (
            MAPPING_IO_COMMAND_ID[ext_type]
            if command_type == TYPE_IO
            else MAPPING_ANA_COMMAND_ID[ext_type]
        )
        if ext_type == IPX:
            return self._ipx_config[id_key][command_number - 1]
        extensions = [
            x for x in self.extensions_config if x["type"] == ext_type]
        if command_number is None:
            return extensions[ext_number - 1][EXT_CONFIG_PARAMS][id_key]
        return extensions[ext_number - 1][EXT_CONFIG_PARAMS][id_key][command_number - 1]

    async def get_io(self, id: int) -> bool:
        """Get IO status on the IPX."""
        response = await self._request_api(f"core/io/{id}")
        return response["on"]

    async def get_ana(self, id: int) -> None:
        """Get an Analog status on the IPX."""
        response = await self._request_api(f"core/ana/{id}")
        return response["value"]

    async def update_io(self, id: int, value: bool, command: str = "on") -> None:
        """Update an IO on the IPX."""
        await self._request_api(f"core/io/{id}", method="PUT", data={command: value})

    async def update_ana(self, id: int, value: int) -> None:
        """Update an Analog on the IPX."""
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
