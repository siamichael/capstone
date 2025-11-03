# Capstone
## differential_steering.py
Given a one-handed VR controller with one joystick and A, B, X, Y buttons oriented like

```
       X (top)
A (left)     Y (right)
      B (bottom)
```

when holding the controller vertically with the joystick on the top, this code 
- controls the up and down movement of the linear actuator using the **X button** for up and the **B button** for down
- controls forward and back movement based on the position of the joystick from the center on the y-axis
  - positive value (10 - 100) for forward, negative value (-10, 100) for backwards
- controls the pivot/turn based on the position of the joystick from the center on the x-axis
  - positive value (10 - 100) for right turn, negative value (-10, 100) for left turn
- controls the speed of movement
  - 0 = no movement, |100| = fastest movement

## motor_driver.py
Controls one motor driver, which controls one motor. Motor drivers are initialized with the GPIO pins they are connected to on the Raspberry Pi, and PWM objecs are defined for forward and backward movement. (...)

## robot.py
Manages the 4 individual motors and linear actuator and uses differential steering to drive the robot. 

(NOT FINISHED)
