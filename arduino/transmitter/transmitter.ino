/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/ttgo-lora32-sx1276-arduino-ide/
*********/

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

#define WATER_SENSOR_PIN 13

void do_stuff();




//packet counter
int counter = 0;
int previousValue = 0;

const int intervalo_sensor = 1000;
int curr_interval = 0;

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RST);

void setup() {
  // variaveis para a contagem do fluxo
  

  //initialize Serial Monitor
  Serial.begin(9600);

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
  display.print("LORA SENDER ");
  display.display();
  
  Serial.println("LoRa Sender Test");

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
  display.print("LoRa Initializing OK!");
  display.display();
  delay(2000);

}

void loop() {
  int sensorValue = analogRead(WATER_SENSOR_PIN);
  float voltage = sensorValue * (5.0/1023.0);

  if ((millis() - curr_interval) > intervalo_sensor) 
  {
    curr_interval = millis();

    do_stuff();
  }

  if (voltage != previousValue)
  {
    if(voltage > previousValue)
    {
      // do_stuff();
      
      counter++;
    }
    previousValue = sensorValue;
  }
  
  // delay(10000);
}

void do_stuff()
{
 
  Serial.print("Pulso ");
  Serial.print(counter);
  Serial.println();
  
  //Send LoRa packet to receiver
  LoRa.beginPacket();
  LoRa.print("Pulso ");
  LoRa.print(counter);
  LoRa.endPacket();

  display.clearDisplay();
  display.setCursor(0,0);
  display.println("LORA SENDER");
  display.setCursor(0,20);
  display.setTextSize(1);
  display.print("LoRa packet sent.");
  display.setCursor(0,30);
  display.print("Pulse Counter:");
  display.setCursor(50,40);
  display.print(counter); 
  display.setCursor(50,55);     
  display.print("=D");
  display.display();
}
