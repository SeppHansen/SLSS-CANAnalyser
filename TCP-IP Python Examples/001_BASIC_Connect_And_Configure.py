"""
    Example script for establishing a connection to the SLSS CANAnalyser software and for manipulating some basic settings in the program.
    This example serves as an introduction to using the SLSS CANAnalyser TCP/IP Class.

    IMPORTANT: Please ensure that the TCP/IP interface is activated in the SLSS CANAnalyser.
"""
__author__      =   "Sebastian Langer"
__company__     =   "Sebastian Langer Software Solutions UG (haftungsbeschraenkt), SeRoSys Technology LLC"
__credits__     =   "Sebastian Langer"
__dev_date__    =   "2024.09.15"
__version__     =   "1.0.0.0"
__email__       =   "info@langer-sebastian.de, slanger@serosys-tech.com"
__status__      =   "production"
__copyright__   =   "Sebastian Langer @ Sebastian Langer Software Solutions UG (haftungsbeschraenkt)"

""" USER SETTINGS AND SLSS CANANALYSER INITIALIZATION """

from cls.cl_SLSS_CANAnalyser_TCPIP_Interface import CANAnalyserTCPIP    # import the class to the current script
slss_com = CANAnalyserTCPIP("127.0.0.1", 49600, True, True)  # Create an instance using the local host IP (this computer) and port 49600
                                                             # (must match the port set in the SLSS CANAnalyser) with immediate establishment
                                                             # of the connection and activated log output.

""" SLSS CANANALYSER COMMANDS """

slss_com.set_FD_custom_state("AB", False)  # deactivate the FD custom settings

slss_com.set_FD_active_state("AB", False)  # set FD active state to False to use standard CAN 2.0 only

slss_com.set_speed("A", "500")  # set CAN speed of channel A to 500kbit/s
slss_com.set_speed("B", "250")  # set CAN speed of channel B to 250kbit/s

slss_com.set_mode("AB", "normal")  # set bus interaction mode for both bus channels to normal

slss_com.unmute_CAN("A")  # un-mute CAN channel A
slss_com.mute_CAN("B")  # mute CAN channel B

slss_com.search_module()  # search for connected module

if "not connected" in slss_com.get_connection():  # check if a dongle connection could be established
    print("ERROR: No Dongle connection could be established --> execution aborted!")
    exit(1)
else:
    print("Well done! The settings have been set and the connection to the Dongle has been successfully established!")