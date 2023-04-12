#!/usr/bin/env python3

########################################################################

import sys
import binascii

########################################################################

# input_string = 'ĮŇŤẸŘŇẸŤ'
# input_string = 'ᑕOᗰᗰᑌᑎIᑕᗩTIOᑎᔕ'
# input_string = 'ᔕ'
# input_string = 'ČỖϻϻǗŇĮČÃŤĮỖŇŜ'

input_string = "abcde"
# input_string = "αβγδε"
# input_string = "早上好"
# input_string = "おはようございます"

# Ɇ₦₵ØĐł₦₲ ₳₦Đ ĐɆ₵ØĐł₦₲ ₣ØⱤ ₦Ɇ₮₩ØⱤ₭ ₮ɆӾ₮ ₮Ɽ₳₦₴₥ł₴₴łØ₦
# input_string = "Ɽ"
# input_string = "₴"

# input_string = "Ɇ"

print("Input string: ", input_string)

sys.stdout.write("%-30s" % " ")
for c in input_string:
    sys.stdout.write("%-15s" % c)
print()

# Given a string representing one Unicode character, ord returns an
# integer representing the Unicode code point of that character.  Hex
# takes an integer and returns a lower case hex string representation,
# e.g., '0x61'.

sys.stdout.write("%-30s" % "Unicode code point")

for c in input_string:
    sys.stdout.write("%-15s" % hex(ord(c)))
print()

# Output the various encodings of the input string. For each unicode
# character in the string: 1) get the encoding as a bytes object; 2)
# For each bytes object, convert it to its printable ascii hex value
# using binascii.hexlify. This gives a new bytes object. Then convert
# them to a string for printing.

encoder_list = [
    "utf-8",
    "utf-16-le",
    "utf-16-be",
    "utf-32-le",
    "utf-32-be"
]

for encoder in encoder_list:
    sys.stdout.write("%-30s" % encoder)
    for c in input_string:
        bytes = c.encode(encoder)
        hex_bytes_str = bytes.hex()
        sys.stdout.write("%-15s" % hex_bytes_str)
        # Or:
        # hex_bytes = binascii.hexlify(bytes)
        # sys.stdout.write("%-15s" % hex_bytes)

        
    print()




    
