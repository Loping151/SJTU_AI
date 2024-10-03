// define the LCD screen
#include <NOKIA5110_TEXT.h>
NOKIA5110_TEXT display(15, 16, 17, 7, 6);
#define inverse  false
#define UseDefaultFont  false
#define contrast 0xBF // default is 0xBF set in LCDinit, Try 0xB1(good @ 3.3V) or 0xBF if your display is too dark
#define bias 0x13 // LCD bias mode 1:48: Try 0x13 or 0x14
#define cd display.LCDClear();
// define the 8266 module
#include <SoftwareSerial.h>
SoftwareSerial esp(2, 3);
uint32_t baud = 115200;
String rt = "";
// control bits for testpoints
int TP[4][3]{0, 0, 0, 8, 9, 14, 12, 13, 19, 10, 11, 18};
#define Rs 0 // small R = 680 Ohm
#define Rl 1 // large R = 470 kOhm
#define ADC 2 // ADC input(PCx) 

#define msg String(rcd[0][0][1])+","+String(rcd[0][0][2])+","+String(rcd[0][1][0])+","+String(rcd[0][1][2])+","+String(rcd[0][2][0])+","+String(rcd[0][2][1])+","+String(rcd[1][0][1])+","+String(rcd[1][0][2])+","+String(rcd[1][1][0])+","+String(rcd[1][1][2])+","+String(rcd[1][2][0])+","+String(rcd[1][2][1])+"\r\n"

void setup()
{
  // screen init and boot effect
  display.LCDInit(inverse, contrast, bias); //initialize
  cd //clear whole screen
  
  // wifi connection
  Serial.begin(baud);
  esp.begin(baud);
  delay(5000);
  // code below will be remembered inside esp8266
  // espCom(F("AT+SAVETRANSLINK=1,\"192.168.1.9\",2333,\"TCP\"\r\n"), 2000);
  // espCom(F("AT+CWMODE=1\r\n"), 2000);
  // espCom(F("AT+RST\r\n"), 2000);
  // espCom(F("AT+CWJAP=\"CMCC-SJTU\",\"Ww331811\"\r\n"), 10000);
  // espCom(F("AT+CIPSTART=\"TCP\",\"192.168.1.9\",2333\r\n"), 10000);
  // espCom(F("AT+CIPMODE=1\r\n"), 2000);
  // espCom(F("AT+CIPSEND\r\n"), 2000);
  onboot_notice();
  rt = espCom("Client Started.\r\n", 500);
}

void loop()
{
  if(rt[0]=='t')
    rt[0] = ' ', disp(rt+" ", 0, 4);
  rt = espCom(autoSelect(), 333);
  
}

// simple display controller
void disp(String s, int X, int Y)
{
  display.LCDgotoXY(X, Y); // (go to (X , Y) (0-84 columns, 0-5 blocks)
  display.LCDString(&s[0]); //print
}

// onboot animation♂
void onboot_notice()
{
  for(register int i=0; i<6; ++i)
  {
    disp("114", 15, i);
    disp("514", 55, 5-i);
    delay(300);
  }
  cd
  disp("Welcome", 20, 2);
  disp("to use", 25, 3);
  disp("LOPING151", 15, 5);
  delay(3000);
  cd
  display.LCDgotoXY(0, 0);
  display.LCDString("Connecting");
  display.LCDgotoXY(0, 1);
  display.LCDString("to server");
  display.LCDgotoXY(0, 2);
  delay(2000);
  cd
}

// send command or data to the server
String espCom(String command, const int timeout)
{
  String inData = "";
  esp.print(command);
  long int time = millis();
  while ( (time + timeout) > millis())
  {
    while (esp.available())
    {
      char c = esp.read();
      inData += c;
    }
  }
  return inData;
}

// set all pin Low before each test
void setLow()
{
  for(register int i=1;i<=3;++i)
    for(register int j=0;j<=2;++j)
      pinMode(TP[i][j], INPUT);
}

// test the case for small resistance
double testRS(int x, int y, int cmd=1)
{
  setLow();
  pinMode(TP[x][ADC], INPUT);
  pinMode(TP[y][ADC], INPUT);
  pinMode(TP[x][Rl], INPUT);
  pinMode(TP[y][Rl], INPUT);
  pinMode(TP[x][Rs], OUTPUT);
  pinMode(TP[y][Rs], OUTPUT);
  digitalWrite(TP[x][Rs], HIGH);
  digitalWrite(TP[y][Rs], LOW);
  delay(5);
  int vinth=analogRead(TP[x][ADC]);
  int vintl=analogRead(TP[y][ADC]);
  if(abs(vinth+vintl-1023)>5 and cmd)
    return 114;
  double vdiff = (vinth-vintl)*5.0/1023;
  return vdiff;
}

// test the case for large resistance
double testRL(int x, int y)
{
  setLow();
  pinMode(TP[x][ADC], INPUT);
  pinMode(TP[y][ADC], INPUT);
  pinMode(TP[x][Rs], INPUT);
  pinMode(TP[y][Rs], INPUT);
  pinMode(TP[x][Rl], OUTPUT);
  pinMode(TP[y][Rl], OUTPUT);
  digitalWrite(TP[x][Rl], HIGH);
  digitalWrite(TP[y][Rl], LOW);
  delay(50);
  int vinth=analogRead(TP[x][ADC]);
  int vintl=analogRead(TP[y][ADC]);
  if(vinth<850)
    delay(200);
  else
    return 514;
  vinth=analogRead(TP[x][ADC]);
  vintl=analogRead(TP[y][ADC]);
  if(abs(vinth+vintl-1023)>15)
    return 514;
  double vdiff = (vinth-vintl)*5.0/1023;
  return vdiff;
}

// large capacity
String testCL(int x, int y)
{ 
  setLow();
  disp(String("Mode: LC"), 0, 1); // Small C
  disp(String("Testing"), 0, 2);
  disp(String("Don't shift!"), 0, 3); // Warning
  pinMode(TP[x][ADC], INPUT);
  pinMode(TP[y][ADC], INPUT);
  pinMode(TP[x][Rl], INPUT); // use small R, the charge time is RC. If C is too small, charge time is small. This case goto TestCS to use larger R
  pinMode(TP[y][Rl], INPUT);
  pinMode(TP[x][Rs], OUTPUT);
  pinMode(TP[y][Rs], OUTPUT);
  int rcdv[200];
  String tmpS;
  int cnt=0;
  int vinth=analogRead(TP[x][ADC]);
  int vintl=analogRead(TP[y][ADC]);
  while(vinth>5 or vintl>5)
    vinth=analogRead(TP[x][ADC]), vintl=analogRead(TP[y][ADC]); // wait until q=0
  delay(10);
  long int Cstart=micros();
  digitalWrite(TP[x][Rs], HIGH);
  while(analogRead(TP[x][ADC])<1018 and micros()-Cstart<1000000)
      rcdv[max(cnt++/3,200)]=analogRead(TP[x][ADC]);
  long int tdiff=micros()-Cstart-116; // 116 is the base 
  tdiff=abs(tdiff);
  disp("            ", 0, 3);
  disp("Used "+String(tdiff)+"us",0,3);
  if(tdiff>900000)
  {
    disp("            ", 0, 0);
    disp("            ", 0, 1);
    disp("            ", 0, 2);
    disp("            ", 0, 3);
    return "Time LE";
  }
  if(tdiff<100)
    return testCS(x, y);
  else
  {
    espCom("plot cnt="+String(cnt)+"\r\n",10);
    for(register int i=0;i<200;++i)
      espCom(String(i)+","+String(rcdv[i])+",", 5);
  }
  return String(0.149*tdiff/680.0)+"uF  ";
}

// small capacity
String testCS(int x, int y) 
{  
  setLow();
  disp(String("Mode: SC"), 0, 1); // Large C
  pinMode(TP[x][ADC], INPUT);
  pinMode(TP[y][ADC], INPUT);
  pinMode(TP[x][Rs], INPUT);
  pinMode(TP[y][Rs], INPUT);
  pinMode(TP[x][Rl], OUTPUT);
  pinMode(TP[y][Rl], OUTPUT);
  int vinth=analogRead(TP[x][ADC]);
  int vintl=analogRead(TP[y][ADC]);
  while(vinth>2 or vintl>2)
    vinth=analogRead(TP[x][ADC]), vintl=analogRead(TP[y][ADC]); // wait until q=0
  long int Cstart=micros();
  digitalWrite(TP[x][Rl], HIGH);
  while(analogRead(TP[x][ADC])<1020 and micros()-Cstart<344);
  long int tdiff=micros()-Cstart-344;
  tdiff=abs(tdiff);
  disp("            ", 0, 3);
  disp("Used "+String(tdiff)+"us",0,3);
  if(tdiff>900000)
  {
    disp("            ", 0, 0);
    disp("            ", 0, 1);
    disp("            ", 0, 2);
    disp("            ", 0, 3);
    return "Time LE";
  }
  if(tdiff<220)
  {
    disp("            ", 0, 0);
    disp("            ", 0, 1);
    disp("            ", 0, 2);
    disp("            ", 0, 3);
    disp("Empty load", 0, 0);
    delay(500);
    return "";
  }
  return String(0.1*tdiff/470.0*1000)+"pF  ";
}

// judge if the voltage is valid for triod
bool isValid(double x)
{
  return x>0.4 and x<1.2;
}

void testNPN(int b)
{
  setLow();
  disp(String("Mode: NPN"), 0, 1);
  pinMode(TP[1][ADC], INPUT);
  pinMode(TP[2][ADC], INPUT);
  pinMode(TP[3][ADC], INPUT);
  // first we suppose b+1 is e and b+2 is c
  int c=1+b%3, e=1+(b+1)%3;
  pinMode(TP[b][Rl], OUTPUT);
  pinMode(TP[c][Rs], OUTPUT);
  pinMode(TP[e][Rs], OUTPUT);
  digitalWrite(TP[b][Rl], HIGH);
  digitalWrite(TP[c][Rs], HIGH);
  digitalWrite(TP[e][Rs], LOW);
  int sw;
  if(not isValid((analogRead(TP[b][ADC])-analogRead(TP[e][ADC]))/1023.0*5.0)) // block
  {
    sw=c, c=e, e=sw;
    pinMode(TP[c][Rl], INPUT);
    pinMode(TP[e][Rl], INPUT);
    pinMode(TP[c][Rs], OUTPUT);
    pinMode(TP[e][Rs], OUTPUT);
    digitalWrite(TP[c][Rs], HIGH);
    digitalWrite(TP[e][Rs], LOW);
    if(not isValid((analogRead(TP[b][ADC])-analogRead(TP[e][ADC]))/1023.0*5.0))
    {
      disp("Invalid", 0, 2);
      delay(1000);
      return;
    }
  }
  disp("TP:e"+String(e)+"b"+String(b)+"c"+String(c), 0, 0);
  delay(50);
  double vb=analogRead(TP[b][ADC])/1023.0*5.0, vc=analogRead(TP[c][ADC])/1023.0*5.0, ve=analogRead(TP[e][ADC])/1023.0*5.0, vcc=5.0;
  // disp("TP:e"+String(analogRead(TP[e][ADC]))+"b"+String(analogRead(TP[b][ADC]))+"c"+String(analogRead(TP[c][ADC])), 0, 3);
  disp("beta="+String((vcc-vc)/680/((vcc-vb)/470000)), 0, 2);
  delay(500);
}

void testPNP(int b)
{
  setLow();
  disp(String("Mode: PNP"), 0, 1);
  pinMode(TP[1][ADC], INPUT);
  pinMode(TP[2][ADC], INPUT);
  pinMode(TP[3][ADC], INPUT);
  // first we suppose b+1 is e and b+2 is c
  int c=1+b%3, e=1+(b+1)%3;
  pinMode(TP[b][Rl], OUTPUT);
  pinMode(TP[c][Rs], OUTPUT);
  pinMode(TP[e][Rs], OUTPUT);
  digitalWrite(TP[b][Rl], LOW);
  digitalWrite(TP[c][Rs], LOW);
  digitalWrite(TP[e][Rs], HIGH);
  int sw;
  if(not isValid(-(analogRead(TP[b][ADC])-analogRead(TP[e][ADC]))/1023.0*5.0)) // block
  {
    sw=c, c=e, e=sw;
    pinMode(TP[c][Rl], INPUT);
    pinMode(TP[e][Rl], INPUT);
    pinMode(TP[c][Rs], OUTPUT);
    pinMode(TP[e][Rs], OUTPUT);
    digitalWrite(TP[c][Rs], LOW);
    digitalWrite(TP[e][Rs], HIGH);
    if(not isValid(-(analogRead(TP[b][ADC])-analogRead(TP[e][ADC]))/1023.0*5.0))
    {
      disp("Invalid", 0, 2);
      delay(1000);
      return;
    }
  }
  disp("TP:e"+String(e)+"b"+String(b)+"c"+String(c), 0, 0);
  delay(50);
  double vb=analogRead(TP[b][ADC])/1023.0*5.0, vc=analogRead(TP[c][ADC])/1023.0*5.0, ve=analogRead(TP[e][ADC])/1023.0*5.0, vcc=5.0;
  // disp("TP:e"+String(analogRead(TP[e][ADC]))+"b"+String(analogRead(TP[b][ADC]))+"c"+String(analogRead(TP[c][ADC])), 0, 3);
  disp("beta="+String(vc/680/(vb/470000)), 0, 2);
  delay(500);
}

// do tests and auto select the mode
String autoSelect()
{  
  disp("            ", 0, 0);
  disp("            ", 0, 1);
  disp("            ", 0, 2);
  disp("            ", 0, 3);
   
  double rcdt[3][3]{};
  for(register int i=0;i<9;++i)
    if(i%3!=i/3)
      rcdt[i/3][i%3]=testRS(i/3+1, i%3+1, 0);
  // Cases for Triode
  if(isValid(rcdt[1][0]) and isValid(rcdt[2][0]))
  {
    testPNP(1);
    return "-1\r\n";
  }  
  if(isValid(rcdt[0][1]) and isValid(rcdt[2][1]))
  {
    testPNP(2);
    return "-1\r\n";
  }
  if(isValid(rcdt[0][2]) and isValid(rcdt[1][2]))
  {
    testPNP(3);
    return "-1\r\n";
  }
  if(isValid(rcdt[0][1]) and isValid(rcdt[0][2]))
  {
    testNPN(1);
    return "-1\r\n";
  }
  if(isValid(rcdt[1][0]) and isValid(rcdt[1][2]))
  {
    testNPN(2);
    return "-1\r\n";
  }
  if(isValid(rcdt[2][0]) and isValid(rcdt[2][1]))
  {
    testNPN(3);
    return "-1\r\n";
  }
  
  double rcd[2][3][3]{}; // rcd[0] records the results for testRS and rcd[1] for testRL.

  // Cases for R
  for(register int i=0;i<9;++i)
    if(i%3!=i/3)
    {
      rcd[0][i/3][i%3]=testRS(i/3+1, i%3+1);
      if(rcd[0][i/3][i%3]>=0.2 and rcd[0][i/3][i%3]<4.5)
      {
        disp(String("TP on ")+String(i/3+1)+String("-")+String(i%3+1), 0, 0);
        disp(String("Mode: SR"), 0, 1); // Small R
        disp(String(1.035*1360*rcd[0][i/3][i%3]/(5-rcd[0][i/3][i%3]))+String(" Ohm"), 0, 2);
        return msg;
      }
    }

  // Cases for short
  if(rcd[0][0][1]<0.1 or rcd[0][0][2]<0.1 or rcd[0][1][2]<0.1 or rcd[0][1][0]<0.1 or rcd[0][2][0]<0.1 or rcd[0][2][1]<0.1)
  {
    disp(String("Short"),0, 0), delay(2000);
    return msg;
  }

  for(register int i=0;i<9;++i)
    if(i%3!=i/3)
    {
      rcd[1][i/3][i%3]=testRL(i/3+1, i%3+1);
      if(rcd[1][i/3][i%3]>=0.1 and rcd[1][i/3][i%3]<=4.8)
      {
        disp(String("TP on ")+String(i/3+1)+String("-")+String(i%3+1), 0, 0);
        disp(String("Mode: LR"), 0, 1); // Large R
        disp(String(-8+1.233*940*rcd[1][i/3][i%3]/(5-rcd[1][i/3][i%3]))+String(" kOhm"), 0, 2);
        return msg;
      }
    }
    
  // Cases for C
  if((rcd[0][0][1]>4.5 or rcd[0][1][0]>4.5) and (max(rcd[0][0][1], rcd[0][1][0])>=max(rcd[0][0][2], rcd[0][2][0])) and (max(rcd[0][0][1], rcd[0][1][0])>=max(rcd[0][1][2], rcd[0][2][1])))
    {
      disp(String("TP on ")+String(1)+String("-")+String(2), 0, 0);
      String resultC = testCL(1, 2);
      if(resultC!="")
      {
        disp(resultC, 0, 2);
        delay(2000);
        cd
      }
      return msg;
    }
  if((rcd[0][0][2]>4.5 or rcd[0][2][0]>4.5) and (max(rcd[0][0][2], rcd[0][2][0])>=max(rcd[0][0][1], rcd[0][1][0])) and (max(rcd[0][0][2], rcd[0][2][0])>=max(rcd[0][1][2], rcd[0][2][1])))
    {
      disp(String("TP on ")+String(1)+String("-")+String(3), 0, 0);
      String resultC = testCL(1, 3);
      if(resultC!="")
      {
        disp(resultC, 0, 2);
        delay(2000);
        cd
      }
      return msg;
    }
  if((rcd[0][1][2]>4.5 or rcd[0][2][1]>4.5) and (max(rcd[0][1][2], rcd[0][2][1])>=max(rcd[0][0][2], rcd[0][2][0])) and (max(rcd[0][1][2], rcd[0][2][1])>=max(rcd[0][0][1], rcd[0][1][0])))
    {
      disp(String("TP on ")+String(2)+String("-")+String(3), 0, 0);
      String resultC = testCL(2, 3);
      if(resultC!="")
      {
        disp(resultC, 0, 2);
        delay(2000);
        cd
      }
      return msg;
    }


  // shouldn't reach here
  cd
  disp("Error", 0, 0);
  delay(5000);
  return msg;
}
