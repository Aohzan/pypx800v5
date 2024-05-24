"""IPX800V5 Thermostat."""

from .const import OBJECT_THERMOSTAT as obj_type
from .ipx800 import IPX800
from .object import Object


class Thermostat(Object):
    """Represent an IPX800 thermostat object."""

    def __init__(self, ipx: IPX800, obj_number: int):
        """Init the object."""
        super().__init__(ipx, obj_type, obj_number)
        # IO
        self.io_state_id = self._config["ioOutput_id"]
        self.io_fault_id = self._config["ioFault_id"]
        self.io_onoff_id = self._config["ioOnOff_id"]
        # Ana
        self.ana_measure_id = self._config["anaMeasure_id"]
        self.ana_consigne_id = self._config["anaCurrSetPoint_id"]
        # Modes
        self.io_eco_id = self._config["ioEco_id"]
        self.io_comfort_id = self._config["ioComfort_id"]
        self.io_nofrost_id = self._config["ioNoFrost_id"]

        self._hysteresis = self._config["hysteresis"]

    @property
    async def current_temperature(self) -> float:
        """Return the current thermostat temperature."""
        return await self._ipx.get_ana(self.ana_measure_id)

    @property
    async def target_temperature(self) -> float:
        """Return the target thermostat temperature."""
        return await self._ipx.get_ana(self.ana_consigne_id)

    @property
    async def status(self) -> bool:
        """Return if thermostat is turned on."""
        return await self._ipx.get_io(self.io_onoff_id)

    @property
    async def heating(self) -> bool:
        """Return if thermostat heating."""
        return await self._ipx.get_io(self.io_state_id)

    @property
    async def fault(self) -> bool:
        """Return if thermostat is in fault status."""
        return await self._ipx.get_io(self.io_fault_id)

    @property
    async def mode_eco(self) -> bool:
        """Return if eco mode is activated."""
        return await self._ipx.get_io(self.io_eco_id)

    @property
    async def mode_comfort(self) -> bool:
        """Return if comfort mode is activated."""
        return await self._ipx.get_io(self.io_comfort_id)

    @property
    async def mode_nofrost(self) -> bool:
        """Return if eco mode is activated."""
        return await self._ipx.get_io(self.io_nofrost_id)

    async def set_mode_eco(self) -> None:
        """Activate the eco mode."""
        await self._ipx.update_io(self.io_eco_id, True)

    async def set_mode_comfort(self) -> None:
        """Activate the comfort mode."""
        await self._ipx.update_io(self.io_comfort_id, True)

    async def set_mode_nofrost(self) -> None:
        """Activate the no frost mode."""
        await self._ipx.update_io(self.io_nofrost_id, True)

    async def set_target_temperature(self, temperature: float) -> None:
        """Set target temperature."""
        await self._ipx.update_ana(self.ana_consigne_id, temperature)

    async def force_heating(self, heat: bool = True) -> None:
        """Set target temperature."""
        await self._ipx.update_io(self.io_onoff_id, heat)

    async def on(self) -> None:
        """Turn on the thermostat."""
        await self._ipx.update_io(self.io_onoff_id, True)

    async def off(self) -> None:
        """Turn off the thermostat."""
        await self._ipx.update_io(self.io_onoff_id, False)

    async def update_params(
        self,
        hysteresis: float | None = None,
        comfortTemp: float | None = None,
        ecoTemp: float | None = None,
        noFrostTemp: float | None = None,
        faultTime: int | None = None,
        invMode: bool | None = None,
        safeMode: bool | None = None,
    ) -> None:
        """Update thermostat params."""
        params = {}
        if hysteresis:
            params["hysteresis"] = hysteresis
        if comfortTemp:
            params["setPointComfort"] = comfortTemp
        if ecoTemp:
            params["setPointEco"] = ecoTemp
        if noFrostTemp:
            params["setPointNoFrost"] = noFrostTemp
        if faultTime:
            params["faultTime"] = faultTime
        if invMode:
            params["invMode"] = invMode
        if safeMode:
            params["safeMode"] = safeMode
        await self._ipx._request_api(
            f"object/thermostat/{self._obj_id}",
            method="PUT",
            data=params,
        )
