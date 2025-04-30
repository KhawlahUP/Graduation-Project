#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

/************* WiFi Access Point *************/
#define WLAN_SSID "Note"
#define WLAN_PASS ""

/************* MQTT Server Details *************/
#define MQTT_SERVER "192.168.157.198" // غيّر هذا حسب عنوان السيرفر الخاص بك
#define MQTT_PORT 1883

/************* Pins *************/
#define FAN_PIN D0
#define LED_PIN D3
#define LED2_PIN D4

/************* WiFi & MQTT Clients *************/
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_PORT);

/************* MQTT Subscriptions *************/
Adafruit_MQTT_Subscribe fanControl = Adafruit_MQTT_Subscribe(&mqtt, "fan/control");
Adafruit_MQTT_Subscribe led1Control = Adafruit_MQTT_Subscribe(&mqtt, "led1/control");
Adafruit_MQTT_Subscribe led2Control = Adafruit_MQTT_Subscribe(&mqtt, "led2/control");

void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(LED_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  pinMode(FAN_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED2_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  mqtt.subscribe(&fanControl);
  mqtt.subscribe(&led1Control);
  mqtt.subscribe(&led2Control);
}

void loop() {
  // تأكد من الاتصال بالسيرفر
  if (mqtt.connected() == false) {
    reconnectMQTT();
  }
  mqtt.processPackets(10000);
  mqtt.ping();

  // استقبال الرسائل
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(100))) {
    if (subscription == &fanControl) {
      controlDevice((char *)fanControl.lastread, FAN_PIN);
    } else if (subscription == &led1Control) {
      controlDevice((char *)led1Control.lastread, LED_PIN);
    } else if (subscription == &led2Control) {
      controlDevice((char *)led2Control.lastread, LED2_PIN);
    }
  }
}

void controlDevice(char* message, int pin) {
  Serial.print("Message received: ");
  Serial.println(message);

  if (strcmp(message, "ON") == 0) {
    digitalWrite(pin, HIGH);
  } else if (strcmp(message, "OFF") == 0) {
    digitalWrite(pin, LOW);
  }
}

void reconnectMQTT() {
  int8_t ret;
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqtt.disconnect();
    delay(5000);
  }
  Serial.println("MQTT Connected!");
}
