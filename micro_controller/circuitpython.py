import board
import busio

uart = busio.UART(board.GP0, board.GP1, baudrate=9600)

while True:
    data=uart.read()
    
    if data is not None:
        print(data)