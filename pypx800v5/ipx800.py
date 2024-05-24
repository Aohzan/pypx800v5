"""Get information and control a GCE IPX800v5."""

from asyncio import TimeoutError
from socket import gaierror
from time import sleep

from aiohttp import ClientError, ClientSession
from async_timeout import timeout

from pypx800v5.const import (
    API_CONFIG_ID,
    API_CONFIG_NAME,
    API_CONFIG_PARAMS,
    API_CONFIG_TYPE,
    EXTENSIONS,
    OBJECT_TEMPO,
    OBJECT_TIMER,
    OBJECTS,
)

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
        request_timeout: int = 30,
        request_retries_count: int = 5,
        request_retries_delay: float = 0.5,
        session: ClientSession | None = None,
    ) -> None:
        """Init a IPX800 V5 API."""
        self.host = host
        self.port = port
        self._api_key = api_key
        self._request_timeout = request_timeout
        self._request_retries_count = request_retries_count
        self._request_retries_delay = request_retries_delay
        self._base_api_url = f"http://{host}:{port}/api/"

        self._firmware_version = None
        self._mac_address = None

        self.io_acpower_id = "ioDetectionAC_id"
        self.ana_ipx_charge_period_id = "anaIPXChargePeriod_id"
        self.ana_ipx_charge_app_id = "anaIPXChargeApp_id"
        self.ana_ipx_charge_rules_id = "anaIPXChargeRules_id"
        self.ana_ipx_charge_ebx_id = "anaIPXChargeEbx_id"
        self.ana_ipx_charge_bsp_id = "anaIPXChargeBsp_id"
        self.ana_ipx_cycle_period_id = "anaIPXCyclePeriod_id"
        self.ana_ipx_cycle_app_id = "anaIPXCycleApp_id"
        self.ana_ipx_cycle_rules_id = "anaIPXCycleRules_id"
        self.ana_ipx_cycle_ebx_id = "anaIPXCycleEBX_id"
        self.ana_heap_free_id = "anaHeapFree_id"
        self.ana_delta_heap_free_id = "anaDeltaHeapFree_id"
        self.ana_monitor_connections_id = "anaMonitorConnections_id"
        self.ana_ipx_clock_id = "anaIPXClock_id"

        self._ipx_config = {}  # type: dict
        self._extensions_config = []  # type: list
        self._objects_config = []  # type: list

        self._session = session
        self._close_session = False

        if self._session is None:
            self._session = ClientSession()
            self._close_session = True

    @property
    def firmware_version(self):
        """Return the firmware version."""
        return self._firmware_version

    @property
    def mac_address(self):
        """Return the MAC Address version."""
        return self._mac_address

    @property
    async def ac_power(self) -> bool:
        """Return if AC Power detected on the X-PSU, None if no X-PSU connected."""
        response = await self._request_api("system/ipx")
        return response.get(self.io_acpower_id) is True

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
        self,
        path,
        data: dict | None = None,
        params: dict | None = None,
        method: str = "GET",
    ) -> dict:
        """Make a request to get the IPX800 JSON API."""
        params_with_api = {"ApiKey": self._api_key}
        if params is not None:
            params_with_api.update(params)

        try:
            request_retries = self._request_retries_count
            content = None
            while request_retries > 0:
                with timeout(self._request_timeout):
                    response = await self._session.request(  # type: ignore
                        method=method,
                        url=self._base_api_url + path,
                        params=params_with_api,
                        json=data,
                    )

                if response.status == 401:
                    raise IPX800InvalidAuthError()

                content = await response.json()

                if response.status >= 200 and response.status <= 206:
                    response.close()
                    return content

                request_retries -= 1
                sleep(self._request_retries_delay)

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

    async def ping(self) -> None:
        """Test a API request to test IPX800 connection."""
        await self._request_api("system/ipx")

    async def init_config(self) -> None:
        """Init the full config of the IPX."""
        print("Init the IPX800V5 configuration.")
        await self.update_ipx_info()
        await self.update_ipx_config()
        await self.update_extensions_config()
        await self.update_objects_config()

    async def get_ipx_info(self) -> dict:
        """Get IPX config."""
        return await self._request_api("system/info")

    async def global_get(self) -> dict:
        """Get all values from the IPX800 API."""
        values = {x["_id"]: x for x in await self._request_api("core/io")}
        values.update({x["_id"]: x for x in await self._request_api("core/ana")})
        return values

    async def reboot(self) -> None:
        """Reboot the IPX800."""
        try:
            await self.update_io(self.ipx_config["ioIPXReset_id"], True)
        except IPX800CannotConnectError:
            print("IPX800V5 rebooted")

    # Update configs from IPX API
    async def update_ipx_info(self) -> None:
        """Update IPX infos."""
        infos = await self._request_api("system/info")
        self._firmware_version = infos["firmwareVersion"]
        self._mac_address = infos["macAdress"]
        self._host_name = infos["hostName"]

    async def update_ipx_config(self) -> None:
        """Update IPX config."""
        self._ipx_config = await self._request_api(
            "system/ipx", params={"option": "filter_id"}
        )

    async def update_extensions_config(self) -> None:
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

    async def update_objects_config(self) -> None:
        """Update the list of configured objects."""
        objects_config = []
        for type_object in OBJECTS:
            search_object = (
                OBJECT_TIMER if type_object in [OBJECT_TEMPO] else type_object
            )
            try:
                for obj in await self._request_api(
                    f"object/{search_object}", params={"option": "filter_id"}
                ):
                    # ignore objects with same parent object
                    if search_object == OBJECT_TIMER and obj["func"] != type_object:
                        continue
                    objects_config.append(
                        {
                            API_CONFIG_TYPE: type_object,
                            API_CONFIG_ID: obj["_id"],
                            API_CONFIG_NAME: obj["name"],
                            API_CONFIG_PARAMS: obj,
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
        return extensions[ext_number][API_CONFIG_PARAMS]

    def get_ext_id(self, ext_type: str, ext_number: int) -> int:
        """Return the unique extension id generated by the IPX."""
        extensions = [
            x for x in self.extensions_config if x[API_CONFIG_TYPE] == ext_type
        ]
        return extensions[ext_number][API_CONFIG_ID]

    def get_ext_name(self, ext_type: str, ext_number: int) -> str:
        """Return the name set in the IPX config."""
        extensions = [
            x for x in self.extensions_config if x[API_CONFIG_TYPE] == ext_type
        ]
        return extensions[ext_number][API_CONFIG_NAME]

    async def get_ext_states(self, ext_type: str, ext_id: int) -> dict:
        """Return all values of extension."""
        return await self._request_api(f"ebx/{ext_type}/{ext_id}")

    def get_obj_config(self, obj_type: str, obj_number: int) -> dict:
        """Return the extension config."""
        objs = [x for x in self.objects_config if x[API_CONFIG_TYPE] == obj_type]
        return objs[obj_number][API_CONFIG_PARAMS]

    def get_obj_id(self, obj_type: str, obj_number: int) -> str:
        """Return the unique object id generated by the IPX."""
        objs = [x for x in self.objects_config if x[API_CONFIG_TYPE] == obj_type]
        return objs[obj_number][API_CONFIG_ID]

    def get_obj_name(self, obj_type: str, obj_number: int) -> str:
        """Return the name set in the IPX config."""
        objs = [x for x in self.objects_config if x[API_CONFIG_TYPE] == obj_type]
        return objs[obj_number][API_CONFIG_NAME]

    # Get/Update commands

    async def get_io(self, id: int) -> bool:
        """Get IO status on the IPX."""
        response = await self._request_api(f"core/io/{id}")
        return response["on"]

    async def get_ana(self, id: int) -> float:
        """Get an Analog status on the IPX."""
        response = await self._request_api(f"core/ana/{id}")
        return response["value"]

    async def get_str(self, id: int) -> str:
        """Get an strint value on the IPX."""
        response = await self._request_api(f"core/str/{id}")
        return response["value"]

    async def update_io(self, id: int, value: bool, command: str = "on") -> None:
        """Update an IO on the IPX."""
        await self._request_api(f"core/io/{id}", method="PUT", data={command: value})

    async def update_ana(self, id: int, value) -> None:
        """Update an Analog on the IPX."""
        if type(value) not in [int, float]:
            raise IPX800RequestError("Ana value need to be a int or a float type.")
        await self._request_api(f"core/ana/{id}", method="PUT", data={"value": value})

    async def update_str(self, id: int, value: str) -> None:
        """Update a string on the IPX."""
        await self._request_api(f"core/str/{id}", method="PUT", data={"value": value})

    # Create resource
    async def create_object(self, obj_type: str, params: dict, auth_token: str) -> dict:
        """Create a resource and update configuration from params."""
        new_object = await self._request_api(
            f"object/{obj_type}", method="POST", params={"AuthToken": auth_token}
        )
        return await self._request_api(
            f"object/{obj_type}/{new_object['_id']}",
            method="PUT",
            params={"AuthToken": auth_token},
            data=params,
        )

    # Async defs
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
