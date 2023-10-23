/* **************************************************************************
 *  USB StreamDeck using Pi ZW, Arduino Pro Micro and a 7" touchscreen
 *  (c) 2023 Anuj Datar <anuj.datar@gmail.com>
 **************************************************************************** */
#include "Wire.h"
#include "Media_Keyboard.h"

void setup() {
  Wire.begin(11);
  Wire.onReceive(receiveData);

  // Serial.begin(115200);

  Media_Keyboard.begin();
}

void loop() {}

void receiveData(int bytecount) {
  String receivedData = "";
  while (Wire.available()) {
    char c = Wire.read();
    receivedData += c;
  }

  // receivedData.trim();
  // receivedData.replace("\0", "");
  receivedData.remove(0,1);

  // Serial.println(receivedData);

  if (receivedData == "v+") {
    Media_Keyboard.write(KEY_VOLUME_UP);
  } else if (receivedData == "v-") {
    Media_Keyboard.write(KEY_VOLUME_DOWN);
  } else if (receivedData == "mt") {
    Media_Keyboard.write(KEY_MUTE);
  } else if (receivedData == "pp") {
    Media_Keyboard.write(KEY_PLAY_PAUSE);
  } else if (receivedData == "st") {
    Media_Keyboard.write(KEY_STOP);
  } else if (receivedData == "t+") {
    Media_Keyboard.write(KEY_NEXT_TRACK);
  } else if (receivedData == "t-") {
    Media_Keyboard.write(KEY_PREVIOUS_TRACK);
  } else {
    for (int i = 0; i < receivedData.length(); i++) {
      char currentChar = receivedData.charAt(i);
      Media_Keyboard.write(currentChar);
    }
    Media_keyboard(KEY_ESC);
    Media_keyboard(KEY_ESC);
  }
}

