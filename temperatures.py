import sys

import board
import busio
import adafruit_mcp9808

import time

i2c = busio.I2C(board.SCL, board.SDA)

mcp_water = adafruit_mcp9808.MCP9808(i2c, address=0x18)
mcp_porch = adafruit_mcp9808.MCP9808(i2c, address=0x19)
mcp_green = adafruit_mcp9808.MCP9808(i2c, address=0x1a)
mcp_inside1 = adafruit_mcp9808.MCP9808(i2c, address=0x1b)
mcp_inside2 = adafruit_mcp9808.MCP9808(i2c, address=0x1c)


def write_to_file(timestamp, temp_data, filehandle):
    temp_format = ("{:0.2f}",)
    time_format = "%Y-%m-%dT%H:%M:%S"
    temp_format_string = ",".join(temp_format * len(temp_data))
    data = time.strftime(time_format, timestamp) + "," + temp_format_string.format(*temp_data) + "\n"
    filehandle.write(data)
    filehandle.flush()


def main(filename):
    print("{:^52s}".format("Measured Temperatures"))
    print("{:^14s} {:^14s} {:^14s} {:^14s} {:^14s}".format("Greenhouse", "Front Porch", "Water", "Inside 1", "Inside 2"))

    print("{:12.1f}   {:12.1f}   {:12.1f}   {:12.1f}   {:12.1f}  ".format(
        mcp_green.temperature,
        mcp_porch.temperature,
        mcp_water.temperature,
        mcp_inside1.temperature,
        mcp_inside2.temperature))

    with open(filename, "a") as fh:

        while True:
            temp_data = (
                mcp_green.temperature,
                mcp_porch.temperature,
                mcp_water.temperature,
                mcp_inside1.temperature,
                mcp_inside2.temperature
            )
            print("{:12.1f}   {:12.1f}   {:12.1f}   {:12.1f}   {:12.1f}  ".format(*temp_data))

            write_to_file(time.gmtime(), temp_data, fh)

            time.sleep(1)



if __name__ == "__main__":
    main(sys.argv[1])
