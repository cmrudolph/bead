class BeadColor:
    def __init__(self, id, code, name, hex_value):
        self._id = id
        self._code = code.upper()
        self._name = name
        self._hex_value = hex_value.lower()

    def __repr__(self):
        return (f"BeadColor('{self._id}', '{self.code}', '{self.name}', "
                f"'{self.hex_value}')")

    @property
    def id(self):
        return self._id

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name

    @property
    def hex_value(self):
        return self._hex_value

    def is_white(self):
        return self._code == 'WHT'
