# Changelog

<!-- version list -->

## v1.5.0 (2026-10-13)

### Bug Fixes

- Await status in X-PWM toggle
  ([`d359d6f`](https://github.com/Aohzan/pypx800v5/commit/d359d6f601091d079750bc23a7222dfbd7bad687))

- Send falsy values in thermostat update_params
  ([`e481727`](https://github.com/Aohzan/pypx800v5/commit/e481727afe55f5be76f93e0238dc0970e88e36d6))

- Use asyncio.timeout instead of async_timeout
  ([`bd6e9b6`](https://github.com/Aohzan/pypx800v5/commit/bd6e9b6ad1df1fb9cd934efd60117ccd52adc6b6))

### Build System

- Package with pyproject.toml and uv
  ([`f98a211`](https://github.com/Aohzan/pypx800v5/commit/f98a2118dc6dfe6ba191ffe2fd4a6e7bbc7df857))

### Continuous Integration

- Keep actions and dev tools up to date with Dependabot
  ([`06f3a71`](https://github.com/Aohzan/pypx800v5/commit/06f3a713b79545431d271acaa5a380fd67f9df80))

- Release to PyPI with python-semantic-release
  ([`2d1e945`](https://github.com/Aohzan/pypx800v5/commit/2d1e9451cb55f56ba044d0ef2a10f8bcaba91c36))

### Features

- Add X-400 extension
  ([`c9914ea`](https://github.com/Aohzan/pypx800v5/commit/c9914eacf9708aa8a14dfed1f04065851960d288))

- Expose the thermostat inverted mode
  ([`6785590`](https://github.com/Aohzan/pypx800v5/commit/67855908b8b8705df2600982366c0bcd27a737e7))


## 1.4.3

- Revert 1.4.2 changes

## 1.4.2

- Fix X-Dimmer off method
- Fix X4VR close method
- Fix X-010V off method

## 1.4.1

- Fix X-Display V2 screens id

## 1.4.0

- Add X-Display V2 new type of screens: weather, consumption, energy
- Fix X-Display V2 unknown screens

## 1.3.4

- Bump requirements to fix security issue

## 1.3.3

- Fix context error with request timeout

## 1.3.2

- Add LOGGER to get proper logs
- Fix sleep error in API call when retrying a request

## 1.3.1

- Add init_config to Thermostat

## 1.3.0

- Add XDisplay V2 screens
- Add Access Control support

## 1.2.2

- Lint

## 1.2.1

- Bump dependencies to fix security issue

## 1.2.0

- Add XDisplay V2 new type of screens: slider, player and four buttons

## 1.1.1

- Fix X-010V level

## 1.1.0

- Add X-Display support
- bump async_timeout

## 1.0.0

- Stable release
- `ext_number` starts now from 0 to match IPX index

## 0.15.0

- Rename methods to update config through init

## 0.14.0

- Change ping method

## 0.13.5

- Fix CI

## 0.13.4

- Fix missing X8D and X010V in extensions

## 0.13.3

- Fix X4FP mode

## 0.13.2

- Add dimmer level verification

## 0.13.1

- Fix constants exports

## 0.13.0

- Add Octo and Open Collector i/o support
- Add X-010V support
- Fix `get_ext_states` method (use by X4FP)
- Lint

## 0.12.0

- Remove api_version property removed in 5.4.3.1 firmware

## 0.11.0

- Increase retries count and delay

## 0.10.0

- Add request retries

## 0.9.0

- Increase timeout

## 0.8.0

- Add X8R long push id

## 0.7.0

- Add object creation method
- Add str methods

## 0.6.1

- Initial release
