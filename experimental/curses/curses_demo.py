import curses
import random

def main(stdscr):

  #stdscr.addstr(0,0, "Hello world!")

  pad = curses.newpad(500,500)

  #target = stdscr
  target = pad
  Y, X = target.getmaxyx()
  #stdscr.addstr(10,10, '%s,%s' % (Y,X))
  stdscr.refresh()

  for y in range(0, Y-1):
    for x in range(0, X-1):
      c = random.choice('abcdefghijklmnoprstuvwxyz')
      ci = ord(c)
      #ci = ord('a') + (x*x+y*y) % 26

      try:
        target.addch(y,x, ci)
      except curses.error:
        #print y, x, c, ci
        raise Exception(y, x, c, ci)

  y, x = 10, 10
  pad.refresh(y,x, 5,5, 20,75)
  #stdscr.refresh()


  while True:
    c = stdscr.getch()

    if c == ord('w'):
      y -=1
    elif c == ord('a'):
      x -= 1
    elif c == ord('s'):
      y += 1
    elif c == ord('d'):
      x += 1

    elif c == ord('q'):
      break

    pad.refresh(y,x, 5,5, 20,75)



if __name__ == '__main__':
  curses.wrapper(main)
