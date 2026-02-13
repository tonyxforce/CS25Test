#include <Arduino.h>
#include <Adafruit_AS7341.h>
#include <Wire.h>
Adafruit_AS7341 as7341;

#include <Adafruit_AMG88xx.h>

Adafruit_AMG88xx amg;

float pixels[AMG88xx_PIXEL_ARRAY_SIZE];

uint16_t readings[12];

bool ledState = 0;

bool as7341Connected = 0;
bool amg88xxConnected = 0;

void setup()
{
  // communication with the host computer serial monitor
  Serial.begin(115200);

  Wire1.setSDA(2);
  Wire1.setSCL(3);

  while (millis() < 5000)
  {
    Serial.println("Waiting for serial...");
    delay(200);
  }

  Serial.println("Initializing...");

  if (!as7341.begin(57U, &Wire1))
  {
    Serial.println("Could not find AS7341");
  }
  else
  {
    Serial.println("Found AS7341!");
    as7341Connected = true;

    as7341.setATIME(100);
    as7341.setASTEP(999);
    as7341.setGain(AS7341_GAIN_256X);
  }

    if (!amg.begin(105U, &Wire1)) {
        Serial.println("Could not find a valid AMG88xx sensor, check wiring!");
    }else{
        Serial.println("Found AMG88xx sensor!");
        amg88xxConnected = true;
    }
}

unsigned long long lastMillis;

void loop()
{
  if(amg88xxConnected)
  {
    amg.readPixels(pixels);
    Serial.print("|STAR|");
    for (int i = 0; i < AMG88xx_PIXEL_ARRAY_SIZE; i++)
    {
      Serial.print(pixels[i]);
      Serial.print("|");
    }
    Serial.println("END|");
  }

  if (as7341Connected)
  {

    if (Serial.available() > 0)
    {
      Serial.read();
      ledState = !ledState;
      as7341.enableLED(ledState);
    }
    if (as7341.checkReadingProgress())
    {
      as7341.getAllChannels(readings); // Calling this any other time may give you old data

      char buf[128];

      sprintf(buf, "as7341|%06d|%05d|%05d|%05d|%05d|%05d|%05d|%05d|%05d|%05d|%05d|%05d|",
              millis() - lastMillis,
              readings[0],
              readings[1],
              readings[2],
              readings[3],
              readings[4],
              readings[5],
              readings[6],
              readings[7],
              readings[8],
              readings[9],
              readings[10],
              readings[11]);

      Serial.println(buf);
      lastMillis = millis();

      as7341.startReading();
    }
  }
}
