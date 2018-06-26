
#include <Wire.h>
#include <Adafruit_BMP085.h>
#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT22

Adafruit_BMP085 bmp;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // Open serial with bluetooth module
  Serial.begin(9600);
  
  if (!bmp.begin()) {
	  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
  }

  dht.begin();
}
  
void loop() {
    float temp = bmp.readTemperature();
    int pressure = bmp.readPressure();
    float altitude = bmp.readAltitude();
   
    float humidity = dht.readHumidity();
    float temperatur = dht.readTemperature();

    String data = "{";
    data = data + "\"temp\": " + String(temp) + ", ";
    data = data + "\"pressure\": " + String(pressure) + ", ";
    data = data + "\"altitude\": " + String(altitude) + ", ";
    data = data + "\"humidity\": " + String(humidity) + ", ";
    data = data + "\"temperatur\": " + String(temperatur) + "}";
  
    Serial.println(data);
    delay(1500);
}
