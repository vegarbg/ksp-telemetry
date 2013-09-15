#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, pprint, pygame, math
from pygame.locals import *

SCREEN_INTERNAL_SIZE = (64, 128)
(XSIZE, YSIZE) = SCREEN_INTERNAL_SIZE
SCREEN_SIZE = (143, 260)
MAX_POLLS_PER_SECOND = 8

WHITE = (255, 255, 255) # Sets pixel
BLACK = (0, 0, 0) # Clears pixel

HEADING_TICK_HEIGHT_MAJOR = 3
HEADING_TICK_HEIGHT_INTERMEDIATE = 2
HEADING_TICK_HEIGHT_MINOR = 1
HEADING_DISPLAY_OFFSET = 10.5 # pixels the 0 indicator is offset to the right
PITCH_DISPLAY_OFFSET = +0.5 # pixels the 0 indicator is offset below

# Initialize PyGame/SDL
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE, DOUBLEBUF)
drawsurface = pygame.Surface(SCREEN_INTERNAL_SIZE)

# Load fonts
font_m = pygame.font.Font("tom-thumb.bdf", 6)
font_s = pygame.font.Font("Resolution-3x3.ttf", 4)

# Render heading display and store it
headingdisplay = pygame.Surface((720, 8))
for x in range(0, 720, 20):
    pygame.draw.line(headingdisplay, WHITE, (x, 0), (x, HEADING_TICK_HEIGHT_INTERMEDIATE), 1)
    for c in range(2, 10, 2):
        pygame.draw.line(headingdisplay, WHITE, (x + c, 0), (x + c, HEADING_TICK_HEIGHT_MINOR), 1)

    pygame.draw.line(headingdisplay, WHITE, (x + 10, 0), (x + 10, HEADING_TICK_HEIGHT_MAJOR), 1)
    degree = font_s.render("%d" % (x/2), False, WHITE, BLACK)
    headingdisplay.blit(degree, (x + 10 - math.trunc(degree.get_width() / 2) + 1, HEADING_TICK_HEIGHT_MAJOR + 1))

    for c in range(12, 20, 2):
        pygame.draw.line(headingdisplay, WHITE, (x + c, 0), (x + c, HEADING_TICK_HEIGHT_MINOR), 1)

# Load pitch display (without text)
pitchscale = pygame.image.load("pitch-roll-indicator.png")
pitchdisplay = pygame.Surface((118, 118))

# Create surface for roll gimbal
rolldisplay = None

# Load level indicator
levelindicator = pygame.image.load("level-indicator.png")

# Draw loop
mainloop = True
while mainloop:
    clock.tick(MAX_POLLS_PER_SECOND)
    eventQueue = pygame.event.get()
    drawsurface.fill(BLACK)

    # DNS resolution eats a lot of time (> 500 ms per request), so we avoid that
    r = requests.get('http://127.0.0.1:8085/telemachus/datalink?a0=v.missionTime&a1=v.lat&a2=v.long&a3=n.pitch&a4=n.heading&a5=n.roll&a6=b.name&p=p.paused')
    json = r.json()

    # Render heading display
    drawsurface.blit(headingdisplay, (json["a4"] / 360 * -1 * headingdisplay.get_width() + XSIZE / 2.0 - HEADING_DISPLAY_OFFSET, 0))
    if json["a4"] / 360 < 0.5:
        # Add an extra length of heading display on the left, so we can scroll past 0
        drawsurface.blit(headingdisplay, (json["a4"] / 360 * -1 * headingdisplay.get_width() - headingdisplay.get_width() + XSIZE / 2.0 - HEADING_DISPLAY_OFFSET - 1, 0))
    else:
        # Add an extra length of heading display on the right, so we can scroll past 360
        drawsurface.blit(headingdisplay, (json["a4"] / 360 * -1 * headingdisplay.get_width() + headingdisplay.get_width() + XSIZE / 2.0 - HEADING_DISPLAY_OFFSET + 1, 0))

    # Render pitch/roll display
    pitchdisplay.fill(BLACK)
    pitchdisplay.blit(pitchscale, ((pitchdisplay.get_width() - pitchscale.get_width()) / 2.0, json["a3"] / 180 * pitchscale.get_height() / 2.0 - pitchscale.get_height() / 2.0 + pitchdisplay.get_height() / 2.0 - PITCH_DISPLAY_OFFSET))
    rolldisplay = pygame.transform.rotate(pitchdisplay, json["a5"])
    cropped = pygame.Surface((64, 83))
    newx = math.ceil( (rolldisplay.get_width() - cropped.get_width()) / 2.0 )
    newy = math.ceil( (rolldisplay.get_height() - cropped.get_height()) / 2.0 )
    cropped.blit(rolldisplay, (0, 0), (newx, newy, cropped.get_width(), cropped.get_height()))
    drawsurface.blit(cropped, (0, 9))

    # Render level indicator
    drawsurface.blit(levelindicator, (0, 51))

    # Testing: Write text
    textsurface = font_m.render("MST %d" % json["a0"], False, WHITE, BLACK)
    drawsurface.blit(textsurface, (0, YSIZE-35))
    textsurface = font_m.render("LAT %.2f" % json["a1"], False, WHITE, BLACK)
    drawsurface.blit(textsurface, (0, YSIZE-29))
    textsurface = font_m.render("LNG %.2f" % json["a2"], False, WHITE, BLACK)
    drawsurface.blit(textsurface, (0, YSIZE-23))
    textsurface = font_m.render("PIT %.2f" % json["a3"], False, WHITE, BLACK)
    drawsurface.blit(textsurface, (0, YSIZE-17))
    textsurface = font_m.render("HDG %.2f" % json["a4"], False, WHITE, BLACK)
    drawsurface.blit(textsurface, (0, YSIZE-11))
    textsurface = font_m.render("ROL %.2f" % json["a5"], False, WHITE, BLACK)
    drawsurface.blit(textsurface, (0, YSIZE-5))

    # Process remaining events in the event queue
    for event in eventQueue:
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
    eventQueue = []

    pygame.transform.scale(drawsurface, SCREEN_SIZE, screen)
    pygame.display.flip()

# Clean up before exiting
pygame.quit()
