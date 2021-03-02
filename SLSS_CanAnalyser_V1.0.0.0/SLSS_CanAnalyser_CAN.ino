
//Set new CAN Baudrate
void CAN_setBaudrate()
{
    //set CAN Baudrate
    CAN0.begin(MCP_ANY, CANSpeed, MCP_MHz);
    CAN0.setMode(MCP_NORMAL);
}
