import time
from math import pi
from Camera import Camera
import pygame as pg
import numpy as np
from DrawObjects import DrawObject

pg.init()
W, H = 800, 600
screen = pg.display.set_mode((W, H))
size = 100
camera = Camera(screen)

vertexes = [[-1.5, -0.5, -0.5],
            [1.5, -0.5, -0.5],
            [1.5, 0.5, -0.5],
            [-1.5, 0.5, -0.5],
            [-1.5, -0.5, 0.5],
            [1.5, -0.5, 0.5],
            [1.5, 0.5, 0.5],
            [-1.5, 0.5, 0.5]]

faces = [[0, 1, 2, 3],
         [4, 5, 6, 7],
         [0, 1, 5, 4],
         [2, 3, 7, 6],
         [0, 3, 7, 4],
         [1, 2, 6, 5]]

brusok = DrawObject(vertexes, [], faces)
brusok.resize(size)
brusok.displace([W // 2, H // 2, 0])
brusok.set_angle_x(0)
brusok.set_angle_y(0)
brusok.set_angle_z(0)

camera.set_position(5, -1, 3)
camera.set_orthographic_projection(W // 2, H // 2, 1)

running = True
rotation_direction = 1
rotation_angle = 0
rotation_speed = 2

while running:
    screen.fill((0, 0, 0))
    camera.render(brusok)
    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    rotation_angle += rotation_direction * rotation_speed

    if rotation_angle >= 120:
        rotation_direction = -1
    elif rotation_angle <= -60:
        rotation_direction = 1

    brusok.set_angle_x(rotation_angle)
 
    '''keys = pg.key.get_pressed()
    if keys[pg.K_q]:  # Вверх по оси Y
        camera.look_at(camera.x, camera.y - 0.1, camera.z)
    if keys[pg.K_e]:  # Вниз по оси Y
        camera.look_at(camera.x, camera.y + 0.1, camera.z)
    if keys[pg.K_w]:  # Вперед по оси Z
        camera.look_at(camera.x, camera.y, camera.z - 0.1)
    if keys[pg.K_s]:  # Назад по оси Z
        camera.look_at(camera.x, camera.y, camera.z + 0.1)
    if keys[pg.K_a]:  # Влево по оси X
        camera.look_at(camera.x - 0.1, camera.y, camera.z)
    if keys[pg.K_d]:  # Вправо по оси X
        camera.look_at(camera.x + 0.1, camera.y, camera.z)
    print(f"Camera position: ({camera.x}, {camera.y}, {camera.z})")'''

    time.sleep(0.05)

pg.quit()
