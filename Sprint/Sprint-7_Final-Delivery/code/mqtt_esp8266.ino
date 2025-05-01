
#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// WiFi credentials
#define WLAN_SSID "AndroidAPAD0D"
#define WLAN_PASS "Itamia2121"

// MQTT server settings
#define MQTT_SERVER "192.168.157.198"
#define MQTT_PORT 1883
#define MQTT_USERNAME ""
#define MQTT_PASSWORD ""

// Pins
#define FAN_PIN D0
#define LED_PIN D3
#define LED2_PIN D4

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD);
Adafruit_MQTT_Subscribe esp8266_led = Adafruit_MQTT_Subscribe(&mqtt, MQTT_USERNAME "/leds/esp8266");

void MQTT_connect();

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(LED_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);

  Serial.println(F("Starting..."));
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  mqtt.subscribe(&esp8266_led);
}

void loop() {
  MQTT_connect();

  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription())) {
    if (subscription == &esp8266_led) {
      char *message = (char *)esp8266_led.lastread;
      Serial.print(F("Got: "));
      Serial.println(message);

      if (strncmp(message, "LED1ON", 6) == 0) {
        digitalWrite(LED_PIN, HIGH);
      } else if (strncmp(message, "LED1OFF", 7) == 0) {
        digitalWrite(LED_PIN, LOW);
      } else if (strncmp(message, "LED2ON", 6) == 0) {
        digitalWrite(LED2_PIN, HIGH);
      } else if (strncmp(message, "LED2OFF", 7) == 0) {
        digitalWrite(LED2_PIN, LOW);
      } else if (strncmp(message, "ALLON", 5) == 0) {
        digitalWrite(LED_PIN, HIGH);
        digitalWrite(LED2_PIN, HIGH);
      } else if (strncmp(message, "ALLOFF", 6) == 0) {
        digitalWrite(LED_PIN, LOW);
        digitalWrite(LED2_PIN, LOW);
      } else if (strncmp(message, "FANON", 5) == 0) {
        digitalWrite(FAN_PIN, HIGH);
      } else if (strncmp(message, "FANOFF", 6) == 0) {
        digitalWrite(FAN_PIN, LOW);
      }
    }
  }

  delay(20);
}

void MQTT_connect() {
  int8_t ret;

  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");
  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqtt.disconnect();
    delay(5000);
    retries--;
    if (retries == 0) {
      while (1);
    }
  }
  Serial.println("MQTT Connected!");
}
