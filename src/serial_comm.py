import serial


def send_serial_msg(msg: str) -> None:
    # Create a serial Connection
    ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)
    ser.write(msg.encode())
    ser.close()
