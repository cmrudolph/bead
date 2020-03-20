import attr


@attr.s(frozen=True)
class Color(object):
    id = attr.ib()
    code = attr.ib(converter=lambda x: x.upper())
    name = attr.ib()
    hex_value = attr.ib(converter=lambda x: x.lower())

    def is_white(self):
        return self.code == 'WHT'
