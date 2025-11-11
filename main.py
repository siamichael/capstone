"""
main control program
reads bluetooth controller and controls device
"""
import time
from robot import Robot
from controller import BluetoothController

def main():
    print("=" * 50)
    print("CONTROL SYSTEM")
    print("=" * 50)
    
    # initialize robot
    print("\n[1/3] Initializing robot hardware...")
    robot = Robot()
    
    # set initial max speed (reduce for testing)
    robot.set_max_speed(50)  # start at 50% for safety
    print("Max speed set to 50% for initial testing")
    
    # initialize controller
    print("\n[2/3] Connecting to Bluetooth controller...")
    try:
        controller = BluetoothController()
    except Exception as e:
        print(f"ERROR: Could not connect to controller: {e}")
        print("Make sure controller is:")
        print("  1. Powered on")
        print("  2. Paired with Raspberry Pi")
        print("  3. Connected (not just paired)")
        robot.cleanup()
        return
    
    print("\n[3/3] Starting main control loop...")
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
    
    finally:
        print("\nStopping robot...")
        robot.stop_all()
        time.sleep(0.5)
        
        print("Cleaning up GPIO...")
        robot.cleanup()
        
        print("\n" + "=" * 50)
        print("ROBOT SHUTDOWN COMPLETE")
        print("=" * 50)
        print("Goodbye!\n")

if __name__ == "__main__":
    main()
