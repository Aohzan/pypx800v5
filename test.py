import asyncio
import os

from pypx800v5 import *

IPX_HOST = os.environ["IPX_HOST"]
IPX_API_KEY = os.environ["IPX_API_KEY"]


async def main():
    async with IPX800(host=IPX_HOST, api_key=IPX_API_KEY) as ipx:
        await ipx.ping()
        await ipx.init_config()

        xdisplay = XDisplay(ipx, 0)
        await xdisplay.refresh_screens()
        for screen in xdisplay.screens:
            print(f"{screen.id} - {screen.name} - {screen.type}")
        print(f"screen status ? {await xdisplay.screen_status}")
        print(f"screen locked ? {await xdisplay.screen_lock_status}")
        print(f"current screen ? {await xdisplay.current_screen_id}")
        await xdisplay.set_screen(0)
        print(f"current screen ? {await xdisplay.current_screen_id}")

        access_control = AccessControl(ipx, 0)
        print(await access_control.success)
        print(await access_control.fault)
        print("Last code: ", await access_control.last_code)
        print("Codes: ", await access_control.codes)

        # relay = IPX800Relay(ipx, 0)
        # print(await relay.status)
        # await relay.on()

        # opencoll = IPX800OpenColl(ipx, 0)
        # print(await opencoll.status)
        # await opencoll.on()

        # input = IPX800DigitalInput(ipx, 2)
        # print(await input.status)

        # input = IPX800AnalogInput(ipx, 0)
        # print(await input.status)

        # input = IPX800OptoInput(ipx, 0)
        # print(await input.status)

        # light = X8R(ipx, 0, 7)
        # print(await light.status)
        # await light.on()

        # pwm = XPWM(ipx, 0, 6)
        # print(await pwm.status)
        # print(await pwm.level)
        # await pwm.set_level(90)

        # light = XDimmer(ipx, 0, 2)
        # print(await light.status)
        # print(await light.level)
        # await light.on()

        # input = X24D(ipx, 0, 14)
        # print(await input.status)

        # capteur = XTHL(ipx, 0)
        # print(await capteur.temperature)
        # print(await capteur.humidity)
        # print(await capteur.luminosity)

        # tempo = Tempo(ipx, 0)
        # print(tempo.name)
        # print(await tempo.status)
        # print(await tempo.time)

        # x010v_output = X010V(ipx, 0, 2)
        # print(await x010v_output.status)
        # print(await x010v_output.level)
        # await x010v_output.on()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
