"""pypx800v5 constants."""

DEFAULT_TRANSITION = 1

IPX = "ipx"

TYPE_IO = "io"
TYPE_ANA = "ana"
TYPE_STR = "str"

API_CONFIG_TYPE = "type"
API_CONFIG_ID = "id"
API_CONFIG_NAME = "name"
API_CONFIG_PARAMS = "params"

# Extensions
EXT_XDIMMER = "xdimmer"
EXT_X8R = "x8r"
EXT_XTHL = "xthl"
EXT_X4FP = "x4fp"
EXT_X8D = "x8d"
EXT_X24D = "x24d"
EXT_X4VR = "x4vr"
EXT_XPWM = "xpwm"
EXT_X010V = "x010v"
EXT_XDISPLAY = "xdisplay"

EXTENSIONS = [
    EXT_XTHL,
    EXT_X4FP,
    EXT_X8D,
    EXT_X24D,
    EXT_X4VR,
    EXT_XDIMMER,
    EXT_X8R,
    EXT_XPWM,
    EXT_X010V,
    EXT_XDISPLAY,
]

# Objects
OBJECT_THERMOSTAT = "thermostat"
OBJECT_COUNTER = "counter"
OBJECT_TEMPO = "tempo"
OBJECT_TIMER = "timer"  # parent
OBJECT_PUSH = "push"
OBJECT_ACCESS_CONTROL = "access_control"

OBJECTS = [OBJECT_THERMOSTAT, OBJECT_COUNTER, OBJECT_TEMPO, OBJECT_ACCESS_CONTROL]
