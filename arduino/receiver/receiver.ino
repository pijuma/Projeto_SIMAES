/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/ttgo-lora32-sx1276-arduino-ide/
*********/

// MQTT
// #include <PubSubClient.h>
#include<WiFi.h>

//Libraries for LoRa
#include <SPI.h>
#include <LoRa.h>

//Libraries for OLED Display
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

//define the pins used by the LoRa transceiver module
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

//433E6 for Asia
//866E6 for Europe
//915E6 for North America
#define BAND 866E6

//OLED pins
#define OLED_SDA 4
#define OLED_SCL 15 
#define OLED_RST 16
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Wifi & setup
const char *SSID = "LETICIA E PIETRA";
const char *PWD = "bcc12010410";

WiFiClient wifiClient;
WiFiClient client;
// PubSubClient mqttClient(wifiClient);
// char * mqttServer = "broker.hivemq.com"
// int mqttPort = 1883;
const uint16_t port = 60000;
const char * host = "192.168.0.7 ";

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RST);

String LoRaData;
int wifi_connected = 0;

void setup() { 
  //initialize Serial Monitor
  Serial.begin(9600);

  // Connect to wifi
  Serial.print("Connecting to wifi: ");
  WiFi.begin(SSID, PWD);
  Serial.println(SSID);
  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  wifi_connected = 1;
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());

  
  
  //reset OLED display via software
  pinMode(OLED_RST, OUTPUT);
  digitalWrite(OLED_RST, LOW);
  delay(20);
  digitalWrite(OLED_RST, HIGH);
  
  //initialize OLED
  Wire.begin(OLED_SDA, OLED_SCL);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3c, false, false)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.print("LORA RECEIVER ");
  display.display();

  Serial.println("LoRa Receiver Test");
  
  //SPI LoRa pins
  SPI.begin(SCK, MISO, MOSI, SS);
  //setup LoRa transceiver module
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("LoRa Initializing OK!");
  display.setCursor(0,10);
  display.println("LoRa Initializing OK!");
  display.display();  



  Serial.println("Connecting to socket..");

  while (!client.connect(host, port)) {
    Serial.print("Connection to ");
    Serial.print(host);
    Serial.println(" failed. Retrying..");
    delay(1000);
  }
  // client.print("ESP 32 conectada! ");

  // Setup MQTT
  // mqttClient.setServer(mqttServer, mqttPort);
  // mqttClient.setCallback(back)
  Serial.print("Connection to ");
  Serial.print(port);
  Serial.println(" successfully established");
}

void loop() {
  
  // Wifi socket
  //try to parse packet
  int packetSize = LoRa.parsePacket();
  
  if (packetSize) {
    //received a packet
    if (wifi_connected) Serial.print("wifi connected. ");
    Serial.print("Received packet ");

    //read packet
    while (LoRa.available()) {
      LoRaData = LoRa.readString();
      Serial.print(LoRaData);
      client.print(LoRaData);
    }

    //print RSSI of packet
    int rssi = LoRa.packetRssi();
    Serial.print(" with RSSI ");    
    Serial.println(rssi);

   // Dsiplay information
   display.clearDisplay();
   display.setCursor(0,0);
   display.print("LORA RECEIVER");
   display.setCursor(0,20);
   display.print("Received packet:");
   display.setCursor(0,30);
   display.print(LoRaData);
   display.setCursor(0,40);
   display.print("RSSI:");
   display.setCursor(30,40);
   display.print(rssi);
   display.display();   
  }
}
