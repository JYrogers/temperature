import board
import terminalio
import displayio
from analogio import AnalogIn
from fourwire import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from adafruit_ms8607 import MS8607
i2c = board.I2C()
pht = MS8607(i2c)
import time
BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0xFFFFF
FOREGROUND_COLOR = 0xAA0088
TEXT_COLOR = 0xFFFF00
displayio.release_displays()
spi = board.SPI()
tft_cs = board.D2
tft_dc = board.D3
dbuss = FourWire(spi, command = tft_dc, chip_select = tft_cs)
display = ST7789(dbuss, rotation = 270, width = 240, height = 135, rowstart =40, colstart = 53)
splash = displayio.Group()
display.root_group = splash
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader = color_palette, x =0, y= 0)
splash.append(bg_sprite)
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.polygon import Polygon

tmp = AnalogIn(board.A0)


try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789

BORDER = 20
FONTSCALE = 2
BACKGROUND_COLOR = 0x00FF00
FOREGROUND_COLOR = 0xAA0088  
TEXT_COLOR = 0xFFFF00

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D2
tft_dc = board.D3

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

inner_bitmap = displayio.Bitmap(
    display.width - BORDER * 2, display.height - BORDER * 2, 1
)
inner_palette = displayio.Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
splash.append(inner_sprite)




def display_text(text):
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)
    splash.append(text_group)
    time.sleep(3.0)
    splash.remove(text_group)

while True:
    pressure = pht.pressure
    print(pressure)
    display_text(str(pressure) + " Pa")
    
    
    tempC = (tmp.value / 65535 * 3.5 - 0.5) * 100
    tempF = (tempC * 9/5) + 32
    tempF = int(tempF * 100) / 100  
    print(tempF)
    display_text(str(tempF) + " Fa")
    
    humidity = pht.relative_humidity
    print(humidity)
    display_text(str(humidity) + " g/kg")
