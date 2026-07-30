const int hallPin = A0;

const float maximumReading = 4095.0;
const float supplyVoltage = 5.0;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);

  delay(2000);  // Gives you time to position the magnet

  Serial.println("sample,raw_reading,voltage");

  for (int sample = 1; sample <= 10; sample++) {
    int rawReading = analogRead(hallPin);

    float sensorVoltage =
        rawReading * supplyVoltage / maximumReading;

    Serial.print(sample);
    Serial.print(",");
    Serial.print(rawReading);
    Serial.print(",");
    Serial.println(sensorVoltage, 4);

    delay(1000);  // One reading every second
  }

  Serial.println("Finished 10 readings.");
}

void loop() {
  // Nothing repeats automatically
}