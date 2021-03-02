#include <SPI.h>
#include <mcp_can.h>

//select frequency of the oszilator on can board
int MCP_MHz = MCP_8MHZ;
//int MCP_MHz = MCP_16MHZ;

//DeviceID --> change for multiple devices
String devID = "001";






//variables for received Messages
char receivedChar;
String receivedMessage;
bool found = false;

//variables for CAN-communication
unsigned char CANlength = 0;
unsigned char rdBuffer[8];
long unsigned int readedId;
String sendCAN, baudrate;
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
  readedId = 0;
  CANlength = 0;
  memset(rdBuffer, 0, sizeof(rdBuffer));

  // check if data coming
  if (CAN_MSGAVAIL == CAN0.checkReceive())
  {
    //read CAN message
    CAN0.readMsgBuf(&readedId, &CANlength, rdBuffer);

    //check if id is plausible and found is true
    if (readedId >= 0 && found)
    {
      //get canData and add it to the String of sendCAN
      String canData;
      for (int i = 0; i < sizeof(rdBuffer); i++)
        canData = canData + rdBuffer[i] + "_";

      //concatenate new received data with former received CAN messages
      sendCAN.concat("C" + String(readedId) + " " + canData + "#");
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
    sendCAN = "";
  }
}
