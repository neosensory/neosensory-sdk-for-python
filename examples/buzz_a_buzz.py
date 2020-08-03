import asyncio
from bleak import BleakClient
from bleak import discover
from neosensory_python import NeoDevice


def notification_handler(sender, data):
    print("{0}: {1}".format(sender, data))


async def run(loop):

    # "X" will  get overwritten if a Buzz is found
    buzz_addr = "X"  # e.g. "EB:CA:85:38:19:1D"
    devices = await discover()
    for d in devices:
        if str(d).find("Buzz") > 0:
            print("Found a Buzz! " + str(d) +
             "\r\nAddress substring: " + str(d)[:17])
            # set the address to a found Buzz
            buzz_addr = str(d)[:17]

    async with BleakClient(buzz_addr, loop=loop) as client:

        my_buzz = NeoDevice(client)

        await asyncio.sleep(1)

        x = await client.is_connected()
        print("Connection State: {0}\r\n".format(x))

        await my_buzz.enable_notifications(notification_handler)

        await asyncio.sleep(1)

        await my_buzz.request_developer_authorization()

        await my_buzz.accept_developer_api_terms()

        await my_buzz.pause_device_algorithm()

        motor_vibrate_frame = [0, 0, 0, 0]
        motor_pattern_index = 0
        motor_pattern_value = 0

        try:
            while True:
                await asyncio.sleep(0.1)
                await my_buzz.vibrate_motors(motor_vibrate_frame)
                motor_pattern_index = (motor_pattern_index + 1) % 4
                motor_pattern_value = (motor_pattern_value + 20) % 255
                motor_vibrate_frame[motor_pattern_index] = motor_pattern_value
        except KeyboardInterrupt:
            await my_buzz.resume_device_algorithm()
            pass

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
