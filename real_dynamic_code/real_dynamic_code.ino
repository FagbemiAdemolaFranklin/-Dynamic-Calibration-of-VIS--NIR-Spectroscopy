

#define SPEC_TRG         A0
#define SPEC_ST          A1
#define SPEC_CLK         A2
#define SPEC_VIDEO       A3
#define WHITE_LED        A4
#define LASER_404        A5

#define SPEC_CHANNELS    288
uint16_t data[SPEC_CHANNELS];

const int delayTime = 1;  // µs delay for clock timing

const int PIXEL_START = 4;
const int PIXEL_END = 283;

const int MIN_THRESHOLD = 250;
const int MAX_THRESHOLD = 900;

// Integration time in microseconds
unsigned long integrationTime_us = 500000;
const unsigned long MIN_INTEGRATION_US = 10;
const unsigned long MAX_INTEGRATION_US = 1000000;

void setup() {
  pinMode(SPEC_CLK, OUTPUT);
  pinMode(SPEC_ST, OUTPUT);
  pinMode(WHITE_LED, OUTPUT);

  digitalWrite(SPEC_CLK, HIGH);
  digitalWrite(SPEC_ST, LOW);
  digitalWrite(WHITE_LED, LOW);

  Serial.begin(115200);
  while (!Serial);
  Serial.println("Ready. Send 's' to auto capture.");
}

void readSpectrometer(unsigned long integrationTime) {
  // Start integration sequence
  digitalWrite(SPEC_CLK, LOW);
  digitalWrite(SPEC_ST, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(SPEC_CLK, LOW);

  // Drop ST LOW to begin integration
  digitalWrite(SPEC_ST, LOW);

  // Wait for integration period
  delayMicroseconds(integrationTime);

  // Dummy clocks (87 recommended for integration end and setup)
  for (int i = 0; i < 87; i++) {
    digitalWrite(SPEC_CLK, HIGH); delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW); delayMicroseconds(delayTime);
  }

  // Read actual pixel data
  for (int i = 0; i < SPEC_CHANNELS; i++) {
    data[i] = analogRead(SPEC_VIDEO);
    digitalWrite(SPEC_CLK, HIGH); delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW); delayMicroseconds(delayTime);
  }

  // Post read dummy clocks
  digitalWrite(SPEC_ST, HIGH);
  for (int i = 0; i < 7; i++) {
    digitalWrite(SPEC_CLK, HIGH); delayMicroseconds(delayTime);
    digitalWrite(SPEC_CLK, LOW); delayMicroseconds(delayTime);
  }

  digitalWrite(SPEC_CLK, HIGH); delayMicroseconds(delayTime);
}

int findMaxPixel(int fromPixel, int toPixel) {
  int maxValue = 0;
  for (int i = fromPixel; i <= toPixel; i++) {
    if (data[i] > maxValue) maxValue = data[i];
  }
  return maxValue;
}

void printData() {
  for (int i = 0; i < SPEC_CHANNELS; i++) {
    Serial.print(data[i]);
    if (i < SPEC_CHANNELS - 1)
      Serial.print(",");
  }
  Serial.println();
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "s") {
      int maxPixel;
      int attempts = 0;

      while (attempts < 20) {
        readSpectrometer(integrationTime_us);
        maxPixel = findMaxPixel(PIXEL_START, PIXEL_END);

        Serial.print("Integration Time (µs): ");
        Serial.print(integrationTime_us);
        Serial.print(" | Max Pixel: ");
        Serial.println(maxPixel);

        // Adjust integration time
        if (maxPixel > MAX_THRESHOLD) {
          integrationTime_us = integrationTime_us / 2;
          if (integrationTime_us < MIN_INTEGRATION_US) integrationTime_us = MIN_INTEGRATION_US;
        } else if (maxPixel < MIN_THRESHOLD) {
          integrationTime_us = integrationTime_us * 2;
          if (integrationTime_us > MAX_INTEGRATION_US) integrationTime_us = MAX_INTEGRATION_US;
        } else {
          break;  // Within acceptable range
        }

        attempts++;
      }

      // Final read and print
      readSpectrometer(integrationTime_us);
      printData();

      Serial.print("✅ Final Integration Time (µs): ");
      Serial.print(integrationTime_us);
      Serial.print(" | Final Max Pixel: ");
      Serial.println(findMaxPixel(PIXEL_START, PIXEL_END));
    }
  }
}
