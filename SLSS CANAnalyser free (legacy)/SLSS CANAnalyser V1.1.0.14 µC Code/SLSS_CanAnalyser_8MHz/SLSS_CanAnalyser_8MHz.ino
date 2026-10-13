/*
SLSS CANAnalyser µC Code
- This µc-code is neccessary for establishing serial connection via SLSS CANAnalyser
   
Author:     Sebastian Langer
Web:        https://www.langer-sebastian.de/slss-cananalyser/
Version:    1.0.2.1
Changelog:  2022.09.06  sla   change rx and tx communication to variable can telegram length 
            2022.09.06  sla   add version check for right µc code version
            2022.10.15  sla   change position of variable found to fix start connection problems on incoming data
            2022.11.01  sla   change data queue from string to char array to avoid memory issues
            
*/
#include <SPI.h>
#include <mcp_can.h>

//select frequency of the oszilator on mounted on the can board
int MCP_MHz = MCP_8MHZ;
// int MCP_MHz = MCP_16MHZ;

//DeviceID --> change for multiple devices (shown as ID in software)
String devID = "001";


//variables for received Messages
char receivedChar;
String receivedMessage;
bool found = false;
String codeVersion = "1021"; // 1021 = 1.0.2.1

//variables for CAN-communication
unsigned char CANlength = 0;
unsigned char rdBuffer[8];
unsigned char sendCAN[512];
long unsigned int readedId;
String baudrate, extIdent;
unsigned int CANSpeed;


//Chip Select for CAN module
MCP_CAN CAN0(10);
int CAN_ReceivePin = 2;

void setup() {
  //set serial speed (115200 for SLSS CANAnalyser communication)
  Serial.begin(115200);

  //set pins for status-led 
  pinMode(7, OUTPUT);

  //CAN Receive PIN
  pinMode(CAN_ReceivePin, INPUT);
}

//programm loop
void loop() {

  //(re-)initialize variables for CAN communication
  readedId = -1;
  CANlength = 0;
  memset(rdBuffer, 0, sizeof(rdBuffer));

  // check if data coming and found is true
  if (CAN_MSGAVAIL == CAN0.checkReceive() && found)
  {
    //read CAN message
    CAN0.readMsgBuf(&readedId, &CANlength, rdBuffer);

    //extended identifier flag for SLSS CANAnalyser
    extIdent = ""; 
    
    //check if extended id format is used
    if ((readedId & 0x80000000) == 0x80000000)
    {
      readedId = readedId & 0x1FFFFFFF;
      extIdent = "*";
    }

    //check if id is plausible 
    if (readedId >= 0)
    {    
      //get canData and add it to the String of sendCAN
      String canData;
      for (int i = 0; i < CANlength; i++)
        canData = canData + rdBuffer[i] + "_";

      //create complete send frame
      canData = ("C" + String(readedId) + " " + canData + " " + extIdent + "#");        

      //concatenate new received data with former received CAN messages if enough place left in buffer 
      if(strlen(sendCAN) + canData.length() < sizeof(sendCAN))
        strcat(sendCAN, (canData).c_str());
      
    }
  }

  //read via ComPort received messages
  while (Serial.available())
  {
    receivedMessage = Serial.readStringUntil('\n');
  }

  //if message received, do some action
  if (receivedMessage != "")
  {
    //handle serial communication with software
    SerialControl(receivedMessage);
  }

  //indicate etablished connection with blinking led
  if (found)
  {
    if (millis() % 1000 < 500)
    {
      digitalWrite(7, HIGH);
    }
    else
    {
      digitalWrite(7, LOW);
    }
  }
  else
  {
    digitalWrite(7, LOW);
          
    //reset sendCAN
    memset(sendCAN, 0, 512);
  }

}
