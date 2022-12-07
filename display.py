import colorama
from colorama import Fore, Back, Style
import minesweeper as mine
import os
import sys
import time
import ctypes
import re

black = Fore.BLACK
red = Fore.LIGHTRED_EX
green = Fore.GREEN
white = Fore.WHITE
bright = Style.BRIGHT
dim = Style.DIM
normal = Style.NORMAL
reset = Fore.RESET

size2 = []

logo = f"""
{green}
███╗░░░███╗██╗███╗░░██╗███████╗░██████╗░██╗░░░░░░░██╗███████╗███████╗██████╗░███████╗██████╗░\n████╗░████║██║████╗░██║██╔════╝██╔════╝░██║░░██╗░░██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗\n██╔████╔██║██║██╔██╗██║█████╗░░╚█████╗░░╚██╗████╗██╔╝█████╗░░█████╗░░██████╔╝█████╗░░██████╔╝\n██║╚██╔╝██║██║██║╚████║██╔══╝░░░╚═══██╗░░████╔═████║░██╔══╝░░██╔══╝░░██╔═══╝░██╔══╝░░██╔══██╗\n██║░╚═╝░██║██║██║░╚███║███████╗██████╔╝░░╚██╔╝░╚██╔╝░███████╗███████╗██║░░░░░███████╗██║░░██║\n╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝
{reset}"""

def print_slow(str, delay):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)

# Returns size of field
def begin() -> int:
  difficulty_selection()
  menu_choice = input(f"[{red}>{reset}] ")
  
  if menu_choice == "1":
    os.system("clear")
    return mine.DIFFICULTY['easy']
  elif menu_choice == "2":
    os.system("clear")
    return mine.DIFFICULTY['normal']
  elif menu_choice == "3" :
    os.system("clear")
    return mine.DIFFICULTY['hard']
  elif menu_choice == "4":
    print()
    print_slow("Created By: Om, Carmel, Lior, Theo, & Liam", 0.1)
    time.sleep(3)
    os.system("clear")
    end_game()
  elif menu_choice == "5":
    end_game()

def end_game():
  os.system("clear")
  print_slow("Thanks For Playing!", 0.1)
  time.sleep(1)
  os.system("clear")


def difficulty_selection():
  print(logo)
  print("Select Difficulty:")
  print(f"""
    [{red}1{reset}] Easy
    [{red}2{reset}] Normal
    [{red}3{reset}] Hard
    [{red}4{reset}] Credits
    [{red}5{reset}] Exit
  """)

SYM_COLOR = {
  '0': Fore.BLACK,
  '1': Fore.BLUE,
  '2': Fore.GREEN,
  '3': Fore.RED,
  '4': Fore.LIGHTBLUE_EX,
  '5': Fore.YELLOW,
  '6': Fore.CYAN,
  '7': Fore.LIGHTMAGENTA_EX,
  '8': Fore.MAGENTA,
  '⚑': Fore.RED
}