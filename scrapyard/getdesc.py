import usb.core
import usb.util

# Replace these with the correct Vendor ID and Product ID
VENDOR_ID = 0x1234
PRODUCT_ID = 0x5678

# Find the USB device
dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError("Device not found")

# Get HID Descriptor
HID_DESCRIPTOR_TYPE = 0x21
REPORT_DESCRIPTOR_TYPE = 0x22

# Find the first HID interface
for cfg in dev:
    for intf in cfg:
        if usb.util.find_descriptor(intf, bDescriptorType=HID_DESCRIPTOR_TYPE) is not None:
            hid_descriptor = usb.util.find_descriptor(
                intf,
                bDescriptorType=HID_DESCRIPTOR_TYPE
            )

            if hid_descriptor:
                hid_report_descriptor_size = hid_descriptor[6] | (hid_descriptor[7] << 8)
                hid_report_descriptor = dev.ctrl_transfer(
                    bmRequestType=usb.util.build_request_type(usb.util.CTRL_IN,
                                                              usb.util.CTRL_TYPE_STANDARD,
                                                              usb.util.CTRL_RECIPIENT_INTERFACE),
                    bRequest=usb.REQ_GET_DESCRIPTOR,
                    wValue=(REPORT_DESCRIPTOR_TYPE << 8),
                    wIndex=intf.bInterfaceNumber,
                    data_or_wLength=hid_report_descriptor_size
                )

                print("HID Report Descriptor:")
                print(hid_report_descriptor)
                break

