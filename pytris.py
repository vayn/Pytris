#!/usr/bin/env python2
# vim:fileencoding=utf-8
# @Name: pytris.py
# @Date: 2011年02月26日 星期六 15时56分56秒

import os
import pygame
import states

__author__ = "Vayn a.k.a. VT"
__copyright__ = "Copyright (c) 2011, Vincent Tsai"

__license__ = "GPL3"
__version__ = "0.1.0"
__email__ = "vayn@vayn.de"
__status__ = "Development"

__metaclass__ = type

class Game:
  def __init__(self):
    self.dir = os.path.split(os.path.abspath(__file__))[0]
    os.chdir(self.dir)
    self.state = None
    self.nextState = states.StartUp()

  def run(self):
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((states.WINDOWWIDTH, states.WINDOWHEIGHT), states.NOFRAME)
    pygame.display.set_caption('Pytris ' + __version__)
    pygame.mouse.set_visible(False)

    icon = pygame.image.load(states.loadData('icon.png', 'image')).convert()
    icon = pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)

    while True:
      clock.tick(states.FPS)
      if self.state != self.nextState:
        self.state = self.nextState
        self.state.firstDisplay(screen)
      for event in pygame.event.get():
        self.state.handle(event)
      self.state.update(self)
      self.state.display(screen)

if __name__ == '__main__':
  game = Game()
  game.run()

