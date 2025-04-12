"""
typedef struct
{
                                                     // No REPORT ID byte
                                                     // Collection: CA:GamePad CP:
  uint16_t GD_GamePadX;                              // Usage 0x00010030: X, Value = 0 to 65535
  uint16_t GD_GamePadY;                              // Usage 0x00010031: Y, Value = 0 to 65535
  uint16_t GD_GamePadRx;                             // Usage 0x00010033: Rx, Value = 0 to 65535
  uint16_t GD_GamePadRy;                             // Usage 0x00010034: Ry, Value = 0 to 65535
                                                     // Collection: CA:GamePad
  uint16_t GD_GamePadZ : 10;                         // Usage 0x00010032: Z, Value = 0 to 1023
  uint8_t  : 6;                                      // Pad
  uint16_t GD_GamePadRz : 10;                        // Usage 0x00010035: Rz, Value = 0 to 1023
  uint8_t  : 6;                                      // Pad
  uint8_t  BTN_GamePadButton1 : 1;                   // Usage 0x00090001: Button 1 Primary/trigger, Value = 0 to 0
  uint8_t  BTN_GamePadButton2 : 1;                   // Usage 0x00090002: Button 2 Secondary, Value = 0 to 0
  uint8_t  BTN_GamePadButton3 : 1;                   // Usage 0x00090003: Button 3 Tertiary, Value = 0 to 0
  uint8_t  BTN_GamePadButton4 : 1;                   // Usage 0x00090004: Button 4, Value = 0 to 0
  uint8_t  BTN_GamePadButton5 : 1;                   // Usage 0x00090005: Button 5, Value = 0 to 0
  uint8_t  BTN_GamePadButton6 : 1;                   // Usage 0x00090006: Button 6, Value = 0 to 0
  uint8_t  BTN_GamePadButton7 : 1;                   // Usage 0x00090007: Button 7, Value = 0 to 0
  uint8_t  BTN_GamePadButton8 : 1;                   // Usage 0x00090008: Button 8, Value = 0 to 0
  uint8_t  BTN_GamePadButton9 : 1;                   // Usage 0x00090009: Button 9, Value = 0 to 0
  uint8_t  BTN_GamePadButton10 : 1;                  // Usage 0x0009000A: Button 10, Value = 0 to 0
  uint8_t  : 6;                                      // Pad
  uint8_t  GD_GamePadHatSwitch : 4;                  // Usage 0x00010039: Hat switch, Value = 1 to 8, Physical = (Value - 1) x 45 in degrees
  uint8_t  : 4;                                      // Pad
                                                     // Collection: CA:GamePad CP:SystemControl
  uint8_t  GD_GamePadSystemControlSystemMainMenu : 1; // Usage 0x00010085: System Main Menu, Value = 0 to 1
  uint8_t  : 7;                                      // Pad
                                                     // Collection: CA:GamePad
  uint8_t  GEN_GamePadBatteryStrength;               // Usage 0x00060020: Battery Strength, Value = 0 to 255
} inputReport_t;
"""

# These were used when I was trying to map between controllers
# To map to a XAC - but was defeated in that by using a driver
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

XAC_NEUTRAL = [0x08, 0x00, 0x00, 0x5E, 0x00, 0x20, 0x7F, 0xFF]


XAC_TRIANGLE = (0, 0x80)
XAC_CIRCLE = (0, 0x40)
XAC_CROSS = (0, 0x10)
XAC_SQUARE = (0, 0x20)

XAC_DPAD_MASK = 0x0F
XAC_DPAD_NONE = (0, 0x08)
XAC_DPAD_U = (0, 0x00)
XAC_DPAD_R = (0, 0x02)
XAC_DPAD_D = (0, 0x04)
XAC_DPAD_L = (0, 0x06)

XAC_RPADDLE = (1, 0x01)
XAC_LPADDLE = (1, 0x02)
XAC_L1 = (1, 0x80)
XAC_L2 = (1, 0x08)
XAC_R1 = (1, 0x40)
XAC_R2 = (1, 0x04)
XAC_SELECT = (1, 0x10)
XAC_START = (1, 0x20)

XAC_PSMENU = (2, 0x08)
XAC_GEARUP = (2, 0x01)
XAC_GEARDOWN = (2, 0x02)
XAC_BACK = (2, 0x04)
XAC_ADJUST_CLOCKWISE = (2, 0x10)
XAC_ADJUST_ANTICLOCKWISE = (2, 0x20)
XAC_PLUS = (2, 0x80)
XAC_MINUS = (2, 0x40)

# Bytes

XAC_XAC_HIGHBYTE = 5
XAC_XAC_LOWBYTE = 4  # 0000-EFF3 But 0000 is extreme
XAC_ACCELERATEBYTE = 6  # 0-FF 0 IS DOWN
XAC_BRAKEBYTE = 7  # 0-FF 0 IS DOWN


# (FromByte,From Bit) -> (ToByte,ToBit)

# XAC Has dedicated Gear buttons and Shifter that arent on the controller
# Stick Click is not used in TDU2 at all so will use that

BUTTON_MAPPINGS = [
    (GAMEPAD_TRIANGLE, XAC_TRIANGLE),
    (GAMEPAD_CIRCLE, XAC_CIRCLE),
    (GAMEPAD_SQUARE, XAC_SQUARE),
    (GAMEPAD_CROSS, XAC_CROSS),
    (GAMEPAD_R1, XAC_R2),
    (GAMEPAD_L1, XAC_L2),
    (GAMEPAD_PSMENU, XAC_PSMENU),
    (GAMEPAD_START, XAC_START),
    (GAMEPAD_SELECT, XAC_SELECT),
    (GAMEPAD_LJOY_BUTTON, XAC_GEARDOWN),
    (GAMEPAD_RJOY_BUTTON, XAC_GEARUP),
]

#These made it work in PS3 menu screen
XMB_BUTTON_MAPPINGS = [
    (GAMEPAD_TRIANGLE, XAC_TRIANGLE),
    (GAMEPAD_CIRCLE, XAC_CIRCLE),
    (GAMEPAD_CROSS, XAC_SQUARE),
    (GAMEPAD_SQUARE, XAC_CROSS),
    (GAMEPAD_R1, XAC_R2),
    (GAMEPAD_L1, XAC_L2),
    (GAMEPAD_PSMENU, XAC_PSMENU),
    (GAMEPAD_START, XAC_START),
    (GAMEPAD_SELECT, XAC_SELECT),
    (GAMEPAD_LJOY_BUTTON, XAC_GEARDOWN),
    (GAMEPAD_RJOY_BUTTON, XAC_GEARUP),
]


DPAD_MAPPINGS = [
    (GAMEPAD_DPAD_NONE, XAC_DPAD_NONE),
    (GAMEPAD_DPAD_U, XAC_DPAD_U),
    (GAMEPAD_DPAD_D, XAC_DPAD_D),
    (GAMEPAD_DPAD_L, XAC_DPAD_L),
    (GAMEPAD_DPAD_R, XAC_DPAD_R),
]


STEAM_BUTTON_MAPPINGS = [
    XAC_CROSS,XAC_CIRCLE,XAC_TRIANGLE,XAC_SQUARE,
    XAC_START,XAC_PSMENU,XAC_SELECT,
    XAC_GEARUP,XAC_GEARDOWN,XAC_L1,XAC_R1
]

STEAM_BUTTONS2_MAPPINGS =  [XAC_LPADDLE,XAC_RPADDLE,XAC_PLUS,XAC_MINUS]

STEAM_DPAD_MAPPINGS = [  XAC_DPAD_U,XAC_DPAD_L,XAC_DPAD_D,XAC_DPAD_R]