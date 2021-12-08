# pypx800v5 - Python GCE IPX800 V5

Control the IPX800 V5, its extensions and objects:

- Thermostat
- Counter
- Tempo
- X-8R
- X-8D
- X-24D
- X-Dimmer
- X-PWM
- X-THL
- X-4VR
- X-4FP

## IPX800 parameters

- host: ip or hostname (mandatory)
- port: (default: `80`)
- api_key: (mandatory)
- request_timeout: timeout for request in seconds (default: `30`)
- request_retries_count: retry request if an error occured (default: `3`)
- request_retries_delay: delay in seconds before trying request (default: `0.1`)
- session: aiohttp.client.ClientSession

## Example

```python
import asyncio

from pypx800v5 import *


async def main():
    async with IPX800(host='192.168.1.123', api_key='xxx') as ipx:
        print("Ping OK" if await ipx.ping() else "Ping KO")
        await ipx.init_config()

        relay = IPX800Relay(ipx, 1)
        print(await relay.status)
        await relay.on()

        input = IPX800DigitalInput(ipx, 2)
        print(await input.status)

        input = IPX800AnalogInput(ipx, 1)
        print(await input.status)

        light = X8R(ipx, 1, 7)
        print(await light.status)
        await light.on()

        pwm = XPWM(ipx, 1, 6)
        print(await pwm.status)
        print(await pwm.level)
        await pwm.set_level(90)

        light = XDimmer(ipx, 1, 2)
        print(await light.status)
        print(await light.level)
        await light.on()

        input = X24D(ipx, 1, 14)
        print(await input.status)

        capteur = XTHL(ipx, 1)
        print(await capteur.temperature)
        print(await capteur.humidity)
        print(await capteur.luminosity)

        tempo = Tempo(ipx, 1)
        print(tempo.name)
        print(await tempo.status)
        print(await tempo.time)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
