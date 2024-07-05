import json
from deepdiff import DeepDiff

# Example JSON objects
json1 = '''
{
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML", "XML"]
                    },
                    "GlossSee": "markup"
                }
            }
        }
    }
}
'''

json2 = '''
{
    "glossary": {
        "title": "example glossary",
        "GlossDiv": {
            "title": "S",
            "GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
                    "SortAs": "SGML",
                    "GlossTerm": "Standard Generalized Markup Language",
                    "Acronym": "SGML",
                    "Abbrev": "ISO 8879:1986",
                    "GlossDef": {
                        "para": "A meta-markup language used to create markup languages such as DocBook.",
                        "GlossSeeAlso": ["GML"]
                    },
                    "GlossSee": "markup"
                }
            }
        }
    }
}
'''

# Load JSON objects
obj1 = json.loads(json1)
obj2 = json.loads(json2)

# Perform the deep comparison
diff = DeepDiff(obj1, obj2, ignore_order=True)

# Print the differences
print(json.dumps(diff, indent=4))

