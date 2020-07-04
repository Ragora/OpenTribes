from setuptools import setup, find_namespace_packages

setup(
    name = "Tribes 2",
    version = "0.1",

    packages = find_namespace_packages(),

    package_data = {
        # Ensure all lark & payload files are included
        "": ["*.lark", "*.txt"]
    },

    test_suite="nose.collector",
    tests_require=["nose"],
)


"""
options = {
    "build_apps": {
        "gui_apps": {"tribes": "opentribes"},
        "plugins": [
            "pandagl",
            "p3openal_audio",
        ],
    }
},
"""
