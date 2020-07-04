from setuptools import setup, find_namespace_packages

setup(
    name = "OpenTribes",
    version = "0.1",

    packages = find_namespace_packages(
        exclude = [
            "*.tests",
            "*.tests.*",
            "tests.*",
            "tests"
        ]
    ),

    options = {
        "build_apps": {
            "gui_apps": {
                "tribes": "main.py" # We don't use 'opentribes' here because it can conflict with the build
            },
            "plugins": [
                "pandagl",
                "p3openal_audio",
            ],
            "include_patterns": [
                # Include all lark definitions in the base application
                "opentribes/**/*.lark",
            ]
        }
    },

    test_suite = "nose.collector",
    tests_require = ["nose"],
)
