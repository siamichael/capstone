"""
GPIO diagnostic script
checks the state of GPIO pins to verify they're working
"""
import RPi.GPIO as GPIO
import time

def check_pin_state(pin_number, pin_name):
    """Check and display the state of a GPIO pin"""
    try:
        GPIO.setup(pin_number, GPIO.IN)
        state = GPIO.input(pin_number)
        print(f"  Pin {pin_number:2d} ({pin_name:15s}): {'HIGH (3.3V)' if state else 'LOW (0V)'}")
    except Exception as e:
        print(f"  Pin {pin_number:2d} ({pin_name:15s}): ERROR - {e}")

def main():
    print("=" * 60)
    print("GPIO PIN STATE DIAGNOSTIC")
    print("=" * 60)
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    print("\nEnter the pin numbers you're using for the actuator:")
    print("(Press Enter to skip a pin)")
    
    try:
        rpwm = input("RPWM (forward) pin: ").strip()
        lpwm = input("LPWM (reverse) pin: ").strip()
        r_en = input("R_EN (right enable) pin: ").strip()
        l_en = input("L_EN (left enable) pin: ").strip()
        
        pins_to_check = []
        if rpwm: pins_to_check.append((int(rpwm), "RPWM (forward)"))
        if lpwm: pins_to_check.append((int(lpwm), "LPWM (reverse)"))
        if r_en: pins_to_check.append((int(r_en), "R_EN (enable)"))
        if l_en: pins_to_check.append((int(l_en), "L_EN (enable)"))
        
        print("\n" + "=" * 60)
        print("PIN STATES (Initial Check)")
        print("=" * 60)
        
        for pin, name in pins_to_check:
            check_pin_state(pin, name)
        
        # Now set enable pins HIGH and check again
        if r_en or l_en:
            print("\n" + "=" * 60)
            print("SETTING ENABLE PINS HIGH")
            print("=" * 60)
            
            if r_en:
                GPIO.setup(int(r_en), GPIO.OUT)
                GPIO.output(int(r_en), GPIO.HIGH)
                print(f"  Pin {r_en} (R_EN) set to HIGH")
            
            if l_en:
                GPIO.setup(int(l_en), GPIO.OUT)
                GPIO.output(int(l_en), GPIO.HIGH)
                print(f"  Pin {l_en} (L_EN) set to HIGH")
            
            time.sleep(0.5)
            
            print("\n" + "=" * 60)
            print("PIN STATES (After Setting Enable HIGH)")
            print("=" * 60)
            
            # Re-check all pins
            for pin, name in pins_to_check:
                GPIO.setup(pin, GPIO.IN)
                state = GPIO.input(pin)
                print(f"  Pin {pin:2d} ({name:15s}): {'HIGH (3.3V)' if state else 'LOW (0V)'}")
            
            print("\n✓ If enable pins show HIGH, they're working correctly")
            print("✓ Measure with multimeter: should see ~3.3V on enable pins")
        
        # Test PWM output
        if rpwm:
            print("\n" + "=" * 60)
            print("TESTING PWM OUTPUT")
            print("=" * 60)
            
            rpwm_pin = int(rpwm)
            GPIO.setup(rpwm_pin, GPIO.OUT)
            pwm = GPIO.PWM(rpwm_pin, 10000)
            pwm.start(50)
            
            print(f"\nRPWM (pin {rpwm}) PWM at 50% duty cycle for 3 seconds...")
            print("Measure with multimeter or oscilloscope - should see ~1.65V average")
            time.sleep(3)
            
            pwm.stop()
            print("PWM stopped")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        GPIO.cleanup()
        print("\n" + "=" * 60)
        print("GPIO CLEANUP COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    main()