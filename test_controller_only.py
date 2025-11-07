# test_controller_only.py
# Check if controller is actually sending values

from controller import BluetoothController
import time

print("Testing controller input...")
print("Move joystick and watch values")
print("Press Ctrl+C to exit\n")

try:
    controller = BluetoothController()
    print("✅ Controller connected\n")
    
    while True:
        controller.read_events()
        forward, turn = controller.get_drive_values()
        
        print(f"Forward: {forward:4d} | Turn: {turn:4d}", end='\r')
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print("\n\nDone")
except Exception as e:
    print(f"❌ Error: {e}")