# These were used when I was trying to map between controllers
# To map to a wheel - but was defeated in that by using a driver
# 2021 comment (What did I mean there?)

GAMEPAD_TRIANGLE = (0, 0x08)
GAMEPAD_CIRCLE = (0, 0x04)
GAMEPAD_CROSS = (0, 0x02)
GAMEPAD_SQUARE = (0, 0x01)

GAMEPAD_DPAD_MASK = 0x0F
GAMEPAD_DPAD_NONE = (2, 0x0F)
GAMEPAD_DPAD_U = (2, 0x00)
GAMEPAD_DPAD_R = (2, 0x02)
GAMEPAD_DPAD_D = (2, 0x04)
GAMEPAD_DPAD_L = (2, 0x06)


GAMEPAD_PSMENU = (1, 0x10)
GAMEPAD_SELECT = (1, 0x01)
GAMEPAD_START = (1, 0x02)

GAMEPAD_LJOY_BUTTON = (1, 0x04)
GAMEPAD_RJOY_BUTTON = (1, 0x08)
GAMEPAD_L1 = (0, 0x10)
GAMEPAD_R1 = (0, 0x20)
GAMEPAD_L2 = (0, 0x40)
GAMEPAD_R2 = (0, 0x80)

GAMEPAD_RTRIGGER = 18
GAMEPAD_LTRIGGER = 17
# These are Bytes not Bits

GAMEPAD_LJOY_X = 3
GAMEPAD_LJOY_Y = 4
GAMEPAD_RJOY_X = 5
GAMEPAD_RJOY_Y = 6

CLICKER_BUTTONS = 2
CLICKER_LEFT = [0x4B]
CLICKER_RIGHT = [0x4E]
CLICKER_UP = [0x05]
CLICKER_DOWN = [0x3E, 0x29]  # Toggles


STEER_MIN = 0x0000
STEER_MAX = 0x3FFF
STEER_MID = 0x1FFF

WHEEL_NEUTRAL = [0x08, 0x00, 0x00, 0x5E, 0x00, 0x20, 0x7F, 0xFF]


WHEEL_TRIANGLE = (0, 0x80)
WHEEL_CIRCLE = (0, 0x40)
WHEEL_CROSS = (0, 0x10)
WHEEL_SQUARE = (0, 0x20)

WHEEL_DPAD_MASK = 0x0F
WHEEL_DPAD_NONE = (0, 0x08)
WHEEL_DPAD_U = (0, 0x00)
WHEEL_DPAD_R = (0, 0x02)
WHEEL_DPAD_D = (0, 0x04)
WHEEL_DPAD_L = (0, 0x06)

WHEEL_RPADDLE = (1, 0x01)
WHEEL_LPADDLE = (1, 0x02)
WHEEL_L1 = (1, 0x80)
WHEEL_L2 = (1, 0x08)
WHEEL_R1 = (1, 0x40)
WHEEL_R2 = (1, 0x04)
WHEEL_SELECT = (1, 0x10)
WHEEL_START = (1, 0x20)

WHEEL_PSMENU = (2, 0x08)
WHEEL_GEARUP = (2, 0x01)
WHEEL_GEARDOWN = (2, 0x02)
WHEEL_BACK = (2, 0x04)
WHEEL_ADJUST_CLOCKWISE = (2, 0x10)
WHEEL_ADJUST_ANTICLOCKWISE = (2, 0x20)
WHEEL_PLUS = (2, 0x80)
WHEEL_MINUS = (2, 0x40)

# Bytes

WHEEL_WHEEL_HIGHBYTE = 5
WHEEL_WHEEL_LOWBYTE = 4  # 0000-EFF3 But 0000 is extreme
WHEEL_ACCELERATEBYTE = 6  # 0-FF 0 IS DOWN
WHEEL_BRAKEBYTE = 7  # 0-FF 0 IS DOWN


# (FromByte,From Bit) -> (ToByte,ToBit)

# Wheel Has dedicated Gear buttons and Shifter that arent on the controller
# Stick Click is not used in TDU2 at all so will use that

BUTTON_MAPPINGS = [
    (GAMEPAD_TRIANGLE, WHEEL_TRIANGLE),
    (GAMEPAD_CIRCLE, WHEEL_CIRCLE),
    (GAMEPAD_SQUARE, WHEEL_SQUARE),
    (GAMEPAD_CROSS, WHEEL_CROSS),
    (GAMEPAD_R1, WHEEL_R2),
    (GAMEPAD_L1, WHEEL_L2),
    (GAMEPAD_PSMENU, WHEEL_PSMENU),
    (GAMEPAD_START, WHEEL_START),
    (GAMEPAD_SELECT, WHEEL_SELECT),
    (GAMEPAD_LJOY_BUTTON, WHEEL_GEARDOWN),
    (GAMEPAD_RJOY_BUTTON, WHEEL_GEARUP),
]

#These made it work in PS3 menu screen
XMB_BUTTON_MAPPINGS = [
    (GAMEPAD_TRIANGLE, WHEEL_TRIANGLE),
    (GAMEPAD_CIRCLE, WHEEL_CIRCLE),
    (GAMEPAD_CROSS, WHEEL_SQUARE),
    (GAMEPAD_SQUARE, WHEEL_CROSS),
    (GAMEPAD_R1, WHEEL_R2),
    (GAMEPAD_L1, WHEEL_L2),
    (GAMEPAD_PSMENU, WHEEL_PSMENU),
    (GAMEPAD_START, WHEEL_START),
    (GAMEPAD_SELECT, WHEEL_SELECT),
    (GAMEPAD_LJOY_BUTTON, WHEEL_GEARDOWN),
    (GAMEPAD_RJOY_BUTTON, WHEEL_GEARUP),
]


DPAD_MAPPINGS = [
    (GAMEPAD_DPAD_NONE, WHEEL_DPAD_NONE),
    (GAMEPAD_DPAD_U, WHEEL_DPAD_U),
    (GAMEPAD_DPAD_D, WHEEL_DPAD_D),
    (GAMEPAD_DPAD_L, WHEEL_DPAD_L),
    (GAMEPAD_DPAD_R, WHEEL_DPAD_R),
]


STEAM_BUTTON_MAPPINGS = [
    WHEEL_CROSS,WHEEL_CIRCLE,WHEEL_TRIANGLE,WHEEL_SQUARE,
    WHEEL_START,WHEEL_PSMENU,WHEEL_SELECT,
    WHEEL_GEARUP,WHEEL_GEARDOWN,WHEEL_L1,WHEEL_R1
]

STEAM_BUTTONS2_MAPPINGS =  [WHEEL_LPADDLE,WHEEL_RPADDLE,WHEEL_PLUS,WHEEL_MINUS]

STEAM_DPAD_MAPPINGS = [  WHEEL_DPAD_U,WHEEL_DPAD_L,WHEEL_DPAD_D,WHEEL_DPAD_R]