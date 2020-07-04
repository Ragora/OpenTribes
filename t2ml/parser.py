import lark

parser = lark.Lark.open("t2ml.lark")

with open("draakan.txt", "r") as handle:
    test_load = handle.read()

tree = parser.parse(test_load)
print(tree.pretty())
