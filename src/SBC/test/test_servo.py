import serial
import time

# Define the serial port and baud rate (typically 9600 for Maestro)
PORT = '/dev/ttyACM0' 
# PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

# Define operational ranges for each servo channel
SERVO_CHANNELS = {
    0: {"name": "steering", "min": 1190, "max": 2300, "middle": 1750}
}

def set_servo_position(ser, channel, pulse_width_us):
    """
    Set the target position of a servo with range checking.
    """
    # Check if channel exists
    if channel not in SERVO_CHANNELS:
        print(f"Error: Channel {channel} not defined.")
        return

    # Get min and max range
    min_pw = SERVO_CHANNELS[channel]["min"]
    max_pw = SERVO_CHANNELS[channel]["max"]

    # Constrain pulse width within the allowed range
    pulse_width_us = max(min_pw, min(pulse_width_us, max_pw))

    # Convert pulse width in microseconds to quarter-microseconds
    target = pulse_width_us * 4

    # The Maestro "Set Target" command: 0x84, channel, two bytes (LSB and MSB)
    command = bytearray([
        0x84,
        channel,
        target & 0x7F,           # lower 7 bits
        (target >> 7) & 0x7F     # upper 7 bits
    ])
    ser.write(command)
    print(f"Sent {SERVO_CHANNELS[channel]['name']} (Channel {channel}) to {pulse_width_us} µs (target={target}).")


def main():
    # Open the serial port
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {PORT}: {e}")
        return

    # Give the connection a moment to settle
    time.sleep(2)
    set_servo_position(ser, channel=0, pulse_width_us=2150)
    time.sleep(2)

    # You can set additional channels similarly:
    set_servo_position(ser, channel=0, pulse_width_us=1190)
    time.sleep(2)
    set_servo_position(ser, channel=0, pulse_width_us=1750)
    time.sleep(2)
    set_servo_position(ser, channel=0, pulse_width_us=2150)
    time.sleep(2)
    set_servo_position(ser, channel=0, pulse_width_us=1700)
    time.sleep(2)
    # Close the serial port when done

    # You can add more preset tests below
    # armPresetPosition(ser, value=1)

    # Close the serial port when done
    ser.close()

if __name__ == '__main__':
    main()
