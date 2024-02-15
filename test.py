import struct

data = bytearray(
    b"distance_msg\x00\x00\x00\x00running\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x05\x00\x00\x00\xbb\x84\xc2?\x00\x00\x00\x00\x9e\xc9r\xc2\xfd\xc3t\xc2"
)


try:
    print(f"Buffer Size: {len(data)}")
    print(f"Struct Size: {struct.calcsize("15s 15s I I f H f f")}")
    unpacked_data = struct.unpack("15s 15s I I f H f f", data)
    print(unpacked_data)

except Exception as e:
    print(f"Exeption {e}")
