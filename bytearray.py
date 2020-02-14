# bytearray get a bytes object as argument
b = bytearray(b"abcdefgh")
# bytarray is mutable, so you can change its slices without
# creating a new object
b[4:6] = b"\x15\xa3"
print(b)

print('To change a single element is kinda different')
# If we want to change/atribute a single element, bytearray expects us to
# pass a value from 0 to 255, not a char or bytes object.
# So we have 'ord', that returns an interger (ordinal) representing the
# character passed to the function
b[3] = ord(b'1')
b[2] = ord('z')
b[1] = 68 # 'D'
print(b)