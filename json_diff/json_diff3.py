import json

def json_diff(json1, json2):
    diff = []

    def compare_dicts(d1, d2, path=""):
        for key in d1.keys():
            new_path = f"{path}/{key}" if path else key
            if key not in d2:
                diff.append(f"- {new_path}: {d1[key]}")
            elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
                compare_dicts(d1[key], d2[key], new_path)
            elif d1[key] != d2[key]:
                diff.append(f"- {new_path}: {d1[key]}")
                diff.append(f"+ {new_path}: {d2[key]}")
        
        for key in d2.keys():
            new_path = f"{path}/{key}" if path else key
            if key not in d1:
                diff.append(f"+ {new_path}: {d2[key]}")

    compare_dicts(json1, json2)
    return diff

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

# Perform the comparison
differences = json_diff(obj1, obj2)

# Print the differences
for line in differences:
    print(line)

