#include <SoftwareSerial.h>
#include <DRV8835MotorShield.h>

#define TRIG 3 //TRIG 핀 설정 (초음파 보내는 핀)
#define ECHO 2 //ECHO 핀 설정 (초음파 받는 핀)

// Pololu DRV8835 쉴드 객체 생성
DRV8835MotorShield motors;

int TxPin = A5;
int RxPin = A4;

SoftwareSerial bluetooth(TxPin, RxPin);

int Fspeed = 200;  // 왼쪽 모터 속도
int Rspeed = 200;  // 오른쪽 모터 속도

char receivedChar; 
bool commandReceived = false;

void Total_Forward();
void Total_Backward();
void Front_Forward();
void Front_Backward();
void Rear_Forward();
void Rear_Backward();
void Stop();
void BTMod();

void Total_Forward() { 
  motors.setM1Speed(-Fspeed);  // 앞쪽 모터 전진
  motors.setM2Speed(-Rspeed);  // 뒤쪽 모터 전진
}

void Total_Backward() {
  motors.setM1Speed(Fspeed); // 앞쪽 모터 후진
  motors.setM2Speed(Rspeed); // 뒤쪽 모터 후진
}

void Front_Forward() {
  motors.setM1Speed(-Fspeed);   // 앞쪽 모터 전진
//  motors.setM2Speed(Rspeed); // 오른쪽 모터 후진
}

void Front_Backward() {
  motors.setM1Speed(Fspeed); // 앞쪽 모터 후진
//  motors.setM2Speed(-Rspeed);  // 뒤쪽 모터 전진
}

void Rear_Forward() {
//  motors.setM1Speed(Fspeed);   // 앞쪽 모터 전진
  motors.setM2Speed(-Rspeed); // 뒤쪽 모터 전진
}

void Rear_Backward() {
//  motors.setM1Speed(-Fspeed); // 앞쪽 모터 후진
  motors.setM2Speed(Rspeed);  // 뒤쪽 모터 후진
}

void Stop() {
  motors.setM1Speed(0);       // 왼쪽 모터 정지
  motors.setM2Speed(0);       // 오른쪽 모터 정지
}

void BTMod() {

  if (bluetooth.available()) {
    receivedChar = bluetooth.read(); // 블루투스로부터 데이터 수신
    Serial.print(receivedChar);      // 시리얼 모니터에 수신된 데이터 출력
    Serial.print(commandReceived);
  }
    if (receivedChar == 'W') { // 전진
      Total_Forward();
    } 
    else if (receivedChar == 'S') { // 후진
      Total_Backward();
    } 
    else if (receivedChar == 'E') { // 전륜 전진
      Front_Forward();
    } 
    else if (receivedChar == 'D') { // 전륜 후진
      Front_Backward();
    } 
    else if (receivedChar == 'Q') { // 후륜구동
      Rear_Forward();
    }
    else if (receivedChar == 'A') { // 후륜구동
      Rear_Backward();
    } 
    else if(receivedChar == 'X') { // 아무 키도 눌리지 않은 경우 정지
      Stop();
    }
}

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  // motors.init();  // DRV8835 초기화

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

void loop() {
  BTMod(); // 블루투스 모드 실행

//  long duration, distance;
//
//  digitalWrite(TRIG, LOW);
//  delayMicroseconds(2);
//  digitalWrite(TRIG, HIGH);
//  delayMicroseconds(10);
//  digitalWrite(TRIG, LOW);
//
//  duration = pulseIn (ECHO, HIGH);

//  Serial.println(duration );
//  Serial.print("\nDIstance : ");
//  Serial.print(distance);
//  Serial.println(" Cm");
//  delay(500);
}
