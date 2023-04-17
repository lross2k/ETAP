from sense_hat import SenseHat
import time

screen = SenseHat()
screen.set_rotation(270)

# wall color
w = [255, 255, 255]
# u stands for 'uuuuh, this is a white LED?'
u = [248, 252, 248]
# path color
p = [0  , 0  , 0  ]
# ball color
b = [255, 0  , 0  ]
# hole color
h = [0  , 255, 0  ]
# s*ht another weird LED color
s = [0  , 252, 0  ]

# hard-coded tileset

lvl = [
w, w, w, w, w, w, w, w,
w, p, w, h, p, p, p, w,
w, p, w, w, w, w, p, w,
w, p, p, p, p, w, p, w,
w, p, w, w, p, p, p, w,
w, p, w, w, w, w, w, w,
w, p, p, p, p, p, p, w,
w, w, w, w, w, w, w, w
]

# render the map
screen.set_pixels(lvl)
x = 1
y = 1
dx = 0
dy = 0
# render the start position for player
screen.set_pixel(x,y,b)

while True:
  yaw = screen.get_orientation()["yaw"]
  # 270 > yaw > 180 : dy 1 dx 1
  if yaw < 270 and yaw >= 180:
    dy = 1
    dx = 1
  # 270 < yaw < 360 : dx 1 dy -1
  elif yaw >= 270 and yaw < 360:
    dy = -1
    dx = 1
  # 90 > yaw > 0 : dy -1 dx -1
  elif yaw >= 0 and yaw < 90:
    dy = -1
    dx = -1
  # 90 < yaw < 180 : dy 1 dx -1
  elif yaw > 90 and yaw <= 180:
    dy = 1
    dx = -1
  
  # if next tile is a wall, negate speed
  dx = 0 if screen.get_pixel(x+dx,y)==u else dx
  x += dx
  dy = 0 if screen.get_pixel(x,y+dy)==u else dy
  y += dy
  
  # show end screen
  if screen.get_pixel(x,y)==s:
    screen.show_message("Has ganado!, aun no hay mas niveles",scroll_speed=0.05,text_colour=h)
  
  # redraw the whole tileset, could be smarter, I know
  screen.set_pixels(lvl)
  # render new player position
  screen.set_pixel(x,y,b)
  time.sleep(1)
