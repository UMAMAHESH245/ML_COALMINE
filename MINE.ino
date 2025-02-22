/*
  ML-Based Coal Mine Monitoring in IoT Network
  Reads sensor data from flame, smoke, and humidity sensors and sends it via Serial.
  - Flame sensor connected to A0
  - Smoke sensor connected to A1
  - Humidity sensor connected to A2
*/

const int flamePin = A0;
const int smokePin = A1;
const int humidityPin = A2;

void setup() {
  Serial.begin(9600);
  // Wait for serial connection
  delay(2000);
  Serial.println("flame,smoke,humidity");  // Print header for clarity
}

void loop() {
  int flameValue = analogRead(flamePin);
  int smokeValue = analogRead(smokePin);
  int humidityValue = analogRead(humidityPin);

  // Send data in CSV format: flame,smoke,humidity
  Serial.print(flameValue);
  Serial.print(",");
  Serial.print(smokeValue);
  Serial.print(",");
  Serial.println(humidityValue);

  delay(1000); // Read sensors every 1 second
}
