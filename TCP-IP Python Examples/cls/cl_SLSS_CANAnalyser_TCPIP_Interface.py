import socket
import time
import datetime
import select


class CANAnalyserTCPIP:
    """ A basic python class to use the standard communication methods of the SLSS CANAnalyser TCP/IP interface """
    sck = None
    ip_address = None
    debug_output = False
    port = None
    chA_muted = False
    chA_muted_save = False
    chB_muted = False
    chB_muted_save = False

    """
    MAIN CONNECTION IMPLEMENTATIONS
    """

    def __init__(self, ip_address: str, port: int, connect=False, debug_output=False):
        """ Create a new instance and setup the TCP/IP connection by the given parameters

            Args:
                ip_address (string) : The IP address or hostname of the target system where the SLSS CANAnalyser software TCP/IP server is running
                port (int) : The opened port of the CANAnalyser TCP/IP server
                connect (bool) : [optional/default=False] The indicator if the server connection should be established when the instance is created (False) or gets established manually (False)
                debug_output (bool) : [optional/default=False] The indicator if the debug log output should be printed to the console (True) or not (False)

            Example:
                slss_com = CANAnalyserTCPIP("127.0.0.1", 49836, True, False)

        """
        self.ip_address = ip_address
        self.port = port
        self.set_debug_mode(True) if debug_output else self.set_debug_mode(False)
        self.establish_connection() if connect else None
      
    def establish_connection(self):
        """ Establish the TCP/IP connection to the SLSS CANAnalyser software manually after the instance was created without doing it.
            Please make sure that the Server in the software was started before!
        """
        try:
            self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sck.settimeout(10)
            self.sck.connect((self.ip_address, self.port))
            self.sck.setblocking(False)            
            self.log_output(1, f"TCP/IP connection established to {self.ip_address} on port {self.port}")

        except socket.error as e:
            self.log_output(0, f"Could not establish TCP/IP connection to {self.ip_address} on port {self.port}. Check the settings and if the TCP/IP interface is active in the CANAnalyser software!\nError msg: {str(e)}")
			

    def close_connection(self):
        """ Close the TCP/IP connection to the SLSS CANAnalyser software """
        if not self.sck:
            self.log_output(0, "No connection to close!")
            return

        try:
            self.sck.close()
            self.log_output(1, f"TCP/IP connection closed to {self.ip_address} on port {self.port}")
        except socket.error as e:
            self.log_output(0, f"Could not close TCP/IP connection to {self.ip_address} on port {self.port}!\nError msg: {str(e)}")

    def flush_incoming_data(self):
        """ Flush the receive buffer to remove all incoming TCP/IP data """
        while True:
            try:
                chunk = self.sck.recv(1024)
            except BlockingIOError:
                break

    """
    MAIN SENDING AND RECEIVING COMMANDS
    """

    def send_CAN_message(self, channel: str, id_decimal: int, payload_decimal: list, is_extended=False, is_fd_message=False, is_fd_bit_rate_switch=False):
        """ Send a CAN / CAN FD message via the TCP/IP interface

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                id_decimal (int) : The can message arbitration id in decimal notation
                payload_decimal (list) : The CAN data payload as list of decimal numbers (0-255)
                is_extended (bool) : [optional/default=False] The indicator if the message is send with extended arbitration id (True) or not (False)
                is_fd_message (bool) : [optional/default=False] The indicator if the message is send as CAN FD message (True) or not (False)
                is_fd_bit_rate_switch (bool) : [optional/default=False] The indicator if the message should use the CAN FD bit rate switch (True) or not (False)

            Example:
                slss_com.send_CAN_message("AB", 10, [0, 10, 20, 30, 40, 50, 60, 70])                            send a standard CAN message (not extended) on CAN channel A and B to arb. Id 10
                slss_com.send_CAN_message("AB", 20, [0, 10, 20, 30, 40, 50, 60, 70], True)                      send a extended CAN message on CAN channel A and B to arb. Id 20
                slss_com.send_CAN_message("AB", 30, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], True, True)         send a extended FD message without bit rate switch on CAN channel A and B to arb. Id 30
                slss_com.send_CAN_message("AB", 40, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], False, True, True)  send a bit rate switched CAN FD message on CAN channel A and B to arb. Id 40
        """
        if not all(0 <= byte <= 255 for byte in payload_decimal):
            raise ValueError("Payload must contain integers between 0 and 255.")

        payload = "_".join(str(x) for x in payload_decimal)
        is_fd_message = True if len(payload_decimal) > 8 else is_fd_message
        payload = payload.rstrip() if not is_extended else payload.rstrip() + " *"
        payload = payload + " %1" if not is_fd_message and not is_fd_bit_rate_switch else payload
        payload = payload + " %2" if is_fd_message and not is_fd_bit_rate_switch else payload
        payload = payload + " %3" if is_fd_bit_rate_switch else payload
        message = f"SEND_{channel}:{str(id_decimal)} {payload}#"
        debug_text = ""

        if self.debug_output:
            debug_text = "[EXT]" if is_extended else debug_text
            debug_text = debug_text + "[FD]" if is_fd_message else debug_text
            debug_text = debug_text + "[BRS]" if is_fd_bit_rate_switch else debug_text

        try:
            self.sck.send(message.encode())
            self.log_output(1, f"Send {debug_text} CAN message {str(payload_decimal)} send to id {str(id_decimal)}")
        except socket.error as e:
            self.log_output(0, f"Could not send {debug_text} CAN message {str(payload_decimal)} to id {str(id_decimal)}. Check the given data and/or the TCP/IP connection and try again!\nError msg: {str(e)}")

    def send_DBC_message(self, channel: str, message_name: str, signal_name: str, value: float, send_message=True):
        """ Set the value of a DBC message / signal row in the DBC Send tab and optionally send the signal to the bus
            Note: The message must be available in the grid.
            Hint: You can use the project load function to load a project with included DBC send list!

            Args:
                channel (string) : The destination CAN channel (A, B, AB). The channel must match the selected CAN channel in the corresponding grid row!
                message_name (string) : The name of the DBC message available int the DBC send grid
                signal_name (string) : The name of the DBC signal available int the DBC send grid
                value (float) : The value of the DBC signal which is set to the corresponding message / signal row
                send_message (bool) : [optional/default=True] The indicator if the message should be sent to the bus after the value was set

            Example:
                slss_com.send_DBC_message("A", "my_CAN_Message_1", "my_CAN_Signal_1", 12.45)         search for the message / signal combination, set the value to 12.45 and send the message to the bus
                slss_com.send_DBC_message("A", "my_CAN_Message_1", "my_CAN_Signal_1", 12.45, False)  search for the message / signal combination and set the value to 12.45 without sending the message to the bus
                slss_com.send_DBC_message("A", "my_CAN_Message_1", "my_CAN_Signal_1", 12.45, False, True)  search for the message / signal combination and set the value to 12.45 without sending the message to the bus but updating for later usage

        """
        do_send = "1" if send_message else "0"
        message = f"DBC_SIGNAL:{channel}||{message_name}||{signal_name}||{str(value)}||{do_send}#"

        try:
            self.sck.send(message.encode())
            if send_message:
                self.log_output(1, f"Set DBC signal {signal_name} of message {message_name} to {str(value)} and send message to the bus")
            else:
                self.log_output(1, f"Set DBC signal {signal_name} of message {message_name} to {str(value)} without sending message to the bus")
        except socket.error as e:
            self.log_output(0, f"Could not send DBC signal {signal_name} of message {message_name}. Check the given data and/or the TCP/IP connection and try again!\nError msg: {str(e)}")

    def receive_CAN_message(self, return_as_dict_list=False, buffer_size=4096):
        """ Receive CAN messages via the TCP/IP interface

            Args:
                return_as_dict_list (bool) : [optional/default=False] The indicator if the message information should be returned as list of dictionaries (True) or as string (False)
                buffer_size (int) : [optional/default=4096] The size of the receive buffer

            Return:
                (string)/(dictionary) : The received CAN messages forwarded by the SLSS CANAnalyser software as string or list of dictionaries
        """
        if not self.sck:
            self.log_output(0, "No active connection to receive CAN messages.")
            return [] if return_as_dict_list else ""

        retVal = ""
        retList = []
        try:
            self.sck.setblocking(False)
            data = self.sck.recv(buffer_size)

            if data:
                dataList = data.decode()

                for value in dataList.split('\n'):
                    if not value.startswith("A:") and not value.startswith("B:") and not value.startswith("SNDA:") and not value.startswith("SNDB:") and "%" not in value:
                        continue

                    msgType = "[EXT]" if "*" in value else ""
                    msgType = msgType + "[FD]" if "%2" in value else msgType
                    msgType = msgType + "[FD][BRS]"if "%3" in value else msgType
                    value = value.replace("%1", "").replace("%2", "").replace("%3", "").replace("*", "").replace(" t:", "").replace(":", " " + msgType + " ")

                    if return_as_dict_list:
                        data_list = value.split(" ")
                        dataDict = {}
                        dataDict["channel"] = data_list[0]
                        dataDict["type"] = data_list[1]
                        dataDict["id"] = data_list[2]
                        dataDict["data"] = data_list[3].replace("_", " ").strip()
                        dataDict["timestamp"] = data_list[5]
                        retList.append(dataDict)
                    else:
                        if value.strip() != "":
                            retVal += value.strip() + "\n"

                self.log_output(1, f"Received CAN message stream {str(retVal)}")

        except BlockingIOError:
            pass  # no message available
        except Exception as e:
            self.log_output(0, f"Could not receive any CAN messages!\nError msg: {str(e)}")  # all other errors

        return retVal if not return_as_dict_list else retList

    """ CAN BUS SETUP """

    def mute_CAN(self, channel: str):
        """ Mute the forwarding of received CAN messages to the TCP/IP connection for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)

            Example:
                slss_com.mute_CAN("A")  mute forwarding of CAN messages for CAN channel A
                slss_com.mute_CAN("B")  mute forwarding of CAN messages for CAN channel B
                slss_com.mute_CAN("AB")  mute forwarding of CAN messages for CAN channel A & B
        """
        chn = "CAN" if channel == "AB" else channel
        cmd = f"MUTE_{chn}||{str(self.port)}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Mute CAN channel {channel}")

            if channel == "A":
                self.chA_muted = True
            elif channel == "B":
                self.chB_muted = True
            elif channel == "AB":
                self.chA_muted = True
                self.chB_muted = True

        except Exception:
            self.log_output(0, f"Could not mute CAN channel {channel}")

    def unmute_CAN(self, channel: str):
        """ Unmute the forwarding of received CAN messages to the TCP/IP connection for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)

            Example:
                slss_com.unmute_CAN("A")  unmute forwarding of CAN messages for CAN channel A
                slss_com.unmute_CAN("B")  unmute forwarding of CAN messages for CAN channel B
                slss_com.unmute_CAN("AB")  unmute forwarding of CAN messages for CAN channel A & B
        """
        chn = "CAN" if channel == "AB" else channel
        cmd = f"UNMUTE_{chn}||{str(self.port)}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Unmute CAN channel {channel}")

            if channel == "A":
                self.chA_muted = False
            elif channel == "B":
                self.chB_muted = False
            elif channel == "AB":
                self.chA_muted = False
                self.chB_muted = False

        except Exception:
            self.log_output(0, f"Could not unmute CAN channel {channel}")

    def set_speed(self, channel: str, speed: str):
        """ Set the CAN arbitration speed via the TCP/IP connection for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                speed (string) : The speed value of the CAN arbitration speed. ("1000", "500", "250", "200", "125", "100", "80", "50", "40", "33.3", "31.25", "20", "10", "5")

            Example:
                slss_com.set_speed("AB", "250")  set both bus channels to 250kbit/s
                slss_com.set_speed("A", "500")   set bus channel A to 500kbit/s
                slss_com.set_speed("B", "500")   set bus channel B to 500kbit/s
        """
        cmd = f"SET_SPEED||{channel}||{speed}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set arbitration speed for CAN channel {channel} to {speed}kbit/s")
        except Exception:
            self.log_output(0, f"Could not set arbitration speed for CAN channel {channel}")

    def set_FD_active_state(self, channel: str, active: bool):
        """ Activate or deactivate CAN FD usage via the TCP/IP connection for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                active (bool) : The indicator if CAN FD is activated (True) or deactivated (False) for the given channel

            Example:
                slss_com.set_FD_active_state("A", True)     activate CAN FD usage for channel A
                slss_com.set_FD_active_state("B", True)     activate CAN FD usage for channel B
                slss_com.set_FD_active_state("AB", False)   deactivate CAN FD usage for both channels
        """
        state = "0" if not active else "1"
        cmd = f"SET_FD_ACTIVESTATE||{channel}||{state}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set CAN FD active state for CAN channel {channel} to {str(active)}")
        except Exception:
            self.log_output(0, f"Could not set CAN FD active state for CAN channel {channel}")

    def set_FD_multiplicator(self, channel: str, multiplicator: int):
        """ Set the CAN FD data speed multiplicator value for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                multiplicator (int) : The multiplicator value for the data bitrate. (1, 2, 3, 4, 5, 6, 8, 10)

            Example:
                slss_com.set_FD_multiplicator("A", 6)    set multiplicator value for channel A to 6 (6 times of the current arbitration speed)
                slss_com.set_FD_multiplicator("B", 8)    set multiplicator value for channel B to 8 (8 times of the current arbitration speed)
                slss_com.set_FD_multiplicator("AB", 4)   set multiplicator value for both channels to 4 (4 times of the current arbitration speed)
        """
        cmd = f"SET_FD_MULTIPLICATOR||{channel}||{str(multiplicator)}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set CAN FD data bitrate multiplicator for CAN channel {channel} to {str(multiplicator)}")
        except Exception:
            self.log_output(0, f"Could not set CAN FD bitrate multiplicator for CAN channel {channel}")

    def set_FD_custom_state(self, channel: str, active: bool):
        """ Activate or deactivate the CAN FD custom setting usage via the TCP/IP connection for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                active (bool) : The indicator if CAN FD custom settings are activated for the given channel

            Example:
                slss_com.set_FD_custom_state("A", True)     activate CAN FD custom settings usage for channel A
                slss_com.set_FD_custom_state("B", True)     activate CAN FD custom settings usage for channel B
                slss_com.set_FD_custom_state("AB", False)   deactivate CAN FD custom settings usage for both channels
        """
        state = "0" if not active else "1"
        cmd = f"SET_FD_CUSTOMSTATE||{channel}||{state}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set CAN FD custom setting usage for CAN channel {channel} to {str(active)}")
        except Exception:
            self.log_output(0, f"Could not set CAN FD custom setting usage for CAN channel {channel}")

    def set_FD_custom_settings(self, channel: str, clk_frequency: str, PSEG1_arb: int, PSEG2_arb: int, sync_jump_width_arb: int, trans_delay_compensation: int, prescaler_arb: int, prescaler_data: int, PSEG1_data: int, PSEG2_data: int, sync_jump_width_data: int):
        """ Set the CAN FD custom connection values via the TCP/IP connection for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                clk_frequency (string) : The clock frequency of the CAN transceiver. ("100", "80", "50", "48", "40", "33.33", "32", "25")
                PSEG1_arb (int) : The PSEG1 value for the arbitration part
                PSEG2_arb (int) : The PSEG2 value for the arbitration part
                sync_jump_width_arb (int) : The sync jump width for the arbitration part
                trans_delay_compensation (int) : The transceiver delay compensation
                prescaler_arb (int) : The prescaler value for the arbitration part
                prescaler_data (int) : The prescaler value for the data part
                PSEG1_data (int) : The PSEG1 value for the data part
                PSEG2_data (int) : The PSEG2 value for the data part
                sync_jump_width_data (int) : The sync jump width for the data part

            Example:
                slss_com.set_FD_custom_settings("A", "80", 119, 40, 40, 8, 4, 2, 14, 5, 5)
                slss_com.set_FD_custom_settings("B", "80", 119, 40, 40, 8, 2, 4, 14, 5, 5)
                slss_com.set_FD_custom_settings("AB", "80", 119, 40, 40, 8, 1, 1, 14, 5, 5)
        """
        cmd = f"SET_FD_CUSTOMSETTINGS||{channel}||{clk_frequency}||{PSEG1_arb}||{PSEG2_arb}||{sync_jump_width_arb}||{trans_delay_compensation}||{prescaler_arb}||{prescaler_data}||{PSEG1_data}||{PSEG2_data}||{sync_jump_width_data}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set CAN FD custom settings for CAN channel {channel}")
        except Exception:
            self.log_output(0, f"Could not set CAN FD custom settings for CAN channel {channel}")

    def set_mode(self, channel: str, mode: str):
        """ Set the bus interaction mode for one or both channels

            Args:
                channel (string) : The destination CAN channel (A, B, AB)
                mode (string) : The bus interaction mode of the given channel. ("normal", "read-only", "off")

            Example:
                slss_com.set_mode("AB", "normal")        set both bus channels to normal interaction mode
                slss_com.set_mode("A", "listen-only")    set bus channel A to listen only mode
                slss_com.set_mode("B", "off")            set bus channel B to off (deactivates transceiver)
        """
        cmd = f"SET_MODE||{channel}||{mode}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set bus interaction mode for CAN channel {channel} to {mode}")
        except Exception:
            self.log_output(0, f"Could not set bus interaction mode for CAN channel {channel}")

    def set_channel(self, channel: str):
        """ Select the monitored bus channel in the SLSS CANAnalyser software

            Args:
                channel (string) : The destination CAN channel (A, B, AB)

            Example:
                slss_com.set_channel("A")    monitor bus channel A only
                slss_com.set_channel("B")    monitor bus channel B only
                slss_com.set_channel("AB")   monitor both bus channels simultaneously
        """
        cmd = f"SET_CHANNEL||{channel}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set CAN channel {channel} as selected channel")
        except Exception:
            self.log_output(0, f"Could not set CAN channel {channel} as selected CAN channel")
            
    def set_id_format(self, format_short_text: str):
        """ Set the arbitration id notation format in the SLSS CANAnalyser software

            Args:
                format_short_text (string) : The short-text of the used arbitration id notation (hex, dec, bin) as string

            Example:
                slss_com.set_id_format("dec")    set arbitration format to decimal
                slss_com.set_id_format("bin")    set arbitration format to binary
                slss_com.set_id_format("hex")    set arbitration format to hexadecimal
        """
        cmd = f"SET_ID_FORMAT||{format_short_text}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set arbitration Id notation format to {format_short_text}")
        except Exception:
            self.log_output(0, f"Could not set arbitration Id notation format")
            
    def set_data_format(self, format_short_text: str):
        """ Set the data notation format in the SLSS CANAnalyser software

            Args:
                format_short_text (string) : The short-text of the used CAN data notation (hex, dec, bin) as string

            Example:
                slss_com.set_data_format("dec")    set data format to decimal
                slss_com.set_data_format("bin")    set data format to binary
                slss_com.set_data_format("hex")    set data format to hexadecimal
        """
        cmd = f"SET_DATA_FORMAT||{format_short_text}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set data notation format to {format_short_text}")
        except Exception:
            self.log_output(0, f"Could not set data notation format")

    def search_module(self):
        """ Search for connected CAN Dongles and connect to the first Dongle which is found """
        cmd = f"SEARCH_MODULE"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Search for connected CAN Dongle")
        except Exception:
            self.log_output(0, f"Could not search for connected CAN Dongle")

    def connect_module(self, COM_port: int):
        """ Connect to a know CAN Dongle by sending the COM port number of the Dongle

            Args:
                COM_port (int) : The COM port number of the Dongle as integer

            Example:
                slss_com.connect_module(14)     connect to Dongle which has is assigned to COM port 14
        """
        cmd = f"CONNECT_MODULE||COM{COM_port}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Connect to CAN Dongle on COM{COM_port}")
        except Exception:
            self.log_output(0, f"Could not connect to CAN Dongle on COM{COM_port}")

    def disconnect_module(self):
        """ Disconnect the established Dongle connection """
        cmd = f"DISCONNECT_MODULE"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Disconnect the CAN Dongle")
        except Exception:
            self.log_output(0, f"Could not disconnect to CAN Dongle")

    """ RUN MODE AND RECORDING """

    def set_runstate(self, runState: str):
        """ Set CANAnalyser to play mode to collect CAN data

         Args:
                runState (string) : The run state of the program to be set (play, pause, stop)

            Example:
                slss_com.set_runstate("play")     set the runstate to play mode
                slss_com.set_runstate("pause")     set the runstate to pause mode
                slss_com.set_runstate("stop")     set the runstate to stop mode
        """

        cmd = f"SET_RUNSTATE||{runState.upper()}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Set program to play mode")
        except Exception:
            self.log_output(0, f"Could not set program to {runState.lower()} mode")
  
    def rec_start(self):
        """ Start the logfile recorder function in the SLSS CANAnalyser software """
        cmd = f"REC_START"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Start recording CAN traffic")
        except Exception:
            self.log_output(0, f"Could not start recording CAN traffic")

    def rec_stop(self, absolute_filepath=None, overwrite_existing_file=False, csv_delimiter=","):
        """ Stop the logfile recorder and optionally save the recorded data to a disc drive

            Args:
                absolute_filepath (string) : The absolute file path if the logfile should be saved to the disc drive after the record was stopped. The supported file format is *.csv or *.rcdf.
                overwrite_existing_file (bool) : [optional/default=False] The indicator if an existing file with the same name should be overwritten (True) or if the filename should be enhanced with a unique number (False)
                csv_delimiter (string) : [optional/default=","] The delimiter if the file is saved as *.csv file

            Example:
                slss_com.rec_stop("C:\\Bus_record.rcdf", False)           stop log recording and save file in standard format
                slss_com.rec_stop("C:\\Bus_record.csv", False, ";")       stop log recording and save file in csv format with ; as delimiter
        """
        cmd = f"REC_STOP"

        if absolute_filepath is not None:
            overwrite = "0" if overwrite_existing_file else "1"
            cmd = f"REC_STOP||{absolute_filepath}||{overwrite}||{csv_delimiter}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Stop recording CAN traffic" if absolute_filepath is None else f"Stop recording CAN traffic and save data file to {absolute_filepath}")
        except Exception:
            self.log_output(0, f"Could not stop recording CAN traffic")

    def start_sending(self, send_area="CAN"):
        """ Start sending the defined message list in the given program area (CAN, LIN, DBC - send tab)

            Args:
                send_area (string) : The send area in which the send function should be started

            Example:
                slss_com.start_sending("CAN") start sending the messages from the Send CAN Messages tab
                slss_com.start_sending("DBC") start sending the messages from the Send Database Signals tab
        """
        cmd = f"START_SENDING||{send_area}"

        try:
            self.send_command(cmd)
            self.log_output(1, f"Start sending messages from the {send_area} send tab")
        except Exception:
            self.log_output(0, f"Could not start sending messages from the {send_area} send tab")

    def stop_sending(self, send_area="CAN"):
        """ Stop sending the defined message list in the given program area (CAN, LIN, DBC - send tab)

            Args:
                send_area (string) : The send area in which the send function should be stopped

            Example:
                slss_com.stop_sending("CAN") stop sending the messages from the Send CAN Messages tab
                slss_com.stop_sending("DBC") stop sending the messages from the Send Database Signals tab
        """
        cmd = f"STOP_SENDING||{send_area}"

        try:
            self.send_command(cmd)
            self.log_output(1, f"Stop sending messages from the {send_area} send tab")
        except Exception:
            self.log_output(0, f"Could not stop sending messages from the {send_area} send tab")

    """ PROGRAM WINDOW INTERACTION """

    def load_project(self, absolute_project_filepath: str):
        """ Load an existing CANAnalyser project file (*.capf) from the disc drive

            Args:
                absolute_project_filepath (string) : The absolute file path of the CANAnalyser project file (*.capf)

            Example:
                slss_com.load_project("C:\\MyV56TestProject\\CANAnalyser_project.capf")
        """
        cmd = f"LOAD_PROJECT||{absolute_project_filepath}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Load SLSS CANAnalyser project file {absolute_project_filepath}")
        except Exception:
            self.log_output(0, f"Could not load SLSS CANAnalyser project file")

    def restart_software(self, start_tcpip_server=True):
        """ Restart the SLSS CANAnalyser software remotely and decide if the TCP/IP server should be started on program restart

            Args:
                start_tcpip_server (bool) : [optional/default=True] The indicator if the TCP/IP server should be automatically started (True) after restart or not (False)

            Example:
               slss_com.restart_software(True)   restart CANAnalyser and activate TCP/IP interface after startup
        """
        server_restart = "1" if start_tcpip_server else "0"
        cmd = f"RESTART_SOFTWARE||{server_restart}"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Restart SLSS CANAnalyser software and automatically start the TCP/IP server" if start_tcpip_server else f"Restart SLSS CANAnalyser software withouty starting the TCP/IP server")
        except Exception:
            self.log_output(0, f"Could not restart SLSS CANAnalyser software")

    def close_software(self):
        """ Close the SLSS CANAnalyser software remotely """
        cmd = f"CLOSE_SOFTWARE"
        try:
            self.send_command(cmd)
            self.log_output(1, f"Close the SLSS CANAnalyser software")
        except Exception:
            self.log_output(0, f"Could not close the SLSS CANAnalyser software")

    """ GET INFORMATION OPERATIONS """

    def get_connection(self):
        """ Get information about the current dongle connection state

            Return:
                (string) : The received connection information from the SLSS CANAnalyser software
        """
        cmd = f"GET_CONNECTION"
        data = ""
        try:
            self.mute_for_command_reply()
            self.flush_incoming_data()
            while True:
                data = self.receive_data_reply(cmd)
                if data.startswith("{") and data.strip().endswith("}"):
                    self.mute_for_command_reply(False)
                    break
            self.log_output(1, f"Retrieve the Dongle connection state from the SLSS CANAnalyser software")
        except Exception:
            self.log_output(0, f"Could not retrieve the Dongle connection state from the SLSS CANAnalyser software")

        return data

    def get_runstate(self):
        """ Get information about the current software run state (play, pause, stop) """
        cmd = f"GET_RUNSTATE"
        data = ""
        try:
            self.mute_for_command_reply()
            self.flush_incoming_data()
            while True:
                data = self.receive_data_reply(cmd)
                if data.startswith("{") and data.strip().endswith("}"):
                    self.mute_for_command_reply(False)
                    break

            self.log_output(1, f"Retrieve the run state information from the SLSS CANAnalyser software")
        except Exception:
            self.log_output(0, f"Could not retrieve run state information from the SLSS CANAnalyser software")

        return data

    def get_DBC_value(self, channel: str, message_name: str, signal_name: str):
        """ Get the value of a DBC message / signal row from the incoming DBC data tab

            Args:
                channel (string) : The CAN channel (A, B). The channel needs to match the channel in the target grid row!
                message_name (string) : The name of the DBC message available int the incoming DBC data grid
                signal_name (string) : The name of the DBC signal available int the incoming DBC data grid

            Example:
                slss_com.get_DBC_value("A", "my_CAN_Message_1", "my_CAN_Signal_1")  search for the message / signal combination and get the value as reply

        """
        cmd = f"GET_DBC_SIGNAL||{channel}||{message_name}||{signal_name}"
        data = ""
        try:
            self.mute_for_command_reply()
            self.flush_incoming_data()
            while True:
                data = self.receive_data_reply(cmd)
                if data.startswith("{") and data.strip().endswith("}"):
                    self.mute_for_command_reply(False)
                    break

            self.log_output(1, f"Retrieve DBC signal value from the SLSS CANAnalyser software")
        except Exception:
            self.log_output(0, f"Could not retrieve DBC signal value from the SLSS CANAnalyser software")

        return data

    """ 
    CLASS HELPER FUNCTIONS 
    """

    def receive_data_reply(self, command: str):
        """ [INTERNALLY_USED] This method is used to receive the reply of a data request

            Args:
                command (string) : The command which should generate the reply in the SLSS CANAnalyser software

            Return:
                (string) : The received reply from the SLSS CANAnalyser software
        """
        data = ""
        retVal = ""
        try:
            cmd = f"CTRL:{command}#"
            self.sck.send(cmd.encode())
            ready = select.select([self.sck], [], [], 4)
            if ready[0]:
                data = self.sck.recv(4096)

            if data:
                retVal = data.decode()
                self.log_output(1, f"Received data request stream {str(retVal)}")
        except Exception as e:
            self.log_output(0, f"Could not receive any data request stream! --> {str(e)}")

        return retVal

    def send_command(self, command: str):
        """ [INTERNALLY_USED] Send a program control command to change different options and settings in the connected SLSS CANAnalyser software
            NOTE: This function is used internally by several comfort functions to transfer remote control commands

            Args:
                command (string) : The control command string which should be send to the SLSS CANAnalyser
        """
        cmd = f"CTRL:{command}#"
        try:
            self.sck.send(cmd.encode())
            time.sleep(1)
            self.log_output(1, f"Send the control command {cmd} to the SLSS CANAnalyser software")
        except Exception:
            self.log_output(0, f"Could not send the control command {cmd} to the SLSS CANAnalyser software. Check the settings and if the TCP/IP interface is active in the CANAnalyser software!")

    def mute_for_command_reply(self, is_start=True):
        """ [INTERNALLY_USED] Class helper function to mute incoming messages while receiving remote command replies

            Args:
                is_start (bool) : [optional/default=True] The flag if the incoming messages should be muted (True) or un-muted (False)
        """
        if is_start:
            self.chA_muted_save = self.chA_muted
            self.chB_muted_save = self.chB_muted
            self.mute_CAN("AB")

        else:
            self.mute_CAN("A") if self.chA_muted_save else self.unmute_CAN("A")
            self.mute_CAN("B") if self.chB_muted_save else self.unmute_CAN("B")
            self.chA_muted = self.chA_muted_save
            self.chB_muted = self.chB_muted_save

    def set_debug_mode(self, debug_active: bool):
        """ [INTERNALLY_USED] Class helper function to enable or disable console the log output of this class

            Args:
                debug_active (bool) : The indicator if the debug output generation is activated (True) or deactivated (False)

        """
        self.debug_output = debug_active

    def log_output(self, log_level: int, log_txt: str, force_output=False):
        """ [INTERNALLY_USED] Class helper function to display the console log output in a structured format

            Args:
                log_level (int) : The log level evaluation indicator (0=ERROR, 1=SUCCESS)
                log_txt (string) : The string which should be displayed as log output
                force_output (bool) : [optional/default=False] The indicator whether the log output should be written, even if debug mode is deactivated (True)
        """
        if self.debug_output or force_output:
            lg_lvl = "ERROR" if log_level == 0 else ""
            lg_lvl = "SUCCESS" if log_level == 1 else lg_lvl
            dt = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")
            print(dt + "\t\t" + lg_lvl + "\t\t" + log_txt)
