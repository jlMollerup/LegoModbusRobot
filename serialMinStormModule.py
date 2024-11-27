import serial
import time



class RobotController:
    def __init__(self, port='/dev/ttyACM0', baud_rate=115200, timeout=1):
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
        self.initialize_motors()

    def send_command(self, command):
        print(f"Sending command: {command}")
        self.ser.write(f"{command}\r\n".encode())
        time.sleep(0.1)
        response = self.ser.read_all().decode().strip()
        if response:
            print(f"Response: {response}")

    def initialize_motors(self):
        self.send_command("^C")
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

    def move_motor_a(self):
        self.send_command("motor_a.run_to_position( 50)")

    def move_motor_b(self):
        self.send_command("motor_b.run_for_degrees(-360, 50)")

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
if __name__ == "__main__":
    robot = RobotController()
    robot.run()