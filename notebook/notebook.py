import datetime


class Note:
    _last_id = 0

    def __init__(self, memo, tags=''):
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        self.__class__.increment_id()
        self.id = self.__class__._last_id

    def match(self, keyword):
        return keyword in self.memo or keyword in self.tags

    @classmethod
    def increment_id(cls):
        cls._last_id += 1


class Notebook:
    def __init__(self):
        self.notes = []

    def new_note(self, memo, tags=''):
        self.notes.append(Note(memo, tags))

    def _find_note(self, note_id):
        for note in self.notes:
            if str(note.id) == str(note_id):
                return note
        return None

    def modify_memo(self, note_id, memo):
        note = self._find_note(note_id)
        if not note:
            raise ValueError('ID does not exist')
        note.memo = memo

    def modify_tags(self, note_id, tags):
        note = self._find_note(note_id)
        if not note:
            raise ValueError('ID does not exist')
        note.tags = tags

    def search(self, keyword):
        return [note for note in self.notes if note.match(keyword)]
