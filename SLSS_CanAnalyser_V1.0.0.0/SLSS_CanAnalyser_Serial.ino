//Serial communication with SLSS-Software 
void SerialControl(String received) {

  //etablish connection to software
  if(received.indexOf("CAN_AnalyserV1.0") != -1)
  {   
    //wait that actual serial output is done 
    Serial.flush();
    
    //split baudrate
    String baudrate = splitString(received, 'X', 1); 
    
    //send Device-ID to etablish connection --> End with \n important
    Serial.print("CAN-Device-" + devID + " @" + baudrate + "kbit/s\n"); 

    //CAN set new Baudrate
    if(baudrate == "1000")
      CANSpeed = CAN_1000KBPS;
    else if(baudrate == "0500")
      CANSpeed = CAN_500KBPS;
    else if(baudrate == "0250")
      CANSpeed = CAN_250KBPS;
    else if(baudrate == "0200")
      CANSpeed = CAN_200KBPS;        
    else if(baudrate == "0125")
      CANSpeed = CAN_125KBPS;      
    else if(baudrate == "0100")
      CANSpeed = CAN_100KBPS;
    else if(baudrate == "0080")
      CANSpeed = CAN_80KBPS; 
    else if(baudrate == "0050")
      CANSpeed = CAN_50KBPS; 
    else if(baudrate == "0040")
      CANSpeed = CAN_40KBPS; 
    else if(baudrate == "33.3")
      CANSpeed = CAN_33K3BPS;            
    else if(baudrate == "31.25")
      CANSpeed = CAN_31K25BPS;
    else if(baudrate == "0020")
      CANSpeed = CAN_20KBPS;
    else if(baudrate == "0010")
      CANSpeed = CAN_10KBPS;
    else if(baudrate == "0005")
      CANSpeed = CAN_5KBPS;

    //set new baudrate
    CAN_setBaudrate();

    found = true;
  }

  //etablish connection to software
  else if(received.indexOf("CAN_closeCON") != -1)
  {
    found = false;
  }

  //send CAN-data if pulled from SLSS-Software (only if found == true)
  else if(received.indexOf("CAN_getDATA") != -1 && found)
  {
    //Check if sendCAN is empty
    if(sendCAN.length() > 0)
    {    
      //send the Line
      for(int i = 0; i < sendCAN.length(); i++)
        Serial.write(sendCAN[i]);
      
      Serial.write('\n');
    }
    else
    {
      Serial.write('\n');
    }
  }


    //send CAN-Error if pulled from SLSS-Software (only if found == true)
  else if(received.indexOf("CAN_getMEM") != -1 && found)
  {
      //read CAN message
      CAN0.readMsgBuf(&readedId, &CANlength, rdBuffer);
    Serial.print("");
  }


      //reset sendCAN
    sendCAN = "";
    
    //reset received message
    receivedMessage = "";
}
