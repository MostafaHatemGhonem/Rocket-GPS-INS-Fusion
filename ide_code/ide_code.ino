#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

SoftwareSerial ss(3, 2); 
TinyGPSPlus gps;
Adafruit_MPU6050 mpu;

// Define a packed struct that perfectly matches Python's '<HIfffffB'
// 2 bytes (header) + 4 (timestamp) + 20 (5 floats) + 1 (flag) = 27 bytes total
struct __attribute__((packed)) TelemetryPacket {
  uint16_t header = 0xBBAA;
  uint32_t timestamp;
  float accel_x;
  float accel_y;
  float accel_z;
  float gps_alt;
  float gps_vel;
  uint8_t gps_updated;
};

void setup() {
  // Matched to Python's SerialManager baud rate
  Serial.begin(500000); 
  ss.begin(9600);
  
  if (!mpu.begin()) {
    // You won't see this in Python, but good for raw serial debugging
    Serial.println("MPU6050 Error"); 
  } else {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  }
}

void loop() {
  // 1. Drain the GPS buffer constantly to prevent SoftwareSerial overflow
  while (ss.available() > 0) {
    gps.encode(ss.read());
  }

  // 2. Transmit data strictly at ~100Hz (every 10ms) without blocking the loop
  static unsigned long lastTime = 0;
  if (millis() - lastTime >= 10) {
    lastTime = millis();
    
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    TelemetryPacket pkt;
    pkt.timestamp = millis();
    pkt.accel_x = a.acceleration.x;
    pkt.accel_y = a.acceleration.y;
    pkt.accel_z = a.acceleration.z;

    // Check if GPS data is valid and fresh
    if (gps.location.isValid() && gps.location.age() < 2000) {
      pkt.gps_alt = gps.altitude.meters();
      pkt.gps_vel = gps.speed.mps(); 
      pkt.gps_updated = 1;
    } else {
      pkt.gps_alt = 0.0;
      pkt.gps_vel = 0.0;
      pkt.gps_updated = 0;
    }

    // Send the entire 27-byte struct in one atomic binary write
    Serial.write((uint8_t*)&pkt, sizeof(pkt));
  }
}
