py_library(
    name = "tokenizer",
    imports = [
        "."
    ],
    srcs = [
        "tokenizer.py"
    ],
    visibility = ["//visibility:public"]
)

py_library(
    name = "ast",
    imports = [
        "."
    ],
    deps = [
        ":tokenizer"
    ],
    srcs = [
        "tsast.py"
    ],
    visibility = ["//visibility:public"]
)
