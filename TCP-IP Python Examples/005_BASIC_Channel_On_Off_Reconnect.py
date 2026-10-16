"""
    Example script for establishing a connection to the SLSS CANAnalyser software
    and demonstrates changing the bus interaction mode from Channel A to Channel B.
    This example serves as an introduction to using the SLSS CANAnalyser TCP/IP Class.

    IMPORTANT: Please ensure that the TCP/IP interface is activated in the SLSS CANAnalyser.
"""
__author__      =   "Sebastian Langer"
__company__     =   "Sebastian Langer Software Solutions UG (haftungsbeschraenkt), SeRoSys Technology LLC"
__credits__     =   "Sebastian Langer"
__dev_date__    =   "2025.01.20"
__version__     =   "1.0.0.0"
__email__       =   "info@langer-sebastian.de, slanger@serosys-tech.com, rzlotnik@serosys-tech.com"
__status__      =   "production"
__copyright__   =   "Sebastian Langer @ Sebastian Langer Software Solutions UG (haftungsbeschraenkt)"

""" USER SETTINGS AND SLSS CANANALYSER INITIALIZATION """

import time
from cls.cl_SLSS_CANAnalyser_TCPIP_Interface import CANAnalyserTCPIP    # import the class to the current script
slss_com = CANAnalyserTCPIP("127.0.0.1", 49600, True, True)  # Create an instance using the local host IP (this computer) and port 49600
                                                             # (must match the port set in the SLSS CANAnalyser) with immediate establishment
                                                             # of the connection and activated log output.

DONGLE_AUTO_DISCOVER = True  # select if the CAN Dongle should be discovered automatically [TRUE] or the following COM port should be used
USED_COM_PORT = 13  # set here the COM-Port of the connected CAN Dongle

""" SLSS CANANALYSER COMMANDS """

slss_com.disconnect_module()  # Begins by disconnecting a dongle (in case one is already connected)

slss_com.set_FD_custom_state("AB", False)  # Deactivate the FD custom settings

slss_com.set_FD_active_state("AB", False)  # set FD active state to False for use of CAN 2.0

slss_com.set_speed("A", "500")  # set CAN speed of channel A to 500kbit/s
slss_com.set_speed("B", "500")  # set CAN speed of channel B to 500kbit/s

slss_com.set_mode("A", "normal")  # set bus interaction mode for channel A to normal
slss_com.set_mode("B", "off")  # set bus interaction mode for channel B to off

slss_com.unmute_CAN("AB")  # unmute CAN channels A and B and show received CAN traffic over TCP/IP

if DONGLE_AUTO_DISCOVER:  # automatically search connected CAN Dongle
    slss_com.search_module()
else:  # manually connect to Dongle which has is assigned to the specified COM port
    slss_com.connect_module(USED_COM_PORT)

slss_com.set_runstate("play")

if "not connected" in slss_com.get_connection():  # check if a dongle connection could be established
    print("ERROR: No Dongle connection could be established --> execution aborted!")
    exit(1)
else:
    print("Well done! The settings have been set and the connection to the Dongle has been successfully established!")

print("Beginning a 5 second delay until disconnecting and reconnecting with different settings")
time.sleep(5)  # Delay for 5 seconds.

slss_com.disconnect_module()  # Begins by disconnecting a dongle (in case one is already connected)

slss_com.set_FD_custom_state("AB", False)  # Deactivate the FD custom settings

slss_com.set_FD_active_state("AB", False)  # set FD active state to False for use of CAN 2.0

slss_com.set_speed("A", "500")  # set CAN speed of channel A to 500kbit/s
slss_com.set_speed("B", "500")  # set CAN speed of channel B to 500kbit/s

slss_com.set_mode("B", "normal")  # set bus interaction mode for channel B to normal
slss_com.set_mode("A", "off")  # set bus interaction mode for channel A to off

slss_com.mute_CAN("AB")  # mute CAN channels A and B

if DONGLE_AUTO_DISCOVER:  # automatically search connected CAN Dongle
    slss_com.search_module()
else:  # manually connect to Dongle which has is assigned to the specified COM port
    slss_com.connect_module(USED_COM_PORT)

slss_com.set_runstate("play")

if "not connected" in slss_com.get_connection():  # check if a dongle connection could be established
    print("ERROR: No Dongle connection could be established --> execution aborted!")
    exit(1)
else:
    print("Well done! The settings have been set and the connection to the Dongle has been successfully established!")