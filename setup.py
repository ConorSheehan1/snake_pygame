from cx_Freeze import setup, Executable

base = None


executables = [Executable("snake_game.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "snake_game",
    options = options,
    version = "1.0",
    description = 'basic snake game built using pygame',
    executables = executables
)