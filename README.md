# Capstone Robot Control System

A Raspberry Pi-based robot control system using a Nintendo Switch Joy-Con (R) controller for wireless operation of a four-wheeled robot with 8-direction discrete steering and a linear actuator.

## Hardware Components

- **Raspberry Pi 3 Model A+**
- **Nintendo Switch Joy-Con (R) controller** (Bluetooth)
- **4x BTS7960 motor drivers** (for drive motors)
- **1x BTS7960 motor driver** (for linear actuator)
- **4x Drive motors** (8-direction steering configuration)
- **1x Linear actuator** (18" travel for tongue lifting)
- **Piezo buzzer** (audio feedback on GPIO 27)

## System Architecture

### File Structure
```
capstone/
├── main.py                      # Main control loop and system initialization
├── controller.py                # Bluetooth controller input handler
├── robot.py                     # High-level robot control and motor coordination
├── motor_driver.py              # Low-level motor driver control with PWM
├── eight_direction_steering.py  # 8-direction discrete steering algorithm
├── buzzer.py                    # Audio feedback system
└── bluetooth_autoconnect.sh     # Auto-connect controller on boot
```

### System Services

- **robot.service** - Auto-starts robot control system on boot
- **bluetooth-autoconnect.service** - Auto-connects Joy-Con controller

## Controller Layout
```
When holding the Joy-Con (R) vertically with the joystick at the top: 
          [Trigger]  (hold to enable controls)
 
          [Joystick]

            X (top)
        Raise actuator

     Y (left)     A (right)     
    Hitch Mode   Drive Mode
  
           B (bottom)
         Lower actuator
```

### Controls

| Input | Function | Range |
|-------|----------|-------|
| **Trigger (hold)** | Enable all controls | Required for operation |
| **Joystick Y-axis** | Forward/Backward | +100 (forward) to -100 (backward) |
| **Joystick X-axis** | Left/Right turn | +100 (right) to -100 (left) |
| **Button A (right)** | **Drive Mode** | **100% max speed** |
| **Button Y (left)** | **Hitch Mode** | **50% max speed (precision)** |
| **X Button** | Raise actuator | While held |
| **B Button** | Lower actuator | While held |
| **Dead zone** | Ignore small movements | ±10 from center |

### Operating Modes

**Drive Mode (100% Speed):**
- Full-speed operation for normal driving
- Best for: Moving between locations, general operation
- Activated by: Button A (right)
- Feedback: Two quick high beeps (4500Hz)

**Hitch Mode (50% Speed):**
- Reduced speed for precision control
- Best for: Positioning, hitching trailers, tight spaces
- Activated by: Button Y (left)
- Feedback: Two quick low beeps (3500Hz)

**Mode switching is instant** - operator can switch anytime during operation. Current mode persists through controller disconnections and reconnections.

### Safety Features

- **Dead zone**: ±10 unit dead zone on joystick to ignore drift
- **Command timeout**: 1.5 second timeout - stops all motors if no input received
- **Auto-reconnection**: Automatically reconnects if controller disconnects
- **Emergency stop**: All motors stop immediately on controller disconnect
- **Acceleration ramping**: Smooth acceleration/deceleration (300 units/sec for drive, 200 for actuator)
- **Event timeout**: Clears all inputs if no controller events for 1 second

## Steering System

The system uses **8-direction discrete steering** for precise, predictable control:
```
Forward-Left    Forward    Forward-Right
     ↖           ↑             ↗
Left ←        [Center]        → Right     
     ↙           ↓             ↘
Backward-Left  Backward  Backward-Right
```

### Advantages of 8-Direction Steering

- **Predictable movement**: Clear directional feedback
- **Easier control**: Operators can anticipate robot behavior
- **Consistent speed**: Same speed in each direction
- **Precise positioning**: Better for alignment tasks
- **Intuitive operation**: Natural mapping to joystick positions

### Motor Control Per Direction

| Direction | Left Motor | Right Motor | Result |
|-----------|------------|-------------|--------|
| **Forward** | +speed | +speed | Both motors forward |
| **Forward-Right** | +speed | 0 | Left forward, right stopped |
| **Right** | +speed | -speed | Pivot turn right |
| **Backward-Right** | -speed | 0 | Left backward, right stopped |
| **Backward** | -speed | -speed | Both motors backward |
| **Backward-Left** | 0 | -speed | Left stopped, right backward |
| **Left** | -speed | +speed | Pivot turn left |
| **Forward-Left** | 0 | +speed | Left stopped, right forward |

## Code Components

### main.py
Main control program that:
- Initializes robot hardware and GPIO
- Manages Bluetooth controller connection with auto-reconnect
- Implements main control loop (20Hz update rate)
- Handles graceful shutdown on SIGTERM/SIGINT
- Monitors controller connection status
- Implements safety timeout for lost controller connection
- Routes controller input to appropriate robot functions

### controller.py
Bluetooth controller input handler using `evdev` library:
- Detects and connects to "Joy-Con (R)" controller
- Reads joystick position (X/Y axes)
- Reads button states (X, B, Y, A, trigger)
- Implements dead zone filtering (±10)
- Provides methods to check connection status
- Auto-clears inputs after 1 second of no events (safety feature)
- Tracks event timing for timeout detection

### robot.py
High-level robot control:
- Manages 4 drive motors + 1 actuator motor
- Implements **8-direction discrete steering** for drive motors
- Provides `drive()`, `raise_tongue()`, `lower_tongue()` methods
- Configurable max speed limiting
- Configurable acceleration for smooth operation
- Emergency stop functionality for all motors
- GPIO cleanup on shutdown

**Key Methods:**
- `drive(x_input, y_input)` - Control robot movement
- `raise_tongue(speed)` - Raise linear actuator
- `lower_tongue(speed)` - Lower linear actuator
- `stop_all()` - Emergency stop all motors
- `update()` - Apply acceleration ramping to all motors

### motor_driver.py
Low-level motor control for BTS7960 drivers:
- PWM control at 10kHz frequency
- Forward/reverse direction control via separate pins
- Acceleration ramping for smooth starts/stops
- Emergency stop with immediate PWM cutoff and GPIO LOW
- Speed range: -100 (full reverse) to +100 (full forward)
- Independent control of each motor

**Key Methods:**
- `set_speed(speed)` - Set target speed with ramping
- `set_speed_instant(speed)` - Set speed immediately
- `emergency_stop()` - Immediate stop with GPIO LOW
- `update()` - Apply acceleration ramping

### eight_direction_steering.py
Converts joystick input to discrete 8-direction control:
- Maps continuous joystick input to 8 discrete directions
- Uses angular thresholds (22.5° divisions) to determine direction
- Speed magnitude calculated from joystick distance from center (Pythagorean theorem)
- Output range: -100 to +100 for each motor

**Algorithm:**
1. Calculate joystick magnitude: `sqrt(x² + y²)`
2. Determine sector using threshold (tan(22.5°) ≈ 0.414)
3. Compare X/Y ratio to determine which 45° sector
4. Assign motor speeds based on sector
5. Speed is constant within each direction

**Direction Detection:**
- If `|x| < |y| × 0.414`: Primarily vertical movement
- If `|y| < |x| × 0.414`: Primarily horizontal movement
- Otherwise: Diagonal movement

### buzzer.py
Audio feedback system using PWM-controlled piezo buzzer:
- Provides audio cues for system events
- Different tones for different events
- PWM control at variable frequencies (1kHz base)

**Audio Feedback Events:**

| Event | Sound Pattern | Frequency |
|-------|---------------|-----------|
| **Controller Connected** | Rising 3-tone beep (ascending) | 3500Hz → 4000Hz → 4500Hz |
| **Controller Disconnected** | Falling 3-tone beep (descending) | 4500Hz → 4000Hz → 3500Hz |
| **Drive Mode** | Two quick high beeps | 4500Hz × 2 |
| **Hitch Mode** | Two quick low beeps | 3500Hz × 2 |
| **Error** | Three rapid beeps | 4000Hz × 3 |

**Key Methods:**
- `beep(frequency, duration)` - Single beep at specified frequency
- `connect_sound()` - Play connection success sound
- `disconnect_sound()` - Play disconnection sound
- `drive_mode_sound()` - Indicate drive mode active
- `hitch_mode_sound()` - Indicate hitch mode active
- `error_sound()` - Play error alert
- `cleanup()` - Stop PWM and cleanup GPIO

### bluetooth_autoconnect.sh
Bash script for automatic controller connection:
- Runs on boot via systemd service
- Searches for paired Joy-Con controller by MAC address
- Attempts connection every 5 seconds
- Infinite retry loop until connected
- Restarts Bluetooth service if needed after 60 attempts (5 minutes)
- Provides status messages for debugging

## GPIO Pin Assignments

| Component | RPWM Pin (Forward) | LPWM Pin (Reverse) | Notes |
|-----------|-------------------|-------------------|-------|
| Front Left Motor | GPIO 17 | GPIO 4 | |
| Front Right Motor | GPIO 15 | GPIO 18 | |
| Rear Left Motor | GPIO 5 | GPIO 11 | |
| Rear Right Motor | GPIO 23 | GPIO 24 | |
| Actuator | GPIO 19 | GPIO 26 | |
| **Buzzer** | **GPIO 27** | - | **PWM output** |
