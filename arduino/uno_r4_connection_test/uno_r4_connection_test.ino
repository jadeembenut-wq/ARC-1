const int ledPin = LED_BUILTIN;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  Serial.println("ARC-1 Arduino connection started.");
}

void loop() {
  digitalWrite(ledPin, HIGH);
  Serial.println("LED ON");
  delay(1000);

  digitalWrite(ledPin, LOW);
  Serial.println("LED OFF");
  delay(1000);}

