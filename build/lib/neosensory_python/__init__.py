import base64
import uuid
import math

# The GATT Characteristic used for writing to Neosensory Buzz
ns_uart_rx_id = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
# The GATT Characteristic used for getting response notifications from Buzz
ns_uart_tx_id = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')


class NeoDevice:
    """A class for controlling a connected Neosensory device with Bleak

    """

    def __init__(self, client):
        self.client = client

    def set_client(self, new_client):
        """Set the Bleak client object

        Args:
            new_client: the Bleak client object
        """
        self.client = new_client

    async def enable_notifications(self, handler):
        """Enable notifications to be sent back to host computer

        Args:
            handler: the handler function that processes the received reponse
        """
        await self.client.start_notify(ns_uart_tx_id, handler)

    async def send_command(self, command):
        """Send a custom API command to Neosensory device

        Args:
            command: command string, e.g. "device info"
        """
        cmd = command.encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def request_developer_authorization(self):
        """Request developer authorization. The CLI returns the message
            “Please type 'accept' and hit enter to agree to Neosensory
            Inc's Developer Terms and Conditions, which can be viewed at
            https://neosensory.com/legal/dev-terms-service
        """
        cmd = ("auth as developer\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def accept_developer_api_terms(self):
        """After successfully calling auth as developer, use the accept
            command to agree to the Neosensory Developer API License
            (https://neosensory.com/legal/dev-terms-service/).
            Successfully calling this unlocks the following commands:
            audio start, audio stop, motors_clear_queue, motors start,
            motors_stop, motors vibrate.
        """
        cmd = ("accept\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def resume_device_algorithm(self):
        """(Re)starts the device’s microphone audio acquisition and
            algorithm. This command requires successful developer
            authorization, otherwise, the command will fail. This
            is functionally the same as startAudio()
        """
        cmd = ("audio start\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def start_audio(self):
        """(Re)starts the device’s microphone audio acquisition.
            This command requires successful developer authorization,
            otherwise, the command will fail.
        """
        cmd = ("audio start\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def stop_audio(self):
        """Stop the device’s microphone audio acquisition.
            This should be called prior to transmitting motor vibration data.
            This command requires successful developer authorization,
            otherwise, the command will fail.
        """
        cmd = ("audio stop\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)
        await self.clear_motor_queue()

    async def get_battery_level(self):
        """Obtain the device’s battery level in %.
            This command does not require developer authorization
        """
        cmd = ("device battery_soc\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def get_device_info(self):
        """Obtain various device and firmware information.
            This command does not require developer authorization.
        """
        cmd = ("device info\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def clear_motor_queue(self):
        """Clear any vibration commands sitting the device’s motor FIFO queue.
            This should be called prior to streaming control frames using
            motors vibrate. This command requires successful developer
            authorization, otherwise, the command will fail.
        """
        cmd = ("motors clear_queue\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def enable_motors(self):
        """Initialize and start the motors interface.
            The motors can then accept motors vibrate commands.
            This command requires successful developer authorization,
            otherwise, the command will fail.
        """
        cmd = ("motors start\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def disable_motors(self):
        """Clear the motors command queue and shut down the
            motor drivers. This command requires successful developer
            authorization, otherwise, the command will fail.
        """
        cmd = ("motors stop\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def stop_motors(self):
        """Send a frame that turns off the motors. Note: the API
            CLI command "motors stop" disables the motor drivers.
            This command requires successful developer authorization,
            otherwise, the command will fail.
            Assumes this is a 4-motor device (e.g. Neosensory Buzz)
        """
        await self.vibrate_motors([0, 0, 0, 0])

    async def pause_device_algorithm(self):
        """Pause the running algorithm on the device to accept motor
            control over the CLI. This command requires successful
            developer authorization, otherwise, the command will fail.
        """
        await self.stop_audio()
        await self.enable_motors()

    async def vibrate_motors(self, motor_list):
        """Set the actuators amplitudes on a connected Neosensory device.
            Note: actuators will stay vibrating indefinitely on the last
            frame received until a new control * frame is received

        Args:
            motor_list: a list of motor intensity values on [0,255].
                This is API call is designed for Neosensory Buzz--and assumes
                4 motors. If the list length is > 4, the Buzz will put
                subsequent encodings on the queue to be played out on a
                16 ms period.

        """

        motor_command_string = "motors vibrate \"{}\"\r\n".format(base64.
            b64encode(bytearray(motor_list)).decode('utf-8')).encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, motor_command_string)


def get_motor_intensity(linear_intensity, min_intensity, max_intensity):
    """Linearly map a value on [0,1] to a motor
        vibration strenght on [min_intensity, max_intensity]

    Args:
        linear_intensity: an intensity value on [0,1]

        min_intensity: a minimum motor intensity value.
            Typically 0 or minimal perceptible motor activation value.

        max_intensity: a maximum motor intensity value.
            For Neosensory Buzz, motor values can be on [0,255]

    Returns:
        A linearly mapped value on [min_intensity, max_intensity]


    """
    if linear_intensity <= 0:
        return min_intensity
    elif linear_intensity >= 1:
        return max_intensity
    else:
        return int(math.expm1(linear_intensity) / (math.e - 1)
         * (max_intensity - min_intensity) + min_intensity)


def get_buzz_illusion_activations(linear_intensity, location,
        min_intensity, max_intensity, num_motors):
    """Apply a haptic illusion across a Neosensory device
        to create the sensation of a single arbitrary point
        around the wrist vibrating.

    Args:
        linear_intensity: an intensity value on [0,1]

        location: a location around the wrist on [0,1]

        min_intensity: a minimum motor intensity value.
            Typically 0 or minimal perceptible motor activation value.

        max_intensity: a maximum motor intensity value.
            For Neosensory Buzz, motor values can be on [0,255]

        num_motors: number of motors on the device (4 for Neosensory Buzz)

    Returns:
        A list of motor encodings representing an illusory point.

    """
    motor_frame = [0]*num_motors
    if linear_intensity <= 0:
        return motor_frame
    motor_intensity = get_motor_intensity(linear_intensity,
        min_intensity, max_intensity)
    motor_location = location * (num_motors - 1)
    lower_motor_index = int(math.floor(motor_location))
    upper_motor_index = int(math.ceil(motor_location))
    lower_distance = abs(motor_location - lower_motor_index)
    upper_distance = abs(motor_location - upper_motor_index)
    lower_activation = int(motor_intensity * math.sqrt(1 - lower_distance))
    upper_activation = int(motor_intensity * math.sqrt(1 - upper_distance))
    motor_frame[lower_motor_index] = lower_activation
    motor_frame[upper_motor_index] = upper_activation
    return motor_frame
