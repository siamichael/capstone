"""
bluetooth controller input handler
reads joystick and button inputs from controller
single joystick / one-handed
"""
import evdev
from evdev import ecodes

class BluetoothController:
    def __init__(self):
        """initialize bluetooth controller"""
        # find controller
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        self.controller = None
        for device in devices:
            device_name = device.name.lower()
            if "joy-con (r)" == device_name:
                self.controller = device
                print(f"Found controller: {device.name}")
                break
        
        if not self.controller:
            print("WARNING: No controller found!")
            print("Available devices:")
            for device in devices:
                print(f"  - {device.name}")
            raise Exception("No Bluetooth controller found!")
        
        # if controller disconnects, instead of program freezing, it continues main function and shuts off program if necessary
        flags = fcntl.fcntl(self.controller.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.controller.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        
        # initialize input values
        self.joystick_x = 0   # left/right turn (-100 to 100)
        self.joystick_y = 0   # forward/backward (-100 to 100)
        
        # buttons - when holding controller vertically
        self.button_x = False   # top button - raise tongue
        self.button_b = False   # bottom button - lower tongue
        self.button_y = False   # left button - (maybe decrease speed)
        self.button_a = False   # right button - (maybe increase speed)
        
        # joystick dead zone (ignore small movements near center)
        self.dead_zone = 10

        # track if controller sent events
        self.received_events_this_frame = False
    
    def read_events(self):
        """
        read controller events and update values
        call this repeatedly in your main loop
        """
        self.received_events_this_frame = False

        try:
            for event in self.controller.read():
                self.received_events_this_frame = True
                
                if event.type == ecodes.EV_ABS:
                    # listening for joystick movement
                    if event.code == ecodes.ABS_RX:
                        # x-axis (left/right turn)
                        raw_value = int((event.value - 128) / 128 * 100) # this is assuming 0-255 range for controller, will have to change if found different
                        # apply dead zone
                        if abs(raw_value) < self.dead_zone:
                            self.joystick_x = 0
                        else:
                            self.joystick_x = raw_value
                    
                    elif event.code == ecodes.ABS_RY:
                        # y-axis (forward/backward)
                        raw_value = int((event.value - 128) / 128 * 100)
                        # apply dead zone
                        if abs(raw_value) < self.dead_zone:
                            self.joystick_y = 0
                        else:
                             # invert: up = forward = negative in raw, positive in our system
                            self.joystick_y = -raw_value # this is assuming 0-255 range where 0 = up and 255 = down (why we invert)
                
                elif event.type == ecodes.EV_KEY:
                    # listening for button press
                    #might have different button naming convention with controller (not sure yet)
                    if event.code == ecodes.BTN_NORTH:
                        self.button_x = (event.value == 1)
                    elif event.code == ecodes.BTN_SOUTH:
                        self.button_b = (event.value == 1)
                    elif event.code == ecodes.BTN_WEST:
                        self.button_y = (event.value == 1)
                    elif event.code == ecodes.BTN_EAST:
                        self.button_a = (event.value == 1)
        
        except BlockingIOError:
            # no events available right now
            pass
    
    def get_drive_values(self):
        """
        get current drive values from single joystick
        
        Returns:
            (forward_speed, turn_speed): Both in range -100 to 100
                forward_speed: Y-axis (up/down)
                turn_speed: X-axis (left/right)
        """
        return (self.joystick_y, self.joystick_x)
    
    def get_actuator_command(self):
        """
        get current actuator command
        
        Returns:
            "raise", "lower", or "stop"
        """
        if self.button_x:  # top button = X
            return "raise"
        elif self.button_b:  # bottom button = B
            return "lower"
        else:
            return "stop"

    """
    def get_speed_adjustment(self):
    
        get speed limit adjustment from side buttons - have speed still found from the x/y position of joystick, but have left/right buttons control the speed limit
        
        Returns:
            "increase", "decrease", or None

        if self.button_a:  # right button
            return "increase"
        elif self.button_y:  # left button
            return "decrease"
        else:
            return None
    
        """

    def is_connected(self):
        """check if controller is still connected"""
        try:
            self.controller.fileno()
            return True
        except:
            return False