"""
differential steering algorithm
converts joystick X/Y input into left/right motor speeds
"""

class DifferentialSteering:
    def __init__(self, pivot_y_limit=25):
        """
        initialize differential steering
        
        Args:
            pivot_y_limit: threshold for pivot turning (0-100)
                          higher = more range for pivot turns
                          default 25 = pivot when joystick is in center 25% range
        """
        self.pivot_y_limit = pivot_y_limit
        self.left_motor = 0
        self.right_motor = 0
        self.compute_range = 100
    
    def compute_motors(self, x_value, y_value):
        """
        compute left and right motor speeds from joystick input
        
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
        # calculate drive turn output due to X input
        if y_value >= 0:
            # forward
            if x_value >= 0:
                mot_premix_l = self.compute_range
                mot_premix_r = self.compute_range - x_value
            else:
                mot_premix_l = self.compute_range + x_value
                mot_premix_r = self.compute_range
        else:
            # reverse
            if x_value >= 0:
                mot_premix_l = self.compute_range - x_value
                mot_premix_r = self.compute_range
            else:
                mot_premix_l = self.compute_range
                mot_premix_r = self.compute_range + x_value
        
        # scale drive output due to y input
        mot_premix_l = mot_premix_l * y_value / self.compute_range
        mot_premix_r = mot_premix_r * y_value / self.compute_range
        
        # calculate pivot
        piv_speed = x_value
        
        # determine pivot blending based on y position
        if abs(y_value) > self.pivot_y_limit:
            piv_scale = 0.0  # no pivot
        else:
            piv_scale = 1.0 - abs(y_value) / self.pivot_y_limit
        
        # mix of drive and pivot
        self.left_motor = int((1.0 - piv_scale) * mot_premix_l + piv_scale * piv_speed)
        self.right_motor = int((1.0 - piv_scale) * mot_premix_r + piv_scale * (-piv_speed))
        
        return self.left_motor, self.right_motor
    
    def get_left_motor(self):
        """get last computed left motor speed"""
        return self.left_motor
    
    def get_right_motor(self):
        """get last computed right motor speed"""
        return self.right_motor