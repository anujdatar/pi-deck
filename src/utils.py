import subprocess
from typing import List
import ujson as json
from src import Key, KeymapTab
import serial

try:
    import smbus
except ImportError:
    import smbus2 as smbus

# import time


def print_command(a: str) -> None:
    print(f"commend: {a}")


def reboot():
    subprocess.run(
        ["systemctl", "reboot"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def shutdown():
    subprocess.run(
        ["systemctl", "poweroff"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def keymap_json_loader(file_path: str = "keymap.json") -> List[KeymapTab]:
    with open(file_path, "r") as keymap_file:
        json_data = json.load(keymap_file)

    tabs: List[KeymapTab] = []
    for tab_data in json_data:
        keys = [Key(**key_data) for key_data in tab_data["keymap"]]
        tabs.append(
            KeymapTab(
                title=tab_data["title"],
                description=tab_data["description"],
                packing=tab_data["packing"],
                keymap=keys,
            )
        )

    # tabs = [KeymapTab(**keymap_tab) for keymap_tab in json_data]
    return tabs


def send_serial_msg(msg: str) -> None:
    ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
    ser.write(msg.encode())
    ser.close()


def send_i2c_msg(message: str):
    arduino_address = 11
    I2Cbus = smbus.SMBus(1)
    data_to_send = message.encode("utf-8")
    I2Cbus.write_i2c_block_data(arduino_address, 0, list(data_to_send))
    # time.sleep(0.1)

    # data_to_send = [ord(char) for char in message]
    # I2Cbus.write_i2c_block_data(arduino_address, 0, data_to_send)
