import json

# To serialize Contact class, it's necessary to get all its attibutes.
# But since 'full_name' is a property, it will not appear in Contact().__dict__.
# To resolve this problem as well as the poor writing 'obj.__dict__' passed to
# dumps we need to provide a helper class derived from 'json.JSONEncoder' that
# overwrite the 'default' method, that need to return the 'obj' dictionary. If
# this class can't handle the obj (isn't 'Contact' class) so
# 'super().default(obj)' will handle this.
class Contact:
    def __init__(self, first, last):
        self.first = first
        self.last = last
        
    @property
    def full_name(self):
        return("{} {}".format(self.first, self.last))
    
    
class ContactEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Contact):
            return {'is_contact': True,
                    'first': obj.first,
                    'last': obj.last,
                    'full': obj.full_name}
        return super().default(obj)

def decode_contact(obj_dictionary):
    if obj_dictionary.get('is_contact'):
        return Contact(obj_dictionary['first'], obj_dictionary['last'])
    return obj_dictionary

c = Contact("John", "Smith")
print(c.full_name)
enc = json.dumps(c, cls=ContactEncoder)
print("Enconding: {}".format(enc))
print(type(enc))

dec = json.loads(enc, object_hook=decode_contact)
print('\nDecoding: {}'.format(dec))
print(type(dec))
print(dec.full_name)
