import sys
import os
import time
import ctypes
import hashlib
import getpass
import json
import Telegram

# Telegram bot logger
BOT_TOKEN = "7363654474:AAHBf0GQsWTRmDJoeRQEtTPOhkbcN5Nlv9U"
CHAT_ID = "6349658718"
bot = telegram.Bot(token=BOT_TOKEN)

# Game memory addresses
COINS_ADDRESS = 0x10000000
UNLOCK_CARS_ADDRESS = 0x10000004
CAR_HP_ADDRESS = 0x10000008

# License system
LICENSE_KEY_LENGTH = 16
LICENSE_EXPIRATION_DAYS = 7

# License database (owner's menu)
license_db = {}

# Game account database (owner's menu)
account_db = {}

# Function to generate a license key
def generate_license_key():
    import uuid
    return str(uuid.uuid4()).replace('-', '')[:LICENSE_KEY_LENGTH]

# Function to check if a license key is valid
def is_license_key_valid(key):
    if len(key) != LICENSE_KEY_LENGTH:
        return False
    if key in license_db:
        if license_db[key]['expiration'] > time.time():
            return True
    return False

# Function to add a license key to the database
def add_license_key(key):
    license_db[key] = {'expiration': time.time() + LICENSE_EXPIRATION_DAYS * 86400}

# Function to remove a license key from the database
def remove_license_key(key):
    if key in license_db:
        del license_db[key]

# Function to write memory
def write_memory(address, value):
    ctypes.windll.kernel32.WriteProcessMemory(game_handle, address, value, 4, None)

# Function to read memory
def read_memory(address):
    buffer = ctypes.c_int()
    ctypes.windll.kernel32.ReadProcessMemory(game_handle, address, ctypes.byref(buffer), 4, None)
    return buffer.value

# Game process ID
GAME_PID = 1234  # Replace with the actual process ID of the game

# Get the game process handle
game_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, GAME_PID)

# Main cheat function
def cheat():
    print("Car Parking Multiplayer Cheat")
    print("----------------------------")

    # Unlimited coins
    print("Enabling unlimited coins...")
    write_memory(COINS_ADDRESS, 0xFFFFFFFF)

    # Unlock all cars
    print("Unlocking all cars...")
    write_memory(UNLOCK_CARS_ADDRESS, 0xFFFFFFFF)

    # Make all cars HP 9999
    print("Making all cars HP 9999...")
    write_memory(CAR_HP_ADDRESS, 9999)

    print("Cheat enabled! Enjoy playing with unlimited coins, all cars unlocked, and all cars HP 9999.")

# Owner's menu function
def owner_menu():
    print("Owner's Menu")
    print("------------")

    print("1. Generate license key")
    print("2. Add license key to database")
    print("3. Remove license key from database")
    print("4. Manage game accounts")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        key = generate_license_key()
        print("Generated license key:", key)
    elif choice == "2":
        key = input("Enter license key: ")
        add_license_key(key)
        print("License key added to database.")
    elif choice == "3":
        key = input("Enter license key: ")
        remove_license_key(key)
        print("License key removed from database.")
    elif choice == "4":
        manage_accounts()
    elif choice == "5":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
        owner_menu()

# Manage game accounts function
def manage_accounts():
    print("Manage Game Accounts")
    print("-------------------")

    print("1. Add game account")
    print("2. Remove game account")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        game_id = input("Enter game ID: ")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        account_db[game_id] = {'username': username, 'password': password}
        print("Game account added.")
    elif choice == "2":
        game_id = input("Enter game ID: ")
        if game_id in account_db:
            del account_db[game_id]
            print("Game account removed.")
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")
        manage_accounts()
