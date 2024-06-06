import asyncio
import logging
from bleak import BleakScanner, BleakClient

log_level = logging.INFO
logging.basicConfig(
    level=log_level,
    # format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def device_by_name(name: str = "MPY ESP32"):
    return await BleakScanner.find_device_by_name(name)


async def list_devices():
    _devices = await BleakScanner.discover()
    for d in _devices:
        print(d)


async def main(address):
    async with BleakClient(address) as client:
        # model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        # print("Model Number: {0}".format("".join(map(chr, model_number))))
        logger.info("connected")

        for service in client.services:
            logger.info("[Service] %s", service)

            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        extra = f", Value: {value}"
                    except Exception as e:
                        extra = f", Error: {e}"
                else:
                    extra = ""

                if "write-without-response" in char.properties:
                    extra += f", Max write w/o rsp size: {char.max_write_without_response_size}"

                logger.info("  [Characteristic] %s (%s)%s", char, ",".join(char.properties), extra, )

                for descriptor in char.descriptors:
                    try:
                        value = await client.read_gatt_descriptor(descriptor.handle)
                        logger.info("    [Descriptor] %s, Value: %r", descriptor, value)
                    except Exception as e:
                        logger.error("    [Descriptor] %s, Error: %s", descriptor, e)

        logger.info("disconnecting...")


async def test(address, action: str = "beep"):
    logger.info(f"Performing action {action} on address {address}")
    async with BleakClient(address) as client:
        logger.debug("connected")
        for service in client.services:
            logger.debug("[Service] %s", service)
            for char in service.characteristics:
                if "write" in char.properties:
                    await client.write_gatt_char(char.handle, bytearray(bytes(action, "utf-8")))
        logger.debug("disconnecting...")


runtests = True
esp32_device = "Hello32"
device = asyncio.run(device_by_name(esp32_device))
if not device:
    logger.info(f"Device not found: {esp32_device}")
    logger.info("Scanning all devices:")
    asyncio.run(list_devices())
else:
    if runtests:
        logger.info(f"test connecting to {device.name}")
        asyncio.run(test(device.address, "toggle_led"))
        asyncio.run(test(device.address, "blink_led"))
        asyncio.run(test(device.address, "nothing"))
        asyncio.run(test(device.address))
        asyncio.run(test(device.address, "toggle_led"))
        logger.info("test disconnected")
    else:
        logger.info(f"connecting to {device.name}")
        asyncio.run(main(device.address))
        logger.info("disconnected")
