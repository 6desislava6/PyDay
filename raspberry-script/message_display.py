import multilineMAX7219 as LEDMatrix


def display_messages(messages):
    LEDMatrix.init()
    try:
        LEDMatrix.brightness(3)
        LEDMatrix.scroll_message_horiz(messages)
        LEDMatrix.clear_all()
    except KeyboardInterrupt:
        LEDMatrix.scroll_message_horiz(["", "Have a good PyDay!", ""], 1, 8)
    LEDMatrix.clear_all()
