DEFAULT_TRANSITION = 1

IPX = "ipx"
EXT_XDIMMER = "xdimmer"
EXT_X8R = "x8r"
EXT_XTHL = "xthl"
EXT_X4FP = "x4fp"
EXT_X8D = "x8d"
EXT_X24D = "x24d"
EXT_X4VR = "x4vr"
EXT_X010V = "x010v"
EXT_X200 = "x200"
EXT_X400 = "x400"
EXT_XDISPLAY = "xdisplay"
EXT_XPWM = "xpwm"

EXTENSIONS = [
    EXT_XTHL,
    EXT_X4FP,
    EXT_X24D,
    EXT_X4VR,
    EXT_XDIMMER,
    EXT_X8R,
    EXT_X010V,
    EXT_X200,
    EXT_X400,
    EXT_XDISPLAY,
    EXT_XPWM,
]

EXT_CONFIG_TYPE = "type"
EXT_CONFIG_ID = "id"
EXT_CONFIG_NAME = "name"
EXT_CONFIG_PARAMS = "params"

TYPE_IO = "io"
TYPE_ANA = "ana"
TYPE_STR = "str"

MAPPING_IO_OUTPUT_ID = {
    IPX: "ioRelayState_id",
    EXT_XDIMMER: "ioOn_id",
    EXT_X8R: "ioOutputState_id",
}

MAPPING_IO_COMMAND_ID = {
    IPX: "ioRelays_id",
    EXT_XDIMMER: "ioOn_id",
    EXT_X8R: "ioOutput_id",
}

MAPPING_IO_INPUT_ID = {
    IPX: "ioDInput_id",
    EXT_X8D: "ioInput_id",
    EXT_X24D: "ioInput_id",
}

MAPPING_ANA_OUTPUT_ID = {
    EXT_XDIMMER: "anaPosition_id",
    EXT_XPWM: "anaCommand_id",
}

MAPPING_ANA_INPUT_ID = {IPX: "ana_IPX_Input"}

MAPPING_ANA_COMMAND_ID = {
    EXT_XDIMMER: "anaCommand_id",
    EXT_XPWM: "anaCommand_id",
}
