"""
    Example script for reading a DBC signal value from the grid in the Incoming DBC Signals tab.
    This example serves as an introduction to using the SLSS CANAnalyser TCP/IP Class.

    IMPORTANT: Please ensure that the TCP/IP interface is activated in the SLSS CANAnalyser.
"""
__author__      =   "Sebastian Langer"
__company__     =   "Sebastian Langer Software Solutions UG (haftungsbeschraenkt), SeRoSys Technology LLC"
__credits__     =   "Sebastian Langer"
__dev_date__    =   "2025.09.09"
__version__     =   "1.0.0.0"
__email__       =   "info@langer-sebastian.de, slanger@serosys-tech.com"
__status__      =   "production"
__copyright__   =   "Sebastian Langer @ Sebastian Langer Software Solutions UG (haftungsbeschraenkt)"

""" USER SETTINGS AND SLSS CANANALYSER INITIALIZATION """

import os
from time import sleep
from cls.cl_SLSS_CANAnalyser_TCPIP_Interface import CANAnalyserTCPIP    # import the class to the current script
slss_com = CANAnalyserTCPIP("127.0.0.1", 49600, True, True)  # Create an instance using the local host IP (this computer) and port 49600
                                                             # (must match the port set in the SLSS CANAnalyser) with immediate establishment
                                                             # of the connection and activated log output.

DONGLE_AUTO_DISCOVER = True  # select if the CAN Dongle should be discovered automatically [TRUE] or the following COM port should be used
USED_COM_PORT = 13  # set here the COM-Port of the connected CAN Dongle

""" SLSS CANANALYSER COMMANDS """

cwd = os.getcwd()  # get current working dir
slss_com.disconnect_module()  # Begins by disconnecting a dongle (in case one is already connected)
slss_com.load_project(os.path.join(cwd, r"additional files\SLSS CANAnalyser Example Project\SLSS_CANAnalyser_Project.capf"))  # load the project from the given directory

if DONGLE_AUTO_DISCOVER:  # automatically search connected CAN Dongle
    slss_com.search_module()
else:  # manually connect to Dongle which has is assigned to the specified COM port
    slss_com.connect_module(USED_COM_PORT)

if "COM" + str(USED_COM_PORT) not in slss_com.get_connection():
    print(f"ERROR: No connection to the dongle on COM{USED_COM_PORT} could be established! Please check the selected COM port and start the test again...")
    exit(1)

# NOTE: The following example is based on the loaded DBC files for the SeRoSys CAN FD Injector.
# Please align message and signal names to your messages shown in the Incoming DBC Signals tab!

# read valid message row from SLSS CANAnalyser
for i in range(1,11):
    val = slss_com.get_DBC_value("B", "Vehicle_Messages", "Speed")
    print(val)

    sleep(2)

# read invalid message row and get error reply from SLSS CANAnalyser
for i in range(1,11):
    val = slss_com.get_DBC_value("B", "Wrong_Message", "Speed")
    print(val)

    sleep(2)