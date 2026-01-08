// ESP32 Potentiometer Reader for ROS2
// Pin D33 connected to potentiometer center pin
// 3.3V and GND to pot outer pins

const int POT_PIN = 34;
const int BAUD_RATE = 115200;
const int READ_DELAY = 50; // 20Hz update rate

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(POT_PIN, INPUT);
  
  // Wait for serial connection
  while (!Serial) {
    delay(10);
  }
  
  Serial.println("ESP32 Potentiometer Ready");
}

void loop() {
  // Read analog value (0-4095 for ESP32 12-bit ADC)
  int potValue = analogRead(POT_PIN);
  
  // Send value over serial
  Serial.println(potValue);
  
  delay(READ_DELAY);
}