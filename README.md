# OpenTribes

OpenTribes is an open source reimplementation of the game engine for [Tribes 2](https://en.wikipedia.org/wiki/Tribes_2) which uses a pre-1.0 version of the [Torque Game Engine](https://en.wikipedia.org/wiki/Torque_(game_engine)).

The scope of the project is to rebuild Tribes 2 to work appropriately on more modern hardware, improve stability and allow for greater customization of the game. Therefore, the intent
is not to build a general purpose engine as [Unreal Engine](https://www.unrealengine.com/) and friends have this thoroughly covered. This means that lower performance code is probably
acceptable as long as the game runs reasonably well given the scope of a game released in 2001.

## Documentation

Documentation of expected behaviors according to the original game engine will be documented on [the wiki](https://github.com/Ragora/OpenTribes/wiki). Documentation of the
actual implementation on this repository will soon be generated using [sphinx](https://www.sphinx-doc.org).

## Running

When either running main.py directly or a built executable, it will expect a ```--gamedata``` parameter if the executable currently does not reside
in the GameData directory of a working Tribes 2 installation.

## Testing

```bash
python3 setup.py test
```

## Building

```bash
python3 setup.py bdist_apps
```

See https://docs.panda3d.org/1.10/python/distribution/setuptools-examples for more information.
