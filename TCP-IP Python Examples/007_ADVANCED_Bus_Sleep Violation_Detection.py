"""
    Example script for using the SLSS CANAnalyser TCP/IP interface to monitor a CAN bus (channel A of the connected dongle) and to detect and record bus sleep violations.
    The script uses a simple state machine to first ensure that there is no more communication on the bus. After the bus sleep has been detected, the script starts the SLSS CANAnalyser
    log recorder and waits for new incoming messages.
    If new incoming messages are detected, the bus traffic is recorded for the time specified in “recording_time_s” and the log file is saved in the path specified in “log_file_path”.
    The cycle then starts again (waiting for the bus to go to sleep to start recording) until the number of cycles specified in “detections_before_exit” has been reached.
"""
__author__      =   "Sebastian Langer"
__company__     =   "Sebastian Langer Software Solutions UG (haftungsbeschraenkt), SeRoSys Technology LLC"
__credits__     =   "Sebastian Langer"
__dev_date__    =   "2024.11.12"
__version__     =   "1.0.0.0"
__email__       =   "info@langer-sebastian.de, slanger@serosys-tech.com"
__status__      =   "productive"
__copyright__   =   "Sebastian Langer @ Sebastian Langer Software Solutions UG (haftungsbeschraenkt)"

""" USER SETTINGS AND CANANALYSER INITIALIZATION """

import time
from cls.cl_SLSS_CANAnalyser_TCPIP_Interface import CANAnalyserTCPIP
ip_address = "127.0.0.1"    # define ip address (use 127.0.0.1 for local use)
port = 49600                # define port
slss_com = CANAnalyserTCPIP(ip_address, port, True)  # create instance with immediately establishing the connection but without log output

dongle_com_port = 3         # the COM port of the connected Dongle
recording_time_s = 60       # the recording time in seconds
detections_before_exit = 2  # the amount of state machine loops before exit
bus_check_interval_s = 1    # the interval how often the bus status should be checked
log_file_path = r"C:\_Workspace\CANAnalyser files\Bus_monitoring_example\Bus_sleep_violation.rcdf"

""" NO MORE USER CHANGES UNTIL HERE """

act_time = 0                # variable to store the current time (do not change)
cur_loop = 0                # variable to store the current loop (do not change)
level = 0                   # variable to store the current level of the state machine (do not change)
u_learn_counter = 0         # variable to store the counter to check steps multiple times before changing state (do not change)
check_run_state = True      # variable if run state check should be performed or not

slss_com.unmute_CAN("A")  # un-mute forwarded CAN messages for CAN channel A
slss_com.mute_CAN("B")    # mute forwarded of CAN messages for CAN channel B (not used in this example)

if "COM" + str(dongle_com_port) not in slss_com.get_connection():  # check if Dongle on is connected to the specified COM port
    slss_com.connect_module(dongle_com_port)  # if not connect, then connect

    if "COM" + str(dongle_com_port) not in slss_com.get_connection():
        print(f"ERROR: No connection to the dongle on COM{dongle_com_port} could be established! Please check the selected COM port and start the test again...")
        exit(1)

slss_com.set_channel("A")  # select channel A only to monitor bus sleep on this channel (need to be done after establishing the connection)

while True:  # main infinite loop

    while check_run_state:  # check if run state isn't play (play is necessary for the incoming message detection)
        status = slss_com.get_runstate()  # get current run state

        if "play" not in status:
            print(f"CANAnalyser not in play mode: Try to set bus interaction mode to play and check again in {bus_check_interval_s}s")
            slss_com.set_runstate("play")  # set play mode
            time.sleep(bus_check_interval_s)  # wait interval time
        else:
            check_run_state = False  # set run state check to false, because correct run state was verified
            break

    rcv = slss_com.receive_CAN_message(False, 100)  # search for received CAN messages
    if level == 0:  # level 0 of the state machine --> wait for bus sleep

        if isinstance(rcv, str) and len(rcv) > 0:  # check if a bus message was received
            u_learn_counter = 0  # reset counter to initial value
            print(f"Bus communication is still active! Check bus communication again in {bus_check_interval_s}s")
            slss_com.flush_incoming_data()  # flush message receive buffer
            time.sleep(bus_check_interval_s)  # wait interval time

        elif isinstance(rcv, str):
            if u_learn_counter < 5:  # check if u_learn_counter limit was reached
                u_learn_counter += 1  # increase u_learn_counter
                print(f"No more bus communication detected! Increase counter value to {u_learn_counter}/5 and check bus communication again in {bus_check_interval_s}s")
                time.sleep(bus_check_interval_s)
            else:
                print(f"Counter has reached maximum value and bus is still inactive, change to level 1")
                level = 1

    elif level == 1:  # level 1 of the state machine --> start recording
        slss_com.rec_start()  # start recording CAN traffic
        print(f"Start recording CAN traffic and change to level 2")
        level = 2

    elif level == 2:  # of the state machine --> bus monitoring
        if len(rcv) == 0:  # check if no bus message was received, then sleep is already active
            print(f"Bus still in sleep mode, check bus in {bus_check_interval_s}s again")
            time.sleep(bus_check_interval_s)
        else:
            print(f"ATTENTION: Bus sleep violation detected! Recording of CAN traffic for the next {recording_time_s}s")
            time.sleep(recording_time_s)
            print(f"Stop recording CAN traffic and save logfile to {log_file_path}")
            slss_com.rec_stop(log_file_path, False)  # save the current logfile and do not overwrite existing files

            if cur_loop < detections_before_exit:  # check if state machine should be restarted or program should exit
                print(f"Reset state machine to start next detection loop")
                cur_loop += 1  # increase current loop
                level = 0  # reset state machine
                slss_com.set_runstate("play")
                check_run_state = False
            else:
                print(f"Maximum state machine loops are reached, exit program")
                exit(0)