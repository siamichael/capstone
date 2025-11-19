"""
8-direction joystick mapper
Converts joystick into 8 discrete directions based on x/y thresholds
"""

class EightDirectionJoystick:
    def __init__(self, pivot_y_limit=25):
        """
        Initialize 8-direction joystick mapper
        
        Args:
            pivot_y_limit: Not used in this version, kept for compatibility
        """
        self.pivot_y_limit = pivot_y_limit
        self.left_motor = 0
        self.right_motor = 0
        self.compute_range = 100
    
    def compute_motors(self, x_value, y_value):
        """
        Compute left and right motor speeds from joystick input
        
        Args:
            x_value: turn input (-100 to 100)
                    negative = turn left
                    positive = turn right
            y_value: drive input (-100 to 100)
                    negative = reverse
                    positive = forward
        
        Returns:
            (left_motor, right_motor): motor speeds in range -100 to 100
        """
        if x_value == 0 and y_value == 0:
            self.left_motor = 0
            self.right_motor = 0
            return self.left_motor, self.right_motor
        
        # calculate magnitude for speed (pythagorean theorem)
        magnitude = int((x_value**2 + y_value**2)**0.5)
        if magnitude > self.compute_range:
            magnitude = self.compute_range
        
        # threshold for diagonal detection (tan(22.5°) ≈ 0.414)
        threshold = 0.4142135623730950488016887242097
        
        abs_x = abs(x_value)
        abs_y = abs(y_value)
        
        # determine which section based on x/y ratio and signs
        if y_value > 0:
            # forward half (top half of joystick)
            if abs_x < abs_y * threshold:
                # forward section (mostly Y, little X)
                self.left_motor = magnitude
                self.right_motor = magnitude
            elif x_value > 0:
                if abs_y < abs_x * threshold:
                    # right section (mostly X, little Y)
                    self.left_motor = magnitude
                    self.right_motor = -magnitude
                else:
                    # forward-right section (diagonal)
                    self.left_motor = magnitude
                    self.right_motor = 0
            else:  # x_value < 0
                if abs_y < abs_x * threshold:
                    # left section (mostly X, little Y)
                    self.left_motor = -magnitude
                    self.right_motor = magnitude
                else:
                    # forward-left section (diagonal)
                    self.left_motor = 0
                    self.right_motor = magnitude
        else:
            # backward half (bottom half of joystick)
            if abs_x < abs_y * threshold:
                # backward section (mostly Y, little X)
                self.left_motor = -magnitude
                self.right_motor = -magnitude
            elif x_value > 0:
                if abs_y < abs_x * threshold:
                    # right section (mostly X, little Y)
                    self.left_motor = magnitude
                    self.right_motor = -magnitude
                else:
                    # backward-right section (diagonal)
                    self.left_motor = -magnitude
                    self.right_motor = 0
            else:  # x_value < 0
                if abs_y < abs_x * threshold:
                    # left section (mostly X, little Y)
                    self.left_motor = -magnitude
                    self.right_motor = magnitude
                else:
                    # backward-left section (diagonal)
                    self.left_motor = 0
                    self.right_motor = -magnitude
        
        return self.left_motor, self.right_motor
    
    def get_left_motor(self):
        """get last computed left motor speed"""
        return self.left_motor
    
    def get_right_motor(self):
        """get last computed right motor speed"""
        return self.right_motor
