#include <Arduino.h>

void setup() {
  Serial.begin(9600);
  Serial.println("setup");
}

#define seconds *1000
void loop() {
  delay(3 seconds);
}