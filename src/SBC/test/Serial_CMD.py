
import serial
import time  # Import the time module for sleep functionality

# Define the serial port and baud rate (typically 9600 for Maestro)
PORT = '/dev/ttyUSB0' 
# PORT = 'COM4'
BAUD_RATE = 115200

START_BYTE = b'$'
END_BYTE = b'\n'

def calculate_checksum(message):
    """
    Calculate XOR checksum for the message.
    :param message: Bytes for checksum calculation.
    :return: Checksum byte.
    """
    checksum = 0
    for byte in message:
        checksum ^= byte
    return checksum

def create_message(command, data=None):
    """
    Create a DD-UART protocol-compliant message.
    :param command: 2-byte command ID (e.g., 0x0001).
    :param data: Optional data as a bytes object.
    :return: Complete message as bytes.
    """
    command_bytes = command.to_bytes(2, 'big')
    data = data if data else b''
    length = 7 + len(data)  # Start, length (2 bytes), command (2 bytes), checksum, end
    length_bytes = length.to_bytes(2, 'big')
    message = START_BYTE + length_bytes + command_bytes + data
    checksum = calculate_checksum(message[1:])
    return message + bytes([checksum]) + END_BYTE

def validate_message(message):
    """
    Validate a received message.
    :param message: Full message as bytes.
    :return: True if valid, False otherwise.
    """
    # Validate start and end bytes
    if message[0:1] != START_BYTE or message[-1:] != END_BYTE:
        return False

    # Validate length
    length = int.from_bytes(message[1:3], 'big')
    if len(message) != length:
        return False

    # Validate checksum
    checksum = calculate_checksum(message[1:-2])
    if checksum != message[-2]:
        return False

    return True

def send_command(ser, command, data=None):
    """
    Send a command to the STM32.
    :param ser: Open serial connection.
    :param command: 2-byte command ID.
    :param data: Optional data as bytes.
    """
    message = create_message(command, data)
    ser.write(message)
    print(f"Sent: {message}")

def read_response(ser):
    """
    Read and validate a response from the STM32.
    :param ser: Open serial connection.
    :return: Decoded response if valid, None otherwise.
    """
    response = ser.read_until(END_BYTE)
    if validate_message(response):
        length = int.from_bytes(response[1:3], 'big')
        command = int.from_bytes(response[3:5], 'big')
        data = response[5:-2]
        return {
            'length': length,
            'command': command,
            'data': data
        }
    else:
        print("Invalid response received.")
        return None

# Example Usage
if __name__ == "__main__":

    
    # Open the serial port
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    except serial.SerialException as e:
        print(f"Error opening serial port {PORT}: {e}")
        exit(1)

    # Send a command to read gyro
    # send_command(ser, 0x0003)

    # # Read and process the response
    # response = read_response(ser)
    # if response:
    #     print(f"Response: {response}")


    # Example: Send the command to move forward (0x0101)
    send_command(ser, 0x0101)
    time.sleep(0.1)
    # Read and process the response
    response = read_response(ser)
    if response:
        print(f"Response: {response}")

    # Wait for 5 seconds before sending the next command
    time.sleep(5)

    # Example: Send the command to stop (0x0103)
    send_command(ser, 0x0103)

    # Read and process the response
    response = read_response(ser)
    if response:
        print(f"Response: {response}")
    time.sleep(5)

    # # Example: Send the command to move in reverse (0x0102)
    send_command(ser, 0x0104,(90).to_bytes(1, 'big'))
    time.sleep(0.1)

    # Read and process the response
    response = read_response(ser)
    if response:
        print(f"Response: {response}")

    time.sleep(5)

    # # Example: Send the command to move in reverse (0x0102)
    send_command(ser, 0x0102)
    time.sleep(0.1)

    # Read and process the response
    response = read_response(ser)
    if response:
        print(f"Response: {response}")

    # Wait for 5 seconds before sending the next command
    time.sleep(5)

    # Example: Send the command to stop (0x0103)
    send_command(ser, 0x0103)

    # Read and process the response
    response = read_response(ser)
    if response:
        print(f"Response: {response}")

    ser.close()
