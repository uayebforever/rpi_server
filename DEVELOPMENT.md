# Raspberry Pi Development

### Ubuntu Server

For various reasons (sigh) I decided to make the *wollemi-server* RPi run on Ubuntu Server. So that means that setting up Adafruit's CircuitPython is slightly more complicated.

The details are how to get the I2C bus working.

This [handy medium article](https://medium.com/vacatronics/getting-started-with-raspberry-pi-i2c-and-ubuntu-server-eaa57ee0baf2) seems to answer the key differences:

| On Raspberrian                         | On Ubuntu Server               |
| -------------------------------------- | ------------------------------ |
| `apt-get install python-smbus`         | `pip3 install smbus2`          |
| `apt-get install -y i2c-tools`         | `apt-get install -y i2c-tools` |
| `raspi-config` (enable kernel support) | *none*                         |
|                                        |                                |

 