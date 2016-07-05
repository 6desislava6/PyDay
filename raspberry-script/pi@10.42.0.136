import sys
import multilineMAX7219 as LEDMatrix

# Initialise the library and the MAX7219/8x8LED arrays
LEDMatrix.init()
try:
    messages = sys.argv[1::]
    LEDMatrix.brightness(3)
    LEDMatrix.scroll_message_horiz(messages)
    LEDMatrix.clear_all()

except KeyboardInterrupt:
    LEDMatrix.scroll_message_horiz(["", "Have a good PyDay!", ""], 1, 8)
LEDMatrix.clear_all()
