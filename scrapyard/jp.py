import hid
def list_hid_devices():
    # Initialize the HID device
    hid_device = hid.device()
    # Get a list of all connected HID devices
    devices = hid.enumerate()
    # Print details of each device
    for device in devices:
        print(f"Device Path: {device['path']}")
        print(f"Vendor ID: {device['vendor_id']}")
        print(f"Product ID: {device['product_id']}")
        print(f"Manufacturer: {device['manufacturer_string']}")
        print(f"Product: {device['product_string']}")
        print(f"Serial Number: {device['serial_number']}")
        print(f"Release Number: {device['release_number']}")
        print(f"Interface Number: {device['interface_number']}")
        print("-" * 40)
# Call the function to list HID devices
list_hid_devices()
