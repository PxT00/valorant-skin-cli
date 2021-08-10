from InquirerPy.utils import color_print
import ctypes,os,traceback

from src.startup import Startup
from src.utility.config_manager import default_config

kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')
hWnd = kernel32.GetConsoleWindow()

# TODO:
# - launch with valorant
# - detect new releases on github
# - clarify some prompts

# TODO LATER:
# - loadouts


if __name__ == "__main__":
    color_print([("Tomato", f''' _   _____   __   ____  ___  ___   _  ________        __    _              ___    
| | / / _ | / /  / __ \/ _ \/ _ | / |/ /_  __/______ / /__ (_)__  ________/ (_)   
| |/ / __ |/ /__/ /_/ / , _/ __ |/    / / / /___(_-</  '_// / _ \/___/ __/ / /    
|___/_/ |_/____/\____/_/|_/_/ |_/_/|_/ /_/     /___/_/\_\/_/_//_/    \__/_/_/'''),("White",f"{default_config['version']}\n")])
    
    try:
        Startup.run()
    except:
        user32.ShowWindow(hWnd, 1)
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x40|0x100))
        color_print([("Red bold","OOPS! O programa encontrou um erro, crie um Issue com o traceback abaixo!")])
        traceback.print_exc()
        input("pressione Enter para sair...")
        os._exit(1)
