# OpenTribes

![Python Package](https://github.com/Ragora/OpenTribes/workflows/Python%20package/badge.svg)

OpenTribes is an open source reimplementation of the game engine for [Tribes 2](https://en.wikipedia.org/wiki/Tribes_2) which uses a pre-1.0 version of the [Torque Game Engine](https://en.wikipedia.org/wiki/Torque_(game_engine)).

The scope of the project is to rebuild Tribes 2 to work appropriately on more modern hardware, improve stability and allow for greater customization of the game. Therefore, the intent
is not to build a general purpose engine as [Unreal Engine](https://www.unrealengine.com/) and friends have this thoroughly covered. This means that lower performance code is probably
acceptable as long as the game runs reasonably well given the scope of a game released in 2001.

## Documentation

Documentation of expected behaviors according to the original game engine will be documented on [the wiki](https://github.com/Ragora/OpenTribes/wiki). Documentation of the
actual implementation on this repository will soon be generated using [sphinx](https://www.sphinx-doc.org).

## Running

Running Tribes 2 with this engine will look a lot like shortcuts to run the original software, however, with some key differences:

```bash
python3 main.py --gamedata /path/to/your/GameData/dir --mod Classic
```

Or with a built distribution:

```bash
./tribes --gamedata /path/to/your/GameData/dir --mod Classic
```

Note the presence of the ```--gamedata``` parameter which is used to tell the code where the installation directory of your game is.

Currently the only original command line flag that is supported is ```--mod``` but in the future the launcher will attempt to mimic the original command like arguments fully.

## Testing

To execute unit tests (used to ensure the programming is working as intended), you run the setup.py script with ```test``` as the parameter:

```bash
python3 setup.py test
```

## Building

```bash
python3 setup.py bdist_apps
```

See https://docs.panda3d.org/1.10/python/distribution/setuptools-examples for more information.
