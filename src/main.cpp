#include <Arduino.h>
#include <build_infos.h> // will be created while building the project

void setup() {
  Serial.begin(9600);
  Serial.printf(
    "(VERSION:%s) (SHA:%s) (DATE:%s)\n",
    Build.getGitVersion(),
    Build.getGitHash(),
    Build.getBuildTime()
  );
}

#define seconds *1000
void loop() {
  delay(3 seconds);
}