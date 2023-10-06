# import sys
import smbus2 as smbus
import time

arduino_address = 11


def send_i2c_msg(message: str):
    I2Cbus = smbus.SMBus(1)
    data_to_send = message.encode("utf-8")
    I2Cbus.write_i2c_block_data(arduino_address, 0, data_to_send)
    time.sleep(0.5)


if __name__ == "__main__":
    send_i2c_msg("test")
