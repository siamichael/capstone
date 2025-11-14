"""
main control program
reads bluetooth controller and controls device
"""
import time
import signal
import sys
from robot import Robot
from controller import BluetoothController

robot = None

def signal_handler(sig, frame):
    """handle shutdown signals"""
    global robot
    print("=" * 50)
    print("SHUTDOWN SIGNAL RECEIVED")
    print("=" * 50)
    if robot:
        print("Stopping all motors...")
        robot.stop_all()
        time.sleep(0.5)
        print("Cleaning up GPIO...")
        robot.cleanup()
    print("=" * 50)
    print("ROBOT SHUTDOWN COMPLETE")
    print("=" * 50)
    sys.exit(0)

def wait_for_controller():
    while True:
        try:
            print("Connecting to controller...")
            controller = BluetoothController()
            print("Controller connected!")
            return controller
        except Exception as e:
            print(f"Controller not found, retrying in 3 seconds...")
            time.sleep(3)

def main():
    print("=" * 50)
    print("CONTROL SYSTEM")
    print("=" * 50)
    
    # initialize robot
    print("\n[1/2] Initializing robot hardware...")
    robot = Robot()
    
    # set initial max speed 
    robot.set_max_speed(100)
    print("Max speed set to 100%")
    
    while True:
    # initialize controller
        print("\n[2/2] Connecting to Bluetooth controller...")
        controller = wait_for_controller()
    
    
        print("\n" + "=" * 50)
        print("ROBOT READY")
        print("=" * 50)
        print("\nControls:")
        print("  Joystick Y-axis   - Forward/Backward")
        print("  Joystick X-axis   - Turn Left/Right")
        print("  Button X (top)    - Raise Tongue")
        print("  Button B (bottom) - Lower Tongue")
        print("  Ctrl+C            - Emergency Stop & Exit") # can change if we get an actual button / could be button on the remote (but idk because if the remote unpairs)
        print("\n" + "=" * 50 + "\n")
    
        # track last command time for timeout safety - if controller disconnects
        last_command_time = time.time()
        command_timeout = 1.5  # stop if no commands for 1.5 seconds
        
        try:
            while True:
                # check if controller is still connected
                if not controller.is_connected():
                    print("\nWARNING: Controller disconnected")
                    robot.stop_all()
                    break
                
                # read controller input
                controller.read_events()
                
                robot.update()
                
                # get drive commands
                forward, turn = controller.get_drive_values()
                
                # update command time if there's input
                if controller.received_events_this_frame or controller.has_input():
                    last_command_time = time.time()
                
                # check for command timeout (safety feature)
                if time.time() - last_command_time > command_timeout:
                    robot.stop_all()
                else:
                    # send drive commands to robot
                    robot.drive(turn, forward)
                
                # get actuator command
                actuator_cmd = controller.get_actuator_command()
                if actuator_cmd == "raise":
                    robot.raise_tongue(100)
                elif actuator_cmd == "lower":
                    robot.lower_tongue(100)
                else:
                    robot.stop_actuator()
                
                # small delay (20Hz update rate)
                time.sleep(0.05)
    
        except KeyboardInterrupt:
            print("\n\n" + "=" * 50)
            print("EMERGENCY STOP ACTIVATED (Ctrl+C)")
            print("=" * 50)
        
        except Exception as e:
            print(f"\n\nERROR: {e}")
            print("Emergency stop activated")
            robot.stop_all()
            time.sleep(2)

if __name__ == "__main__":
    main()
