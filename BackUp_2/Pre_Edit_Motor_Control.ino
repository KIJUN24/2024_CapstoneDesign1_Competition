#include <SoftwareSerial.h>
#include <DRV8835MotorShield.h>

// Pololu DRV8835 쉴드 객체 생성
DRV8835MotorShield motors;

int TxPin = A5;
int RxPin = A4;

SoftwareSerial bluetooth(TxPin, RxPin);

int Lspeed = 255;  // 왼쪽 모터 속도
int Rspeed = 255;  // 오른쪽 모터 속도

char receivedChar;



void Forward();
void Backward();
void Right();
void Left();
void Stop();
void BTMod();

void Forward() { 
  motors.setM1Speed(-Lspeed);  // 왼쪽 모터 전진
  motors.setM2Speed(-Rspeed);  // 오른쪽 모터 전진
}

void Backward() {
  motors.setM1Speed(Lspeed); // 왼쪽 모터 후진
  motors.setM2Speed(Rspeed); // 오른쪽 모터 후진
}

void Right() {
  motors.setM1Speed(-Lspeed);  // 왼쪽 모터 전진
  motors.setM2Speed(Rspeed); // 오른쪽 모터 후진
}

void Left() {
  motors.setM1Speed(Lspeed); // 왼쪽 모터 후진
  motors.setM2Speed(-Rspeed);  // 오른쪽 모터 전진
}

void Stop() {
  motors.setM1Speed(0);       // 왼쪽 모터 정지
  motors.setM2Speed(0);       // 오른쪽 모터 정지
}

void BTMod() {
  if (bluetooth.available()) {
    receivedChar = bluetooth.read(); // 블루투스로부터 데이터 수신
    Serial.print(receivedChar);      // 시리얼 모니터에 수신된 데이터 출력
  }

  if (receivedChar == 'F') { // 전진 (앱에서 인식하는 키에 따라 수정할 것)
    Forward();
  } 
  else if (receivedChar == 'B') { // 후진
    Backward();
  } 
  else if (receivedChar == 'L') { // 좌회전
    Left();
  } 
  else if (receivedChar == 'R') { // 우회전
    Right();
  } 
  else if (receivedChar == 'X') { // 정지
    Stop();
  }
}

void setup() {
  Serial.begin(9600);
  bluetooth.begin(9600);
  // motors.init();  // DRV8835 초기화/
}

void loop() {
  BTMod(); // 블루투스 모드 실행
}
