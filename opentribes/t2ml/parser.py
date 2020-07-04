import pkg_resources

import lark

def low_level_parse(payload):
    grammar = pkg_resources.resource_string(__name__, "t2ml.lark")
    parser = lark.Lark(grammar.decode("utf-8"))
    return parser.parse(payload)

def low_level_parse_file(path, encoding="utf-8"):
    with open(path, "r") as handle:
        return low_level_parse(payload=handle.read().decode(encoding))
