void setup() {
  Serial.begin(31250);
  pinMode(A0, INPUT);
}

void loop() {
  Serial.print(millis());
  Serial.print(" ");
  Serial.println(analogRead(A0));
}
