import machine

uart = machine.UART(0, baudrate=115200)

while True:
    if uart.any():
        data = uart.read().decode('utf-8')
        if '\n' in data:
            data = data.strip('\n')
        print(data)
