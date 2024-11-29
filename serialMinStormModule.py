import serial
import time
import os



class RobotController:




    def __init__(self, baud_rate=115200, timeout=4):
        port = self.find_available_port()
        if port is None:
            raise Exception("No available port found")
        self.ser = None
        for attempt in range(3):
            try:
                self.ser = serial.Serial(port, baud_rate, timeout=timeout)
                if self.ser.is_open:
                    print(f"Serial connection established on attempt {attempt + 1}")
                    break
            except serial.SerialException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)
                else:
                    print("Failed to establish serial connection after 3 attempts")
                    raise

        if self.ser is None or not self.ser.is_open:
            raise Exception("Failed to open serial connection")
        
        time.sleep(2)
        self.initialize_motors()
        self.move_motor_a(100)
        time.sleep(2)
        self.move_motor_a(10 )

    def find_available_port(self):
        ports = ['/dev/ttyACM1', '/dev/ttyACM0']
        for port in ports:
            if os.path.exists(port):
                with open('available_port.txt', 'w') as file:
                    file.write(port)
                return port
        return None

    def send_command(self, command):
        print(f"Sending command: {command}")
        self.ser.write(f"{command}\r\n".encode())
        
        time.sleep(0.1)
        response = self.ser.read_all().decode().strip()
        if response:
            print(f"Response: {response}")

    def initialize_motors(self):
        
        self.ser.write(b'\x03')
        time.sleep(10)
        self.send_command("from mindstorms import Motor")
        self.send_command("motor_a = Motor('A')")
        self.send_command("motor_b = Motor('B')")

    def read_motor_angle(self, motor='A'):
        if motor not in ['A', 'B']:
            raise ValueError("Motor must be 'A' or 'B'")
        self.send_command(f"print(int(motor_{motor.lower()}.get_position()))")
        time.sleep(0.9)
        response =""
        response += self.ser.read(self.ser.in_waiting).decode()
        time.sleep(0.1)
        
        
        response = self.ser.read_all().decode().strip()
        try:
            return int(response)
        except ValueError:
            print(f"Error: Unable to parse motor angle from response: {response}")
            return None

    def move_motor_a(self,agu):
        self.send_command(f"motor_a.run_to_position({agu})")
    def move_motor_b(self,agu):
        self.send_command(f"motor_b.run_to_position({agu})")

    def run_motors_simultaneously(self,agu_a,agu_b):
        self.send_command(f"motor_a.start({agu_a})")
        self.send_command(f"motor_b.start({agu_b})")
        time.sleep(2)
        self.send_command("motor_a.stop()")
        self.send_command("motor_b.stop()")

    def get_motor_positions(self):
        self.send_command("print(motor_a.get_position())")
        self.send_command("print(motor_b.get_position())")

    def run(self):
        try:

            # self.move_motor_a()
            # self.move_motor_b()
            # self.run_motors_simultaneously()
            # self.get_motor_positions()
            print(f"vinkel er :{self.read_motor_angle(motor='B')}")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close()

    def close(self):
        time.sleep(2)
        self.ser.close()
        print("Serial connection closed")

# Usage
# if __name__ == "__main__":
#     robot = RobotController()

        self.send_command("motor_a.run_to_position( 50)")



    def run_motors_simultaneously(self):
        self.send_command("motor_a.start(50)")
        self.send_command("motor_b.start(-50)")
        time.sleep(2)
        self.send_command("motor_a.stop()")
        self.send_command("motor_b.stop()")

    def get_motor_positions(self):
        self.send_command("print(motor_a.get_position())")
        self.send_command("print(motor_b.get_position())")

    def run(self):
        try:
            
            # self.move_motor_a()
            # self.move_motor_b()
            # self.run_motors_simultaneously()
            # self.get_motor_positions()
            print(f"vinkel er :{self.read_motor_angle(motor='B')}")
        
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close()

    def close(self):
        time.sleep(2)
        self.ser.close()
        print("Serial connection closed")

# Usage
# if __name__ == "__main__":
#     robot = RobotController()
#     robot.run()