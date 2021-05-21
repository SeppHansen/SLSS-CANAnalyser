//Set new CAN Baudrate
void CAN_setBaudrate()
{
    //set CAN Baudrate
    if(CAN0.begin(MCP_ANY, CANSpeed, MCP_MHz) == CAN_OK)
      Serial.println("CAN Connection etablished");
    else
       Serial.println("Error CAN Connection");   
    CAN0.setMode(MCP_NORMAL);
}
