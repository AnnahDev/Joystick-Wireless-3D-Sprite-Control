#include <SoftwareSerial.h>

// Bluetooth module pins
#define BT_RX 11  // Connect to TX of HC-05
#define BT_TX 10  // Connect to RX of HC-05

// Joystick pins
#define JOY_X A0
#define JOY_Y A1
#define JOY_BTN 2

// Button pins
#define JUMP_BTN 3
#define WAVE_BTN 4
#define DANCE_BTN 5

// Create software serial for Bluetooth
SoftwareSerial BTSerial(BT_RX, BT_TX);

// Button state tracking
bool joyBtnLastState = HIGH;
unsigned long lastCommandTime = 0;

void setup() {
  // Initialize serial communications
  Serial.begin(9600);
  BTSerial.begin(38400);  // HC-05 default baud rate
  
  // Configure button pins with internal pull-up resistors
  pinMode(JOY_BTN, INPUT_PULLUP);
  pinMode(JUMP_BTN, INPUT_PULLUP);
  pinMode(WAVE_BTN, INPUT_PULLUP);
  pinMode(DANCE_BTN, INPUT_PULLUP);
  
  // LED indicator
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("Joystick Controller Ready");
}

void loop() {
  // Read joystick values
  int xValue = analogRead(JOY_X);
  int yValue = analogRead(JOY_Y);
  int joyBtn = digitalRead(JOY_BTN);
  int jumpBtn = digitalRead(JUMP_BTN);
  int waveBtn = digitalRead(WAVE_BTN);
  int danceBtn = digitalRead(DANCE_BTN);
  
  // Map values to 0-1023 range (in case your joystick is different)
  xValue = constrain(xValue, 0, 1023);
  yValue = constrain(yValue, 0, 1023);
  
  // Send data in format: "x,y,btn1,btn2,btn3,btn4"
  // btn1 = joystick button, btn2 = jump, btn3 = wave, btn4 = dance
  String data = String(xValue) + "," + 
                String(yValue) + "," + 
                String(!joyBtn) + "," +  // Invert button state (pull-up)
                String(!jumpBtn) + "," + 
                String(!waveBtn) + "," + 
                String(!danceBtn);
  
  BTSerial.println(data);
  
  // Optional: Print to Serial Monitor for debugging
  Serial.println(data);
  
  // Small delay to prevent overwhelming the system
  delay(50);
}
