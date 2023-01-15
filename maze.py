from operator import truediv
from random import randrange
import random
import pygame
import sys
import pdb
pygame.init()

width = 1000
height = 1000
room_size = 50
player_size = room_size // 4
goal_size = room_size // 2
num_rooms = (width*height // room_size**2)
num_columns = width // room_size
num_rows = height // room_size


def generate_walls(index):
    ret = []

    cell_x = index
    cell_col = 0
    while cell_x >= num_columns:
        cell_x -= num_columns
        cell_col += 1

    cell_y = index
    cell_row = 0
    while cell_y >= num_rows:
        cell_y -= num_rows
        cell_row += 1

    cell_x *= room_size
    cell_y = cell_row * room_size

    # top wall
    if index - num_columns > 0:
        ret.append({
            "cells": [index, index - num_columns],
            "points": [(cell_x, cell_y), (cell_x + room_size, cell_y)]
        })
    #   bottom wall
    if (index + num_columns) < num_rooms:
        ret.append({
            "cells": [index, index + num_columns],
            "points": [(cell_x, cell_y + room_size), (cell_x + room_size, cell_y + room_size)]
        })
    # left wall
    if index % num_columns != 0:
        ret.append({
            "cells": [index - 1, index],
            "points": [(cell_x, cell_y), (cell_x, cell_y + room_size)]
        })
    # right wall
    if (index + 1) % num_columns != 0:
        ret.append({
            "cells": [index + 1, index],
            "points": [(cell_x + room_size, cell_y), (cell_x + room_size, cell_y + room_size)]
        })

    return ret


maze = {0}
_walls = [generate_walls(i) for i in range(num_rooms)]
walls = [wall for sublist in _walls for wall in sublist if wall["cells"][0] >=
         0 and wall["cells"][1] >= 0 and wall["cells"][0] < num_rooms and wall["cells"][1] < num_rooms]
swap = [1, 0]


def add_adjacent(i):
    for wall in walls:
        if i in wall["cells"]:
            prox = wall["cells"][swap[wall["cells"].index(i)]]
            if prox not in maze and prox not in adjacent:
                adjacent.append(prox)


def maze_adjacent(i):
    ret = []
    for wall in walls:
        if i in wall["cells"]:
            prox = wall["cells"][swap[wall["cells"].index(i)]]
            if prox in maze and prox not in ret:
                ret.append(prox)
    return ret


adjacent = []
current = 0
screen = pygame.display.set_mode((width, height))
player = pygame.Rect((room_size - player_size) // 2,
                     (room_size - player_size) // 2, player_size, player_size)
goal = pygame.Rect((width - room_size) + ((room_size - goal_size) // 2),
                   (height - room_size) + ((room_size - goal_size) // 2), room_size, room_size)
wall_rects = []
game_over = False
while True:
    screen.fill("medium purple")
    add_adjacent(current)
    if len(adjacent) > 0:
        current = adjacent[random.randrange(len(adjacent))]
        visited_adj = maze_adjacent(current)
        if len(visited_adj) == 0:
            pdb.set_trace()
        prox = visited_adj[random.randrange(len(visited_adj))]
        walls = [wall for wall in walls if prox not in wall["cells"]
                 or current not in wall["cells"]]
        maze.add(current)
        adjacent.remove(current)
    elif not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if player.left > 0:
                player = player.move(-1, 0)
                if ~player.collidelist(wall_rects):
                    player = player.move(1, 0)
        if keys[pygame.K_RIGHT]:
            if player.right < width:
                player = player.move(1, 0)
                if ~player.collidelist(wall_rects):
                    player = player.move(-1, 0)
        if keys[pygame.K_UP]:
            if player.top > 0:
                player = player.move(0, -1)
                if ~player.collidelist(wall_rects):
                    player = player.move(0, 1)
        if keys[pygame.K_DOWN]:
            if player.bottom < height:
                player = player.move(0, 1)
                if ~player.collidelist(wall_rects):
                    player = player.move(0, -1)
        if player.colliderect(goal):
            game_over = True
    wall_rects = [pygame.draw.line(
        screen, (255, 255, 255), wall["points"][0], wall["points"][1]) for wall in walls]
    pygame.draw.rect(screen, ("dark orange"), player)
    pygame.draw.rect(screen, ("medium blue"), goal)
    if game_over:
        font = pygame.font.SysFont(None, 72)
        img = font.render("You Win!", True, (0, 0, 255))
        rect = img.get_rect()
        rect.center = width // 2, height // 2
        screen.blit(img, rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()
    pygame.time.Clock().tick(240)
