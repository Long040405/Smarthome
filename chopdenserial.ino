int DENNGU = 11;
int DENKHACH = 12;
int RELAY_PIN = 5;
#include <Servo.h> 
int sensorPin = A0;
int SERVO = 3;
int SERVO2 = 4;
int SERVO3 = 2;

Servo myservo;
Servo myservo2;
Servo myservo3;
int pos = 0;    

char command;

int gettime() { 
  int delaytime = 200;
  return delaytime;
}

void setup() {
  Serial.begin(9600);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(DENNGU, OUTPUT);
  pinMode(DENKHACH, OUTPUT);
  myservo.attach(SERVO);
  myservo2.attach(SERVO2);
  myservo3.attach(SERVO3);
  myservo3.write(0);
}

void simulatePresence() {
  // Ngẫu nhiên bật/tắt đèn phòng ngủ
  digitalWrite(DENNGU, HIGH);
  delay(random(5000, 10000));  // Bật trong khoảng thời gian ngẫu nhiên từ 5 đến 10 giây
  digitalWrite(DENNGU, LOW);
  delay(random(5000, 10000));  // Tắt trong khoảng thời gian ngẫu nhiên từ 5 đến 10 giây
  
  // Ngẫu nhiên bật/tắt đèn phòng khách
  digitalWrite(DENKHACH, HIGH);
  delay(random(5000, 10000));  // Bật trong khoảng thời gian ngẫu nhiên từ 5 đến 10 giây
  digitalWrite(DENKHACH, LOW);
  delay(random(5000, 10000));  // Tắt trong khoảng thời gian ngẫu nhiên từ 5 đến 10 giây

  // Ngẫu nhiên bật/tắt quạt
  digitalWrite(RELAY_PIN, HIGH);
  delay(random(5000, 10000));  // Bật trong khoảng thời gian ngẫu nhiên từ 5 đến 10 giây
  digitalWrite(RELAY_PIN, LOW);
  delay(random(5000, 10000));  // Tắt trong khoảng thời gian ngẫu nhiên từ 5 đến 10 giây
}

void loop() {
  // Kiểm tra dữ liệu gửi từ Serial
  if (Serial.available() > 0) {    
    command = Serial.read();   

    // ĐÈN PHÒNG NGỦ
    if (command == '1') {
      digitalWrite(DENNGU, HIGH); // Bật đèn
      Serial.println("ĐÈN PHÒNG NGỦ ĐÃ BẬT");
    } else if (command == '0') {
      digitalWrite(DENNGU, LOW); // Tắt đèn
      Serial.println("ĐÈN PHÒNG NGỦ ĐÃ TẮT");
    } else if (command == '2') {
      Serial.println("ĐÈN PHÒNG NGỦ ĐANG NHÁY");
      int delaytime = gettime();
      for (int i = 0; i < 10; i++) {
        digitalWrite(DENNGU, LOW); 
        delay(delaytime);
        digitalWrite(DENNGU, HIGH); 
        delay(delaytime);
      }
    }
    // ĐÈN PHÒNG KHÁCH
    else if (command == '3') {
      digitalWrite(DENKHACH, HIGH); 
      Serial.println("ĐÈN PHÒNG KHÁCH ĐÃ BẬT");
    } else if (command == '4') {
      digitalWrite(DENKHACH, LOW); 
      Serial.println("ĐÈN PHÒNG KHÁCH ĐÃ TẮT");
    } else if (command == '5') {
      Serial.println("ĐÈN PHÒNG KHÁCH ĐANG NHÁY");
      int delaytime = gettime();
      for (int i = 0; i < 10; i++) {
        digitalWrite(DENKHACH, LOW); 
        delay(delaytime);
        digitalWrite(DENKHACH, HIGH); 
        delay(delaytime);
      }
    }
    // Chớp đèn cùng lúc
    else if (command == '6') {
      Serial.println("2 ĐÈN CÙNG CHỚP");
      int delaytime = gettime();
      for (int i = 0; i < 32; i++) {
digitalWrite(DENNGU, HIGH); 
        delay(delaytime);
        digitalWrite(DENNGU, LOW); 
        delay(delaytime);
        digitalWrite(DENKHACH, HIGH); 
        delay(delaytime);
        digitalWrite(DENKHACH, LOW); 
        delay(delaytime);
      }
    }
    // Quạt
    else if (command == 'b') {
      digitalWrite(RELAY_PIN, HIGH); 
      Serial.println("QUẠT ĐÃ BẬT");
    } else if (command == 't') {
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("QUẠT ĐÃ TẮT");
    }
    // Cửa mở
    else if (command == 'm') {
      myservo.write(0);              
      myservo2.write(180);              
      delay(1000);
    }
    // Cửa đóng
    else if (command == 'd') {
      myservo2.write(90);
      delay(100);
      myservo.write(90); 
      delay(1000);
    }
    // Garage 
    //đóng
    else if (command == 'g') {
      myservo3.write(0);
      delay(100);
    }
    //mở
    else if (command == 'e') {
      myservo3.write(180);
      delay(100);
    }
    if (command == 'p') {
      Serial.println("CHẾ ĐỘ MÔ PHỎNG CÓ NGƯỜI Ở NHÀ ĐƯỢC KÍCH HOẠT");
      simulatePresence();
    }

  }

  // Đọc nhiệt độ từ cảm biến LM35
  int reading = analogRead(sensorPin);
  float voltage = reading * 5.0 / 1024.0;
  float temp = voltage * 100.0;
  Serial.print("Nhiệt độ: ");
  Serial.print(temp);
  Serial.println(" C");
  delay(1000); 

  // Nếu nhiệt độ lớn hơn 60 độ C
  if (temp > 60.0) {
    Serial.println("NHIỆT ĐỘ CAO! THỰC HIỆN CÁC HÀNH ĐỘNG KHẨN CẤP");
    int delaytime = gettime();
    // Nháy đèn 2 lần
    for (int i = 0; i < 2; i++) {
      digitalWrite(DENNGU, HIGH); 
      delay(delaytime);
      digitalWrite(DENNGU, LOW); 
      delay(delaytime);
      digitalWrite(DENKHACH, HIGH); 
      delay(delaytime);
      digitalWrite(DENKHACH, LOW); 
      delay(delaytime);
    }
    // Tắt đèn phòng ngủ
    digitalWrite(DENNGU, LOW); 
    Serial.println("ĐÈN PHÒNG NGỦ ĐÃ TẮT DO NHIỆT ĐỘ CAO");
    // Tắt đèn phòng khách
    digitalWrite(DENKHACH, LOW); 
    Serial.println("ĐÈN PHÒNG KHÁCH ĐÃ TẮT DO NHIỆT ĐỘ CAO");
    // Mở quạt
    digitalWrite(RELAY_PIN, HIGH); 
    Serial.println("QUẠT ĐÃ BẬT DO NHIỆT ĐỘ CAO");
    // Mở cửa
    myservo.write(0);              
    myservo2.write(180);              
    Serial.println("CỬA ĐÃ MỞ DO NHIỆT ĐỘ CAO");
    // Mở cửa garage
    myservo3.write(180);
    Serial.println("CỬA GARAGE ĐÃ MỞ DO NHIỆT ĐỘ CAO");
  }
}