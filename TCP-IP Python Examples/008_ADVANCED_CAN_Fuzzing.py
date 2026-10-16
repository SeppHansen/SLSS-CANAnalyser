"""
    Example of a quick CAN fuzzing test via the SLSS CANAnalyser TCP/IP interface
"""
__author__      =   "Sebastian Langer"
__company__     =   "Sebastian Langer Software Solutions UG (haftungsbeschraenkt), SeRoSys Technology LLC"
__credits__     =   "Sebastian Langer"
__dev_date__    =   "2025.01.10"
__version__     =   "1.0.0.0"
__email__       =   "info@langer-sebastian.de, slanger@serosys-tech.com"
__status__      =   "productive"
__copyright__   =   "Sebastian Langer @ Sebastian Langer Software Solutions UG (haftungsbeschraenkt)"

""" USER SETTINGS AND SLSS CANANALYSER INITIALIZATION """

import random
import time
from cls.cl_SLSS_CANAnalyser_TCPIP_Interface import CANAnalyserTCPIP
ip_address = "127.0.0.1"    # define ip address (use 127.0.0.1 for local use)
port = 49600                # define port
slss_com = CANAnalyserTCPIP(ip_address, port, True)  # create instance with immediately establishing the connection but without log output

dongle_com_port = 3        # the COM port of the connected Dongle
iMessageInterval_ms = 100  # delay time between two messages

# Dictionary for user defined fuzzing messages

# key:      Provide a numeric value or string. Use a string with the flag "RAND" to create random id's within the range of CAN2.0 A/B.
#           To predefine the range of used ids, add underscore separated minimum and maximum values behind the RAND flag ("RAND_0_10", "RAND_25_1000", etc.)

# value:    Provide a list with 3 items.
# item 1:   numeric value of message generation loops with the given id and settings. Insert -1 to infinite loop this test setup
# item 2:   string value of message type identifiers. Add [EXT],[FD],[BRS] to specify the message type you would use for the execution
# item 3:   list of byte values. Each byte value provides different fuzzing methods.
#           The 5 main methods are:
#               - numeric value: to send a fix numeric value on this position
#               - string "RAND": to send a random byte value in the range between 0 and 255
#               - string "INC": increase the byte value stepwise from 0 to 255 and restart if 255 is reached
#               - string "DEC": decrease the byte value stepwise from 255 to 0 and restart if 0 is reached
#               - dictionary:   A dictionary with the manipulation method ("RAND", "INC", "DEC") as key and a list with two numerical values as minimum and
#                               maximum range values. The method only uses values in this range

dFuzzMessages = {
        "RAND": [-1, "[EXT]", ["RAND", "RAND", "RAND", "RAND", "RAND", "RAND", "RAND", "RAND"]]
    }

""" NO MORE USER CHANGES UNTIL HERE """

dOldDataStore = {}


def get_rand_num(i_min=0, i_max=255):
    """ get a random number in range of i_min and i_max"""
    i_min = 0 if i_min < 0 else i_min
    i_max = 255 if i_max > 255 else i_max
    rand_num = random.randint(i_min, i_max)
    return rand_num


def get_rand_id(is_extended, i_min=0, i_max=536870911):
    """ get a random ID in range of standard or extended id """
    maxID = 2047 if not is_extended else 536870911
    i_min = 0 if i_min < 0 else i_min
    i_max = i_max if i_max < maxID else maxID
    rand_id = random.randint(i_min, i_max)
    return rand_id


if __name__ == '__main__':
    slss_com.mute_CAN("AB")  # mute forwarded CAN messages for both CAN channels (not necessary in this example)

    if "COM" + str(dongle_com_port) not in slss_com.get_connection():  # check if Dongle on is connected to the specified COM port
        slss_com.connect_module(dongle_com_port)  # if not connect, then connect

        if "COM" + str(dongle_com_port) not in slss_com.get_connection():
            print(f"ERROR: No connection to the dongle on COM{dongle_com_port} could be established! Please check the selected COM port and start the test again...")
            exit(1)

    slss_com.set_channel("AB")  # select channel A only to monitor bus sleep on this channel (need to be done after establishing the connection)

    for hId, lMsg in dFuzzMessages.items():  # iterate over CAN id / message values
        if len(lMsg) != 3:  # data length check for value list
            print(f"Value length error in message {str(hId)}!")
        else:
            bInfiniteFlag = True if lMsg[0] == -1 else False  # detect infinite loop value and set to start value
            lMsg[0] = 1 if lMsg[0] == -1 else lMsg[0]  # detect infinite loop value and set to start value
            cnt = 0
            while cnt < lMsg[0]:  # run until max value is reached
                lCANDataPayload = []  # variable to build send list out of message values
                for iBytePos in range(0, len(lMsg[2])):
                    if isinstance(lMsg[2][iBytePos], int):  # when a static numerical value is used

                        lCANDataPayload.append(lMsg[2][iBytePos])

                    elif isinstance(lMsg[2][iBytePos], str):  # when a string is used, check for commands

                        if lMsg[2][iBytePos].upper() == "RAND":  # when using random byte values
                            lCANDataPayload.append(get_rand_num())

                        elif lMsg[2][iBytePos].upper() == "INC":  # when incrementing a byte value
                            if hId in dOldDataStore:  # check if a k/v pair is already stored in data store
                                num = dOldDataStore[hId][iBytePos]
                                num = num + 1 if num < 255 else 0  # check if in range, else reset to 0
                                lCANDataPayload.append(num)
                            else:
                                lCANDataPayload.append(0)

                        elif lMsg[2][iBytePos].upper() == "DEC":  # when decrementing a byte value
                            if hId in dOldDataStore:  # check if a k/v pair is already stored in data store
                                num = dOldDataStore[hId][iBytePos]
                                num = num - 1 if num > 0 else 255  # check if in range, else reset to 255
                                lCANDataPayload.append(num)
                            else:
                                lCANDataPayload.append(255)

                    elif isinstance(lMsg[2][iBytePos], dict):
                        if "RAND" in str(lMsg[2][iBytePos].keys()).upper():
                            if isinstance(lMsg[2][iBytePos]["RAND"], list):
                                startValue = lMsg[2][iBytePos]["RAND"][0]
                                endValue = lMsg[2][iBytePos]["RAND"][1]
                                if startValue > endValue:
                                    tempStartValue = startValue
                                    startValue = endValue
                                    endValue = tempStartValue

                                num = get_rand_num(startValue, endValue)
                                lCANDataPayload.append(num)

                        elif "INC" in str(lMsg[2][iBytePos].keys()).upper():
                            if isinstance(lMsg[2][iBytePos]["INC"], list):
                                startValue = lMsg[2][iBytePos]["INC"][0]
                                endValue = lMsg[2][iBytePos]["INC"][1]
                                if endValue < startValue:
                                    tempStartValue = startValue
                                    startValue = endValue
                                    endValue = tempStartValue
                                if hId in dOldDataStore:  # check if a k/v pair is already stored in data store
                                    num = dOldDataStore[hId][iBytePos]
                                    num = num + 1 if num < endValue else startValue  # check if in range, else reset to 0
                                    lCANDataPayload.append(num)
                                else:
                                    lCANDataPayload.append(startValue)

                        elif "DEC" in str(lMsg[2][iBytePos].keys()).upper():
                            if isinstance(lMsg[2][iBytePos]["DEC"], list):
                                startValue = lMsg[2][iBytePos]["DEC"][0]
                                endValue = lMsg[2][iBytePos]["DEC"][1]
                                if endValue > startValue:
                                    tempStartValue = startValue
                                    startValue = endValue
                                    endValue = tempStartValue
                                if hId in dOldDataStore:  # check if a k/v pair is already stored in data store
                                    num = dOldDataStore[hId][iBytePos]
                                    num = num - 1 if num > endValue else startValue  # check if in range, else reset to 0
                                    lCANDataPayload.append(num)
                                else:
                                    lCANDataPayload.append(startValue)

                dOldDataStore[hId] = lCANDataPayload
                cnt = 0 if bInfiniteFlag else cnt + 1  # detect infinite loop value and set to back to start value if necessary

                bExtIdent = True if "EXT" in lMsg[1] else False
                bFDMsg = True if "FD" in lMsg[1] else False
                bBRSused = True if "BRS" in lMsg[1] else False
                sCANDataPayload = "_".join(str(val) for val in lCANDataPayload)

                # check for ID manipulation
                iSendId = None
                if isinstance(hId, int):
                    iSendId = hId
                elif isinstance(hId, str) and "RAND" in hId.upper():
                    if hId.count('_') > 0:
                        iMinMaxValues = hId.split('_')
                        iSendId = get_rand_id(bExtIdent, int(iMinMaxValues[1]), int(iMinMaxValues[2]))
                    else:
                        iSendId = get_rand_id(bExtIdent)
                else:
                    continue

                slss_com.send_CAN_message("AB", iSendId, lCANDataPayload, bExtIdent, bFDMsg, bBRSused)
                time.sleep(iMessageInterval_ms / 1000)