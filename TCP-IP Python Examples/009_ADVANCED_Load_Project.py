"""
    Example script for loading a project from the project directory.
    This example serves as an introduction to using the SLSS CANAnalyser TCP/IP Class.

    IMPORTANT: Please ensure that the TCP/IP interface is activated in the SLSS CANAnalyser.
"""
__author__      =   "Sebastian Langer"
__company__     =   "Sebastian Langer Software Solutions UG (haftungsbeschraenkt), SeRoSys Technology LLC"
__credits__     =   "Sebastian Langer"
__dev_date__    =   "2026.10.09"
__version__     =   "1.0.0.0"
__email__       =   "info@langer-sebastian.de, slanger@serosys-tech.com"
__status__      =   "production"
__copyright__   =   "Sebastian Langer @ Sebastian Langer Software Solutions UG (haftungsbeschraenkt)"

""" USER SETTINGS AND SLSS CANANALYSER INITIALIZATION """

import os
from cls.cl_SLSS_CANAnalyser_TCPIP_Interface import CANAnalyserTCPIP    # import the class to the current script
slss_com = CANAnalyserTCPIP("127.0.0.1", 49600, True, True)  # Create an instance using the local host IP (this computer) and port 49600
                                                             # (must match the port set in the SLSS CANAnalyser) with immediate establishment
                                                             # of the connection and activated log output.

""" SLSS CANANALYSER COMMANDS """

cwd = os.getcwd()  # get current working dir
slss_com.disconnect_module()  # Begins by disconnecting a dongle (in case one is already connected)
slss_com.load_project(os.path.join(cwd, r"additional files\SLSS CANAnalyser Example Project\SLSS_CANAnalyser_Project.capf"))  # load the project from the given directory