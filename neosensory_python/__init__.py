import base64
import uuid

# The GATT Characteristic used for writing to Neosensory Buzz
ns_uart_rx_id = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
# The GATT Characteristic used for getting response notifications from Buzz
ns_uart_tx_id = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')


class NeoDevice:


    def __init__(self, client):
        self.client = client

    def set_client(self, new_client):
        self.client = new_client

    async def enable_notifications(self, handler):
        await self.client.start_notify(ns_uart_tx_id, handler)

    async def request_developer_authorization(self):
        cmd = ("auth as developer\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def accept_developer_api_terms(self):
        cmd = ("accept\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def resume_device_algorithm(self):
        cmd = ("audio start\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def start_audio(self):
        cmd = ("audio start\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def stop_audio(self):
        cmd = ("audio stop\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)
        await self.clear_motor_queue()

    async def get_battery_level(self):
        cmd = ("device battery_soc\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def get_device_info(self):
        cmd = ("device info\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def clear_motor_queue(self):
        cmd = ("motors clear_queue\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def enable_motors(self):
        cmd = ("motors start\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def disable_motors(self):
        cmd = ("motors stop\r\n").encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, cmd)

    async def stop_motors(self):
        await self.vibrate_motors([0, 0, 0, 0])

    async def pause_device_algorithm(self):
        await self.stop_audio()
        await self.enable_motors()

    async def vibrate_motors(self, motor_list):
        motor_command_string = "motors vibrate \"{}\"\r\n".format(base64.
            b64encode(bytearray(motor_list)).decode('utf-8')).encode("utf-8")
        await self.client.write_gatt_char(ns_uart_rx_id, motor_command_string)
