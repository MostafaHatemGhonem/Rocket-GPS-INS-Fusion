#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;
unsigned long lastTime = 0;
float velocityZ = 0;
float positionZ = 0;
float baseZAccel = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.begin();
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);

  float sumZ = 0;
  for (int i = 0; i < 500; i++) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    sumZ += a.acceleration.z;
    delay(3);
  }
  baseZAccel = sumZ / 500.0;

  lastTime = millis();
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  unsigned long currentTime = millis();
  float dt = (currentTime - lastTime) / 1000.0;
  lastTime = currentTime;

  float accelZ = a.acceleration.z - baseZAccel;

  velocityZ += accelZ * dt;
  positionZ += velocityZ * dt;

  Serial.println(positionZ);
  delay(10);
}
