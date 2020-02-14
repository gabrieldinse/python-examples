import sys
import re

# run the script as <python root/regex_library.py "hello worl" "hello world">

# pattern to verified, from the beginning to the end
pattern = sys.argv[1]
# string to be analyzed
search_string = sys.argv[2]

match = re.match(pattern, search_string)
if match:
    print("'{}' matches '{}'".format(search_string, pattern))
else:
    print("'{}' does not match '{}'".format(search_string, pattern))