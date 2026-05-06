#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

SoftwareSerial ss(3, 2); 
TinyGPSPlus gps;
Adafruit_MPU6050 mpu;

void sendBinary(float val) {
  byte* b = (byte*)&val;
  Serial.write(b, 4);
}

void setup() {
  Serial.begin(115200);
  ss.begin(9600); 

  if (!mpu.begin()) {
    Serial.println("Error");
  } else {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }
}

void loop() {
  unsigned long t = millis();
  while (ss.available() > 0 && (millis() - t < 10)) {
    gps.encode(ss.read());
  }

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  sendBinary(a.acceleration.x);
  sendBinary(a.acceleration.y);
  sendBinary(a.acceleration.z);

  if (gps.location.isValid() && gps.location.age() < 2000) {
    sendBinary((float)gps.location.lat());
    sendBinary((float)gps.location.lng());
    sendBinary((float)gps.altitude.meters());
  } else {
    sendBinary(0.0);
    sendBinary(0.0);
    sendBinary(0.0);
  }

  Serial.write('\n'); 
  delay(100); 
}
