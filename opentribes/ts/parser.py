from lark import Lark

with open("torque.lark", "r") as handle:
    payload = handle.read()

parser = Lark(payload)

with open("function.cs", "r") as handle:
    test_load = handle.read()

print(test_load)
print(parser.parse(test_load))
