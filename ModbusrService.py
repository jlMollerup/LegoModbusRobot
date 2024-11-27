from pymodbus.client import ModbusTcpClient
import time
import serialMinStormModule
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
    # init minstomer
    tool = serialMinStormModule.RobotController()
    


    while True:
        # Read inputs
        inputs = read_inputs()
        
        if inputs != prev_inputs:
            for i, (prev, current) in enumerate(zip(prev_inputs or [], inputs)):
                if prev != current:
                    match i:
                        case 0:
                            print("Input 0 changed:", current)
                            # Add your custom logic here for input 0 change
                            tool.move_motor_a(current)
                        case 1:
                            print("Input 1 changed:", current)
                            # Add your custom logic here for input 1 change
                        case 2:
                            print("Input 2 changed:", current)
                            # Add your custom logic here for input 2 change
                        case 3:
                            print("Input 3 changed:", current)
                            # Add your custom logic here for input 3 change
                        case _:
                            print(f"Input {i} changed:", current)
                            # Add your custom logic here for other input changes





                    
            prev_inputs = inputs.copy()


        # Read outputs
        outputs = read_outputs()
        if outputs != prev_outputs:
            print("Outputs changed:", outputs)
            prev_outputs = outputs

        # Example: Change output values
        # Uncomment and modify as needed
        # output_values = [1, 2, 3, 4]
        # write_outputs(output_values)
# Asynchronous update of output registers every 1 second
        if time.time() % 1 < 0.1:  # Check if it's close to a whole second
            output_values = [int(time.time()) % 256] * NUM_REGISTERS  # Example: Use current time as values
            write_outputs(output_values)

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    client.close()
