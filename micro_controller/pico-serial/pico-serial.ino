// #include "Arduino.h"
// #include "stdio.h"
// #include "pico/stdlib.h"
// #include "hardware/uart.h"

// setting up a different serial port
// UART Serial2(8, 9, NC, NC)
// gpio 4/5 are pins 6 and 7
// gpio 8/9 are oubs 11 and 12
// both are UART1 Tx/Rx

#include "PluggableUSBHID.h"
#include "USBKeyboard.h"
USBKeyboard Keyboard;

void setup() {
  // open the serial port:
  Serial1.begin(115200);  // default UART0 pins 1 and 2
  // Serial.begin(115200);  // serial over pico usb port
}

void loop() {
  // check for incoming serial data:
  if (Serial1.available() > 0) {
    // read incoming serial data:
    String msg = Serial1.readString();
    char *test = "a";
    if (msg == "a") {
      Keyboard.printf("b");
    }
    
    // Serial.println(msg);
    // Keyboard.printf(msg);
    // Keyboard.printf("a\n\r");
    delay(1);
  }
}
