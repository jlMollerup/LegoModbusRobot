from pymodbus.client import ModbusTcpClient
import time

# Define Modbus server details
SERVER_IP = '192.168.10.100'
SERVER_PORT = 502

# Define register addresses
INPUT_REGISTER_START = 0
OUTPUT_REGISTER_START = 0
NUM_REGISTERS = 4

# Variables for changing outputs
output_values = [0, 0, 0, 0]

# Create Modbus client
client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)

# Function to read input registers
def read_inputs():
    result = client.read_input_registers(INPUT_REGISTER_START, count=NUM_REGISTERS,slave=1)
    if result.isError():
        print(f"Error reading inputs: {result}")
    else:
        return result.registers

# Function to read output registers
def read_outputs():
    result = client.read_holding_registers(OUTPUT_REGISTER_START, count=NUM_REGISTERS)
    if result.isError():
        print(f"Error reading outputs: {result}")
    else:
        return result.registers

# Function to write output registers
def write_outputs(values):
    result = client.write_registers(OUTPUT_REGISTER_START, values)
    if result.isError():
        print(f"Error writing outputs: {result}")

# Main loop
prev_inputs = None
prev_outputs = None

try:
    while True:
        # Read inputs
        inputs = read_inputs()
        if inputs != prev_inputs:
            print("Inputs changed:", inputs)
            prev_inputs = inputs

        # Read outputs
        outputs = read_outputs()
        if outputs != prev_outputs:
            print("Outputs changed:", outputs)
            prev_outputs = outputs

        # Example: Change output values
        # Uncomment and modify as needed
        # output_values = [1, 2, 3, 4]
        # write_outputs(output_values)

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.close()
