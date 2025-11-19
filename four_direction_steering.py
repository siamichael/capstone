"""
4-direction joystick
"""

class FourDirectionJoystick:
    def __init__(self, pivot_y_limit=25):
        """
        initialize 4-direction joystick mapper
        
        Args:
            pivot_y_limit: not used in this version, kept for compatibility
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
        
        # determine which section based on dominant axis
        abs_x = abs(x_value)
        abs_y = abs(y_value)
        
        if abs_y > abs_x:
            # y-axis dominant (forward or backward section)
            if y_value > 0:
                # forward section
                self.left_motor = magnitude
                self.right_motor = magnitude
            else:
                # backward section
                self.left_motor = -magnitude
                self.right_motor = -magnitude
        else:
            # x-axis dominant (left or right section)
            if x_value > 0:
                # right section
                self.left_motor = magnitude
                self.right_motor = -magnitude
            else:
                # left section
                self.left_motor = -magnitude
                self.right_motor = magnitude
        
        return self.left_motor, self.right_motor
    
    def get_left_motor(self):
        """get last computed left motor speed"""
        return self.left_motor
    
    def get_right_motor(self):
        """get last computed right motor speed"""
        return self.right_motor