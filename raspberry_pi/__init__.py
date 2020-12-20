__ALL__ = ('real_raspberry_pi', 'TFT240x135')

import subprocess

real_raspberry_pi = (subprocess.check_output(("uname", "-m")).decode().strip() == "armv7l")

if real_raspberry_pi:
    from raspberry_pi.raspberry_pi import *
else:
    from raspberry_pi.mock_pi import *

