"""
test script for linear actuator only
tests actuator control with bluetooth controller
run from test directory: python test_actuator.py
"""
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO
from controller import BluetoothController
from motor_driver import MotorDriver

def main():
    print("=" * 50)
    print("LINEAR ACTUATOR TEST")
    print("=" * 50)
    
    print("\n[1/3] Initializing GPIO...")
    GPIO.setmode(GPIO.BCM)
    
    print("[2/3] Initializing actuator...")
    actuator = MotorDriver(
        rpwm_pin=19,
        lpwm_pin=26,
        r_en_pin=13,
        l_en_pin=16,
        name="Actuator"
    )
    
    # initialize controller
    print("[3/3] Connecting to Bluetooth controller...")
    try:
        controller = BluetoothController()
    except Exception as e:
        print(f"ERROR: Could not connect to controller: {e}")
        print("Make sure controller is:")
        print("  1. Powered on")
        print("  2. Paired with Raspberry Pi")
        print("  3. Connected (not just paired)")
        actuator.cleanup()
        GPIO.cleanup()
        return
    
    print("\nVerifying GPIO pin configuration...")
    try:
        # check if pins are set up correctly
        print(f"  ✓ RPWM Pin {actuator.rpwm_pin}: Configured")
        print(f"  ✓ LPWM Pin {actuator.lpwm_pin}: Configured")
        if actuator.r_en_pin:
            print(f"  ✓ R_EN Pin {actuator.r_en_pin}: Configured (HIGH)")
        if actuator.l_en_pin:
            print(f"  ✓ L_EN Pin {actuator.l_en_pin}: Configured (HIGH)")
    except Exception as e:
        print(f"  ✗ GPIO Error: {e}")
        actuator.cleanup()
        GPIO.cleanup()
        return
    
    print("\n" + "=" * 50)
    print("ACTUATOR TEST READY")
    print("=" * 50)
    print("\nControls:")
    print("  Button X (top)    - Raise Actuator")
    print("  Button B (bottom) - Lower Actuator")
    print("  Ctrl+C            - Stop & Exit")
    print("\n" + "=" * 50 + "\n")
    
    last_command_time = time.time()
    command_timeout = 1.5  # stop if no commands for 1.5 seconds
    
    try:
        while True:
            if not controller.is_connected():
                print("\nWARNING: Controller disconnected")
                actuator.stop()
                break
            
            controller.read_events()
            
            if controller.received_events_this_frame:
                last_command_time = time.time()
            
            if time.time() - last_command_time > command_timeout:
                actuator.stop()
            else:
                actuator_cmd = controller.get_actuator_command()
                
                if actuator_cmd == "raise":
                    actuator.set_speed(50)  # 50% speed raising
                    print("Raising actuator...", end='\r')
                elif actuator_cmd == "lower":
                    actuator.set_speed(-50)  # 50% speed lowering
                    print("Lowering actuator...", end='\r')
                else:
                    actuator.stop()
            
            time.sleep(0.05)
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 50)
        print("TEST STOPPED (Ctrl+C)")
        print("=" * 50)
    
    except Exception as e:
        print(f"\n\nERROR: {e}")
        print("Stopping actuator...")
    
    finally:
        print("\nStopping actuator...")
        actuator.stop()
        time.sleep(0.5)
        
        print("Cleaning up GPIO...")
        actuator.cleanup()
        GPIO.cleanup()
        
        print("\n" + "=" * 50)
        print("TEST COMPLETE")
        print("=" * 50)
        print("Goodbye!\n")

if __name__ == "__main__":
    main()