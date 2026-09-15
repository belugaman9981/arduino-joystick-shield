const int JOY_X = A0;
const int JOY_Y = A1;

const int BUTTON_A = 2;
const int BUTTON_B = 3;
const int BUTTON_C = 4;
const int BUTTON_D = 5;
const int BUTTON_E = 6;
const int JOY_BUTTON = 7;

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);
  pinMode(BUTTON_D, INPUT_PULLUP);
  pinMode(BUTTON_E, INPUT_PULLUP);
  pinMode(JOY_BUTTON, INPUT_PULLUP);
}

void loop() {
  int x = analogRead(JOY_X);
  int y = analogRead(JOY_Y);

  Serial.print(x);
  Serial.print(",");
  Serial.print(y);
  Serial.print(",");
  Serial.print(!digitalRead(BUTTON_A));
  Serial.print(",");
  Serial.print(!digitalRead(BUTTON_B));
  Serial.print(",");
  Serial.print(!digitalRead(BUTTON_C));
  Serial.print(",");
  Serial.print(!digitalRead(BUTTON_D));
  Serial.print(",");
  Serial.print(!digitalRead(BUTTON_E));
  Serial.print(",");
  Serial.println(!digitalRead(JOY_BUTTON));

  delay(15);
}