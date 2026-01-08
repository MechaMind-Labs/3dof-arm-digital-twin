// ESP32 4-Potentiometer Reader for ROS2
// d33 - pot_1 (joint_1)
// d32 - pot_2 (joint_2)
// d35 - pot_3 (joint_3)
// d34 - pot_4 (gripper/joint_4)

const int POT_1 = 33;
const int POT_2 = 32;
const int POT_3 = 35;
const int POT_4 = 34;

const int BAUD_RATE = 115200;
const int READ_DELAY = 10;

// Moving average filter
const int FILTER_SIZE = 20;
int readings_1[FILTER_SIZE];
int readings_2[FILTER_SIZE];
int readings_3[FILTER_SIZE];
int readings_4[FILTER_SIZE];

int readIndex = 0;
int total_1 = 0;
int total_2 = 0;
int total_3 = 0;
int total_4 = 0;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(POT_1, INPUT);
  pinMode(POT_2, INPUT);
  pinMode(POT_3, INPUT);
  pinMode(POT_4, INPUT);
  
  // Initialize filter arrays
  for (int i = 0; i < FILTER_SIZE; i++) {
    readings_1[i] = 0;
    readings_2[i] = 0;
    readings_3[i] = 0;
    readings_4[i] = 0;
  }
  
  Serial.println("ESP32 4-Pot Ready");
}

void loop() {
  // Read all potentiometers
  int raw_1 = analogRead(POT_1);
  int raw_2 = analogRead(POT_2);
  int raw_3 = analogRead(POT_3);
  int raw_4 = analogRead(POT_4);
  
  // Apply moving average filter for pot_1
  total_1 = total_1 - readings_1[readIndex];
  readings_1[readIndex] = raw_1;
  total_1 = total_1 + readings_1[readIndex];
  
  // Apply moving average filter for pot_2
  total_2 = total_2 - readings_2[readIndex];
  readings_2[readIndex] = raw_2;
  total_2 = total_2 + readings_2[readIndex];
  
  // Apply moving average filter for pot_3
  total_3 = total_3 - readings_3[readIndex];
  readings_3[readIndex] = raw_3;
  total_3 = total_3 + readings_3[readIndex];
  
  // Apply moving average filter for pot_4
  total_4 = total_4 - readings_4[readIndex];
  readings_4[readIndex] = raw_4;
  total_4 = total_4 + readings_4[readIndex];
  
  readIndex = (readIndex + 1) % FILTER_SIZE;
  
  // Calculate filtered values
  int filtered_1 = total_1 / FILTER_SIZE;
  int filtered_2 = total_2 / FILTER_SIZE;
  int filtered_3 = total_3 / FILTER_SIZE;
  int filtered_4 = total_4 / FILTER_SIZE;
  
  // Send as comma-separated values
  Serial.print(filtered_1);
  Serial.print(",");
  Serial.print(filtered_2);
  Serial.print(",");
  Serial.print(filtered_3);
  Serial.print(",");
  Serial.println(filtered_4);
  
  delay(READ_DELAY);
}
