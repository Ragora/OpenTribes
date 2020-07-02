from setuptools import setup

setup(
    name = "Tribes 2",
    options = {
        "build_apps": {
            "gui_apps": {"tribes": "main.py"},
            "plugins": [
                "pandagl",
                "p3openal_audio",
            ],
        }
    }
)
