from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
import logging
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize data store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0]*100),
    co=ModbusSequentialDataBlock(0, [0]*100),
    hr=ModbusSequentialDataBlock(0, [0]*100),
    ir=ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)

# Modbus addresses
# Readable values: 40001, 40002
# Writable values: 40003, 40004

def update_values():
    while True:
        # Check for changes in readable values
        value1 = store.getValues(3, 0, 1)[0]
        value2 = store.getValues(3, 1, 1)[0]
        
        # Check for changes in writable values
        value3 = store.getValues(3, 2, 1)[0]
        value4 = store.getValues(3, 3, 1)[0]
        
        print(f"Current values: {value1}, {value2}, {value3}, {value4}")
        time.sleep(1)

# Start the update thread
update_thread = threading.Thread(target=update_values, daemon=True)
update_thread.start()

# Start the Modbus server
StartTcpServer( address=("localhost", 502))
