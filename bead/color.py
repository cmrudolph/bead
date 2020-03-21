import attr


@attr.s(frozen=True)
class Color(object):
    id = attr.ib()
    code = attr.ib(converter=lambda x: x.upper())
    name = attr.ib()
    hex_internal = attr.ib(converter=lambda x: x.lower())
    hex_view = attr.ib(converter=lambda x: x.lower())
    hex_edge = attr.ib(converter=lambda x: x.lower())
