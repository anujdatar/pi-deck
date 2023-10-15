/* **************************************************************************
 *  USB StreamDeck using Pi ZW, Arduino Pro Micro and a 7" touchscreen
 *  (c) 2023 Anuj Datar <anuj.datar@gmail.com>
 **************************************************************************** */
#include "Wire.h"
#include "Media_Keyboard.h"

void setup() {
  Wire.begin(11);
  Wire.onReceive(receiveData);

  // Serial1.begin(115200);
  Serial.begin(115200);

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

  Serial.println(receivedData);

  if (receivedData == "v+") {
    Media_Keyboard.write(KEY_VOLUME_UP);
  } else if (receivedData == "v-") {
    Media_Keyboard.write(KEY_VOLUME_DOWN);
  } else if (receivedData == "mute") {
    Media_Keyboard.write(KEY_MUTE);
  } else if (receivedData == "pause") {
    Media_Keyboard.write(KEY_PLAY_PAUSE);
  } else if (receivedData == "stop") {
    Media_Keyboard.write(KEY_STOP);
  } else if (receivedData == "next") {
    Media_Keyboard.write(KEY_NEXT_TRACK);
  } else if (receivedData == "prev") {
    Media_Keyboard.write(KEY_PREVIOUS_TRACK);
  } else {
    for (int i = 0; i < receivedData.length(); i++) {
      char currentChar = receivedData.charAt(i);
      Media_Keyboard.write(currentChar);
    }
  }
}
