To reverse engineer KICKR 

On an Androidn Phone enable developer mode
Then Turn on Bluetooth HCI Logging 
Turn Bluetooth off and on again to enable

Now interack with KICKR - Change power form 5 to 100 and back to 0

Turn BT Off
Turn BT Debug Off
<Do not turn BT ON>

attach to phone using SDK and adb

download data

```
adb bugreport filename
```

then unzip

```
unzip filename.zip
```

change to `FS/data/log/bt`

```
 tshark -xPVr btsnoop_hci.log > btsnoop.txt


 ```

 Now yoy can look for packets where your phone is writing

 ```

 1321 280.702071 SamsungE_11:e7:78 (John's S22) → f5:7c:ad:e6:7d:c9 () ATT 14 Sent Write Command, Handle: 0x0025 (Generic Access Profile: Central Address Resolution: Unknown)
Frame 1321: 14 bytes on wire (112 bits), 14 bytes captured (112 bits)
    Encapsulation type: Bluetooth H4 with linux header (99)
    Arrival Time: Mar 23, 2025 16:32:18.977847000 GMT
    [Time shift for this packet: 0.000000000 seconds]
    Epoch Time: 1742747538.977847000 seconds
    [Time delta from previous captured frame: 0.004248000 seconds]
    [Time delta from previous displayed frame: 0.004248000 seconds]
    [Time since reference or first frame: 280.702071000 seconds]
    Frame Number: 1321
    Frame Length: 14 bytes (112 bits)
    Capture Length: 14 bytes (112 bits)
    [Frame is marked: False]
    [Frame is ignored: False]
    Point-to-Point Direction: Sent (0)
    [Protocols in frame: bluetooth:hci_h4:bthci_acl:btl2cap:btatt]
Bluetooth
Bluetooth HCI H4
    [Direction: Sent (0x00)]
    HCI Packet Type: ACL Data (0x02)
Bluetooth HCI ACL Packet
    .... 0000 0000 0001 = Connection Handle: 0x001
    ..00 .... .... .... = PB Flag: First Non-automatically Flushable Packet (0)
    00.. .... .... .... = BC Flag: Point-To-Point (0)
    Data Total Length: 9
    Data
    [Connect in frame: 1137]
    [Source BD_ADDR: SamsungE_11:e7:78 (a4:75:b9:11:e7:78)]
    [Source Device Name: John's S22]
    [Source Role: Unknown (0)]
    [Destination BD_ADDR: f5:7c:ad:e6:7d:c9 (f5:7c:ad:e6:7d:c9)]
    [Destination Device Name: ]
    [Destination Role: Unknown (0)]
    [Current Mode: Unknown (-1)]
Bluetooth L2CAP Protocol
    Length: 5
    CID: Attribute Protocol (0x0004)
Bluetooth Attribute Protocol
    Opcode: Write Command (0x52)
        0... .... = Authentication Signature: False
        .1.. .... = Command: True
        ..01 0010 = Method: Write Request (0x12)
    Handle: 0x0025 (Generic Access Profile: Central Address Resolution: Unknown)
        [Service UUID: Generic Access Profile (0x1800)]
        [Characteristic UUID: Central Address Resolution (0x2aa6)]
    Value: 0104

0000  02 01 00 09 00 05 00 04 00 52 25 00 01 04         .........R%...

```

Loog in the log for Write COmmand


