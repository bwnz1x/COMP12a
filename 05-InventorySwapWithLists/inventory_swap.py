# Inventory Swap
# Ben Phan
# Feb 6
import time
from operator import index
import os
# Hot Key Binder for League of Legend
'''
ALGORITHM: Inventory Swap

Display welcome message
Get input for each control

while true
    ask if they are happy with the control
    if user are happy with control:
        break out of the loop and end program
    else:
        ask what control to change 
        ask the keybind for the specific control
        change the keybind
        coutinue looping
'''

# Variables
player_keybind = []
controls = ["skill 1", "skill 2", "skill 3", "ultimate", "summoner Spell 1", "summoner Spell 2", "recall"]

def instructions():
    """ Display the welcome message for the program"""
    print("Welcome to the Keybindings program for League Of Legends")
    print("You can edit these controls:")
    for i in range(len(controls)):
        print(controls[i])


def get_keybind():
    """Get the keybinds for specific control, add to player_keybind list"""
    for i in range(len(controls)):
        while True: # loop check for input
            key = input("Please input the keys you want for " + controls[i] + ": ")
            if len(key) == 1: # only accepting 1 character
                break
            elif len(key) == 0:
                print("You have to input at least one key")
            else:
                print("Please only input a single character")
        player_keybind.append(key)
    os.system('cls' if os.name == 'nt' else 'clear')
    confirmation()


def confirmation():
    """Check if the user are happy with their current keybind, else forward to find_item()"""

    print("Here is your current keybind: ")
    for i in range(len(controls)):
        print(controls[i] + ": " + player_keybind[i])

    while True:
        confirm = confirmation_check()
        if confirm is True:
            print("Keybinds are set. Happy Playing!")
            exit()
        elif confirm is False:
            while True:
                key_change = input("What control do you want to change: ")
                if key_change in controls:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    find_control(key_change)
                    break


def confirmation_check():
    """confirmation returning  Yes(and similar) with True, and No(and similar) with False"""
    while True:
        ans = input("Are you happy with your keybinds? (Y/N)")
        if ans == "Y" or ans == "y" or ans == "YES" or ans == "yes":
            return True
        elif ans == "N" or ans == "n" or ans == "NO" or ans == "no":
            return False
        else:
            print("Sorry, I didn't understand that.")


def find_control(skill):
    """Find the index of the skill in controls list"""
    index_of_control = controls.index(skill)

    while True:
        keyinput = input("Please input the keys you want for " + controls[index_of_control] + ": ")
        if len(keyinput) == 1:
            break
        elif len(keyinput) == 0:
            print("You have to input at least one key")
        else:
            print("Please only input a single character")
    os.system('cls' if os.name == 'nt' else 'clear')
    swap_control(index_of_control, keyinput)


def swap_control(index_of_control, key):
    player_keybind[index_of_control] = key
    confirmation()


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    instructions()
    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear')
    get_keybind()

main()