from lark import Lark

parser = Lark.open("t2ml.lark")

with open("draakan.txt", "r") as handle:
    test_load = handle.read()

#print(test_load)

tree = parser.parse(test_load)
print(tree)
