# pypx800v5 - Python GCE IPX800 v5

Control the IPX800 v5 ans its extensions: X-PWM, X-THL, X-4VR, X-4FP, X-8R, X-8D, X-24D and X-Dimmer trough:

- Relay
- Virtual output
- Virtual input
- Digital input
- Analog input
- Counter
- X-Dimmer output
- X-PWM channel
- X-THL (temp, hum, lux)
- X-4VR output
- X-4FP zone

## IPX800 parameters

- host: ip or hostname (mandatory)
- port: (default: `80`)
- api_key: (mandatory)
- request_retries: number of request retries on error (default: `3`)
- request_timeout: timeout for request (default: `5`)
- request_checkstatus: true to raise error if IPX800 return no success result like partial result, after `request_retries` retries (default: `True`)
- session: aiohttp.client.ClientSession

## Example

```python
import asyncio

from pypx800v5 import (IPX800, X4FP, X4VR, XPWM, XTHL, AInput, VAInput, DInput, Relay,
                     VInput, VOutput, XDimmer)


async def main():
    async with IPX800(host='192.168.1.123', api_key='xxx') as ipx:
        config = await ipx.get_config()

        data = await ipx.global_get()
        print("all values:", data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```
