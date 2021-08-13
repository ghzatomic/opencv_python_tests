#include "Arduino.h"
#include "Servo.h"
#include <stdlib.h>
#include <SoftwareSerial.h>

#define servo_pinX 8 
#define servo_pinY 7

#define BTHC05_PIN_TXD  9
#define BTHC05_PIN_RXD  10

#define TRIGGER_FIRE  5

const int servoXStartRestPosition   = 90;  //Starting position X
const int servoYStartRestPosition   = 120;  //Starting position Y

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
  //bthc05.begin(9600);
  //bthc05.setTimeout(1);

  pinMode(TRIGGER_FIRE, OUTPUT); 

  pinMode(servo_pinX, OUTPUT); 
  pinMode(servo_pinY, OUTPUT); 

  servo_X.attach(servo_pinX); // start servo control
  //servo_X.detach();
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
    moveX(false, charToInt(comando[2]));
    //Serial.println("DIREITA");
  }
  if (comando[3] != '0'){
    moveX(true, charToInt(comando[3]));
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
  servo_Y.write(servoYStartRestPosition);
  servo_X.write(servoXStartRestPosition);
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

void scan(){
  servo_X.write(0); 
  delay(2000); 
  servo_X.write(180); 
  delay(2000); 
}

void atira(){
  digitalWrite(TRIGGER_FIRE, HIGH);
  delay(100);
  digitalWrite(TRIGGER_FIRE, LOW);
}


int multiplicador_vel_servo(int forca){
  if (forca == 3){
    return 3;
  }else if (forca == 2){
    return 2;
  }else{
    return 1;
  }
}

void controla_posicoes_limites(){
  if (posY >= 180){
    posY = 180;
  }else if (posY <= 10){
    posY = 10;
  }
  if (posX >= 180){
    posX = 180;
  }else if (posX <= 0){
    posX = 0;
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
  if (last_posX != posX){
    servo_X.write(posX);  
  }
  if (last_posY != posY){
    servo_Y.write(posY);  
  }
  //servo_Y.detach();
  //servo_X.detach();
}

void loop() {
  // put your main code here, to run repeatedly:
  int aval = Serial.available();
  //int aval = true;
  char character;
  if (aval) {
    character = Serial.read();//bthc05.read();
    if (character == '|'){
      //Serial.println(comando);
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
