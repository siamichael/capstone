"""
GPIO shutdown button listener
hold button for 2 seconds to trigger shutdown
button connected to GPIO3
"""
from gpiozero import Button
from subprocess import check_call
from signal import pause

def shutdown():
    print("Shutdown button pressed - shutting down safely...")
    check_call(['sudo', 'poweroff'])

shutdown_button = Button(3, hold_time=2)

shutdown_button.when_held = shutdown

print("Shutdown button listener started on GPIO3")
print("Hold button for 2 seconds to shutdown")

pause()