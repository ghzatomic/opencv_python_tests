#include "Arduino.h"
#include "Servo.h"
#include <stdlib.h>
#include <SoftwareSerial.h>

#define servo_pinX 4 
#define servo_pinY 3

#define BTHC05_PIN_TXD  9
#define BTHC05_PIN_RXD  10

#define TRIGGER_FIRE  6
 
#define IN4 10
#define IN3 9
#define ENABLEB 4

const bool usedriver_x = false;

const bool useBluetooth = false;

const int servoXStartRestPosition   = 1500;  //Starting position X
const int servoYStartRestPosition   = 1200;  //Starting position Y

const int servoXMaxPos   = 2000;
const int servoXMinPos   = 1000;

const int servoYMaxPos   = 2000;
const int servoYMinPos   = 1000;

Servo servo_X; // servo controller (multiple can exist)
Servo servo_Y; // servo controller (multiple can exist)

int posX = servoXStartRestPosition;
int posY = servoYStartRestPosition;

int last_posX = posX;
int last_posY = posY;

SoftwareSerial bthc05(BTHC05_PIN_RXD,BTHC05_PIN_TXD); // RX, TX // Lembrar de inverter no arduino .. onde ta tx vira rx

void setup() {
  
  Serial.begin(115200);
  Serial.setTimeout(1);
  while (!Serial) ; // wait for serial port to connect. Needed for native USB
  Serial.println("start");
  if (useBluetooth){
    bthc05.begin(9600);
    bthc05.setTimeout(1);
  }
  

  pinMode(TRIGGER_FIRE, OUTPUT); 

  pinMode(servo_pinX, OUTPUT); 
  pinMode(servo_pinY, OUTPUT); 

  if (!usedriver_x){
    servo_X.attach(servo_pinX); // start servo control
  //servo_X.detach();
  }else{
    pinMode(ENABLEB, OUTPUT); 
    pinMode(IN4, OUTPUT); 
    pinMode(IN3, OUTPUT); 
    digitalWrite(ENABLEB, HIGH);
  }
  
  servo_Y.attach(servo_pinY); // start servo control
  //servo_Y.detach();
  reset();

  digitalWrite(TRIGGER_FIRE, HIGH);
  delay(1000);
  digitalWrite(TRIGGER_FIRE, LOW);
  
}


String comando = "";

void comandoEncontrado(String comando){
  Serial.println(comando);
  if (comando[0] != '0'){
    moveY(false, charToInt(comando[0]));
    //Serial.println("SOBE");
  }
  if (comando[1] != '0'){
    moveY(true, charToInt(comando[1]));
    //Serial.println("DESCE");
  }
  if (comando[2] != '0'){
    if (!usedriver_x){
      moveX(false, charToInt(comando[2]));
    }else{
      moveX_driver(false);
    }
    //Serial.println("DIREITA");
  }
  if (comando[3] != '0'){
    if (!usedriver_x){
      moveX(true, charToInt(comando[3]));
    }else{
      moveX_driver(true);
    }
    //Serial.println("ESQUERDA");
  }
  if (comando[4] != '0'){
    atira();
    //Serial.println("ATIRA");
  }
  if (comando[5] != '0'){
    reset();
    //Serial.println("ATIRA");
  }
}

void reset(){
  last_posX = servoXStartRestPosition;
  last_posY = servoYStartRestPosition;
  servo_Y.writeMicroseconds(servoYStartRestPosition);
  servo_X.writeMicroseconds(servoXStartRestPosition);
  delay(100);
}

char floatToStr(float val){
  char* arr;
  String value = String(val);
  strcpy( arr, value.c_str() );
  return *arr;
}

int charToInt(char c){
  return c - '0';
}

void atira(){
  digitalWrite(TRIGGER_FIRE, HIGH);
  delay(100);
  digitalWrite(TRIGGER_FIRE, LOW);
}


int multiplicador_vel_servo(int forca){
  if (forca == 3){
    return 15;
  }else if (forca == 2){
    return 5;
  }else{
    return 1;
  }
}

void controla_posicoes_limites(){
  if (posY >= servoYMaxPos){
    posY = servoYMaxPos;
  }else if (posY <= servoYMinPos){
    posY = servoYMinPos;
  }
  if (posX >= servoXMaxPos){
    posX = servoXMaxPos;
  }else if (posX <= servoXMinPos){
    posX = servoXMinPos;
  }
}

void moveX_driver(bool direita){
  if(direita){
    posX += multiplicador_vel_servo(1);  
    digitalWrite(IN4, HIGH);
    delay(80);
    digitalWrite(IN4, LOW);
  }else{
    posX -= multiplicador_vel_servo(1);
    digitalWrite(IN3, HIGH);
    delay(80);
    digitalWrite(IN3, LOW);
  }
}

void moveX(bool direita, int forca){
  if(direita){
    posX += multiplicador_vel_servo(forca);    
  }else{
    posX -= multiplicador_vel_servo(forca);   
  }
  //Serial.print("Servo X: ");
  //Serial.println(posX);
}

void moveY(bool cima, int forca){
  if(cima){
    posY += multiplicador_vel_servo(forca);    
  }else{
    posY -= multiplicador_vel_servo(forca);   
  }
  //Serial.print("Servo Y: ");
  //Serial.println(posY);
}

void update_servos(){
  controla_posicoes_limites();
  //servo_Y.attach(servo_pinY); // start servo control
  //servo_X.attach(servo_pinX); // start servo control
  if (!usedriver_x){
    if (last_posX != posX){
      servo_X.writeMicroseconds(posX);  
    }
  }
  if (last_posY != posY){
    servo_Y.writeMicroseconds(posY);  
  }
  //servo_Y.detach();
  //servo_X.detach();
}

void loop() {
  // put your main code here, to run repeatedly:
  int aval = 0;
  if (useBluetooth){
    aval = bthc05.available();
  }else{
    aval = Serial.available();
  }
  
  char character;
  if (aval) {
    if (useBluetooth){
      character = bthc05.read();
    }else{
      character = Serial.read();//;
    }
    Serial.println(character);
    if (character == '|'){
      Serial.println(comando);
      comandoEncontrado(comando);
      comando = "";        
    }else{
      comando+=character;
    }  
    
  }

  //moveX(true, 1);
  update_servos();
  last_posX = posX;
  last_posY = posY;
  //scan();
}
