import board, digitalio
import storage

button = digitalio.DigitalInOut(board.GP16)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Disable devices pin 16 button is not pressed
# when you've tested everything and make sure it works, uncomment the following lines
# if button.value:
    # storage.disable_usb_drive()