# bytes object in hexadecimal
characters = b'\x63\x6c\x69\x63\x68\xe9'
print(characters)
# str object decoded to 'latin-1'
# default (no args in 'decode') is 'utf-8' (ASCII)
print(characters.decode("latin-1"))

print('\nMany forms to encode:')
characters = "clich\xe9"
print(characters.encode("UTF-8"))
print(characters.encode("latin-1"))
print(characters.encode("CP437"))
# nao cabe na representacao ASCII, entao pode-se usar um segundo argumento
# print(characters.encode("ascii"))
# print(characters.encode("ascii", 'strict')) -> 'strict' = default
print(characters.encode("ascii", 'replace'))
print(characters.encode("ascii", 'ignore'))
print(characters.encode("ascii", 'xmlcharrefreplace'))