#include <Servo.h>

Servo hazardServo;

int currentState = 1;         // Default state (safe)
int lastServoPosition = 25;   // Default servo position

// Define LED pins
const int greenLED = 2; 
const int whiteLED = 5;
const int redLED = 3;
const int blinkLED = 6;

// Push button setup
const int buttonPin = 7; // Push button on D7
const int ledPin = 3;    // LED to glow when button pressed (blinkLED)

unsigned long buttonPressTime = 0;
bool buttonPressed = false;
bool sosActivated = false;  // Flag to track SOS activation
bool buttonClickedRapidly = false;
unsigned long lastButtonClickTime = 0;

void setup() {
  Serial.begin(9600);       
  hazardServo.attach(9);    
  hazardServo.write(lastServoPosition);  

  pinMode(greenLED, OUTPUT);
  pinMode(whiteLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(blinkLED, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // Use internal pull-up resistor
  pinMode(ledPin, OUTPUT);          // LED pin for SOS indication
}

void loop() {
  // Read button state
  bool buttonState = (digitalRead(buttonPin) == LOW); // True when pressed

  if (buttonState && !buttonPressed) {
    // Button just pressed
    buttonPressTime = millis(); // Start counting time
    buttonPressed = true;
  }

  // Check if the button was pressed for 3 seconds
  if (buttonPressed && (millis() - buttonPressTime >= 3000) && !sosActivated) {
    digitalWrite(ledPin, HIGH); // Turn ON the LED (SOS activated)
    sosActivated = true;        // Set SOS flag
    Serial.println(-1);         // Send -1 to Python for SOS Activated
  }

  // Handle rapid double-click for deactivating SOS
  if (buttonState && !buttonClickedRapidly) {
    if (millis() - lastButtonClickTime < 500) {
      // Button pressed again within 500ms (rapid click)
      if (sosActivated) {
        sosActivated = false;
        digitalWrite(ledPin, LOW);  // Turn OFF LED (SOS deactivated)
        Serial.println(-2);         // Send -2 to Python for SOS Deactivated
      }
      buttonClickedRapidly = true;
    }
    lastButtonClickTime = millis();
  }

  if (!buttonState) {
    buttonClickedRapidly = false; // Reset on button release
    buttonPressed = false;        // Reset button press detection
  }

  // Check Serial for state change (other commands from Python)
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int received = input.toInt();

    if (received != currentState) {
      currentState = received;

      if (currentState == 3) {
        hazardServo.write(0); 
        lastServoPosition = 0;

        digitalWrite(redLED, HIGH);
        digitalWrite(greenLED, LOW);
        digitalWrite(whiteLED, LOW);
      } 
      else if (currentState == 1) {
        hazardServo.write(90); 
        lastServoPosition = 90;

        digitalWrite(greenLED, HIGH);
        digitalWrite(whiteLED, LOW);
        digitalWrite(redLED, LOW);
      }
      else if (currentState == 2) {
        hazardServo.write(90); 
        lastServoPosition = 90;

        digitalWrite(whiteLED, HIGH);
        digitalWrite(greenLED, LOW);
        digitalWrite(redLED, LOW);
      }
    }
  }
}
