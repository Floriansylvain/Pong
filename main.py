#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
import sys
import os
import pygame
from pygame.locals import *

WIDTH = 900
HEIGHT = 600

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
window = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont('consolas', 48)
clock = pygame.time.Clock()

LOOP = True


def main():

    # Initialisation

    if os.name == 'posix':
        path_txt = os.path.abspath(os.path.dirname(sys.argv[0])) + r'/'
        icon = pygame.image.load(os.path.abspath(path_txt
                                 + 'icon/icon1.jpg'))
        s_ping = pygame.mixer.Sound(path_txt + 'songs/ping.ogg')
        s_pong = pygame.mixer.Sound(path_txt + 'songs/pong.ogg')
        s_lose = pygame.mixer.Sound(path_txt + 'songs/lose.ogg')
    else:
        path_txt = os.path.abspath(os.path.dirname(sys.argv[0])) \
            + chr(92)
        icon = pygame.image.load(os.path.abspath(path_txt
                                 + r'icon\icon1.jpg'))
        s_ping = pygame.mixer.Sound(path_txt + r'songs\ping.ogg')
        s_pong = pygame.mixer.Sound(path_txt + r'songs\pong.ogg')
        s_lose = pygame.mixer.Sound(path_txt + r'songs\lose.ogg')

    pygame.display.set_caption('Le pong de Fallen')
    pygame.display.set_icon(icon)

    class Player:

        def __init__(
            self,
            x,
            y,
            width,
            height,
            vel,
            color,
            ):

            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = vel
            self.color = color

        def draw(self, window):
            pygame.draw.rect(window, self.color, (int(self.x),
                             int(self.y), self.width, self.height))

    black = (0, 0, 0)
    white = (255, 255, 255)

    player_1 = Player(
        10,
        224,
        25,
        150,
        1,
        white,
        )
    player_2 = Player(
        865,
        225,
        25,
        150,
        1,
        white,
        )
    pong = Player(
        425,
        275,
        50,
        50,
        7,
        white,
        )

    hfont = pygame.font.SysFont('consolas', 128)
    font = pygame.font.SysFont('consolas', 48)

    titre = hfont.render('Pong', True, (255, 255, 255))
    titre_pause = hfont.render('Pause', True, white)
    titre_pause_shadow = hfont.render('Pause', True, black)

    exit = font.render('Exit', True, white)
    play = font.render('Play', True, white)
    resume_txt = font.render('Resume', True, white)
    menu_txt = font.render('Menu', True, white)
    player_1_font = font.render('P1', True, white)
    player_2_font = font.render('P2', True, white)
    player_1_win_font = font.render(' P1 has win !', True, white)
    player_2_win_font = font.render(' P2 has win !', True, white)

    def play_sound(whs):
        if whs == 'ping':
            pygame.mixer.Sound.play(s_ping)
        if whs == 'pong':
            pygame.mixer.Sound.play(s_pong)
        if whs == 'lose':
            pygame.mixer.Sound.play(s_lose)

    def dashed_line():
        tracage_y = 0
        while tracage_y < 600:
            pygame.draw.line(window, (255, 255, 255), [450, tracage_y],
                             [450, tracage_y + 20], 5)
            tracage_y += 40

    def pong_direction(dir):
        if dir == 'left':
            pong.x -= pong.vel
        if dir == 'right':
            pong.x += pong.vel
        if dir == 'botRight':
            pong.x += pong.vel
            pong.y += pong.vel
        if dir == 'botLeft':
            pong.x -= pong.vel
            pong.y += pong.vel
        if dir == 'topRight':
            pong.x += pong.vel
            pong.y -= pong.vel
        if dir == 'topLeft':
            pong.x -= pong.vel
            pong.y -= pong.vel

    def game_loop():

        def render():
            window.fill((0, 0, 0))
            player_1.draw(window)
            player_2.draw(window)
            pong.draw(window)
            dashed_line()
            window.blit(counter_j1, (425 - counter_j1.get_width(), 0))
            window.blit(counter_j2, (475, 0))
            window.blit(player_1_font, (425
                        - player_1_font.get_width(), 600
                        - player_1_font.get_height()))
            window.blit(player_2_font, (475, 600
                        - player_2_font.get_height()))
            pygame.display.update()

        incremental_counter_j1 = 0
        incremental_counter_j2 = 0
        direction = 0
        old_direction = 0
        pong_dv = ''
        direction = random.randint(1, 2)

        player_1.x = 10
        player_1.y = 224
        player_2.x = 865
        player_2.y = 225

        # game loop

        global LOOP
        LOOP = True
        while LOOP:
            tiret = font.render('-', True, (255, 255, 255))

            def reset_game():
                play_sound('lose')
                pong.x = 425
                pong.y = 275
                pong.vel = 7

            delta_time = clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    LOOP = False
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            if player_1.y + player_1.height < HEIGHT:
                if keys[K_s]:
                    player_1.y += player_1.vel * delta_time
            if player_1.y > player_1.vel:
                if keys[K_w] or keys[K_z]:
                    player_1.y -= player_1.vel * delta_time
            if player_2.y + player_2.height < HEIGHT:
                if keys[K_DOWN]:
                    player_2.y += player_2.vel * delta_time
            if player_2.y > player_2.vel:
                if keys[K_UP]:
                    player_2.y -= player_2.vel * delta_time

            if keys[K_F10]:
                command = input('Cmd : ')
                if command == 'red':
                    pong.color = (255, 0, 0)
                    player_1.color = (255, 0, 0)
                    player_2.color = (255, 0, 0)
                elif command == 'green':
                    pong.color = (0, 255, 0)
                    player_1.color = (0, 255, 0)
                    player_2.color = (0, 255, 0)
                elif command == 'blue':
                    pong.color = (0, 0, 255)
                    player_1.color = (0, 0, 255)
                    player_2.color = (0, 0, 255)
                elif command == 'size':
                    pong.width += 100
                    pong.height += 100
                elif command == 'reset':
                    pong.width = 50
                    pong.height = 50
                    pong.color = (255, 255, 255)
                    player_1.color = (255, 255, 255)
                    player_2.color = (255, 255, 255)
                else:
                    print('Command unknow.')

            # collisions Player 1 debut de partie

            if direction == 1 and old_direction == 0:
                if pong.x > player_1.x + player_1.width:
                    pong_dv = 'left'
                    pong_direction(pong_dv)
                elif pong.y + pong.height > player_1.y and pong.y \
                    + pong.height / 2 < player_1.y + player_1.height \
                    / 2:
                    play_sound('ping')
                    pong_dv = 'topRight'
                    direction = 2
                    old_direction = 1
                elif pong.y < player_1.y + player_1.height and pong.y \
                    + pong.height / 2 > player_1.y + player_1.height \
                    / 2:
                    play_sound('ping')
                    pong_dv = 'botRight'
                    direction = 2
                    old_direction = 1
                else:

                # condition de fin

                    incremental_counter_j2 += 1
                    direction = 2
                    old_direction = 0
                    reset_game()

            # collisions Player 2 debut de partie

            if direction == 2 and old_direction == 0:
                if pong.x + pong.width < player_2.x:
                    pong_dv = 'right'
                    pong_direction(pong_dv)
                elif pong.y + pong.height > player_2.y and pong.y \
                    + pong.height / 2 < player_2.y + player_2.height \
                    / 2:
                    play_sound('pong')
                    pong_dv = 'topLeft'
                    direction = 1
                    old_direction = 2
                elif pong.y < player_2.y + player_2.height and pong.y \
                    + pong.height / 2 > player_2.y / 2 \
                    + player_2.height:
                    play_sound('pong')
                    pong_dv = 'botLeft'
                    direction = 1
                    old_direction = 2
                else:

                # condition de fin

                    incremental_counter_j1 += 1
                    direction = 1
                    old_direction = 0
                    reset_game()

            # collisions Player 1 en partie

            if direction == 2 and old_direction == 1:
                if pong.x + pong.width < player_2.x:
                    pong_direction(pong_dv)
                elif pong.y + pong.height > player_2.y and pong.y \
                    < player_2.y + player_2.height:
                    play_sound('pong')
                    if pong_dv == 'topRight':
                        pong_dv = 'topLeft'
                    if pong_dv == 'botRight':
                        pong_dv = 'botLeft'
                    direction = 1
                    old_direction = 2
                    pong.vel += 1
                else:

                # condition de fin

                    incremental_counter_j1 += 1
                    direction = 2
                    old_direction = 0
                    reset_game()

            # collisions Player 2 en partie

            if direction == 1 and old_direction == 2:
                if pong.x > player_1.x + player_1.width:
                    pong_direction(pong_dv)
                elif pong.y + pong.height > player_1.y and pong.y \
                    < player_1.y + player_1.height:
                    play_sound('ping')
                    if pong_dv == 'topLeft':
                        pong_dv = 'topRight'
                    if pong_dv == 'botLeft':
                        pong_dv = 'botRight'
                    direction = 2
                    old_direction = 1
                    pong.vel += 1
                else:

                # lose condition

                    incremental_counter_j2 += 1
                    direction = 1
                    old_direction = 0
                    reset_game()

            # collisions bords

            if pong.y <= pong.vel:
                if direction == 1:
                    pong_dv = 'botLeft'
                    pong_direction(pong_dv)
                if direction == 2:
                    pong_dv = 'botRight'
                    pong_direction(pong_dv)
            if pong.y >= HEIGHT - pong.height:
                if direction == 1:
                    pong_dv = 'topLeft'
                    pong_direction(pong_dv)
                if direction == 2:
                    pong_dv = 'topRight'
                    pong_direction(pong_dv)

            # Pause Menu

            if keys[K_ESCAPE]:
                pause = True
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pause = False
                            pygame.quit()
                            sys.exit()

                    surface = pygame.Surface((900, 600))

                    if os.name == 'posix':
                        surface.set_alpha(50)
                        surface.fill((20, 20, 20))
                    else:
                        surface.set_alpha(2)
                        surface.fill((50, 50, 50))

                    window.blit(surface, (0, 0),
                                special_flags=BLEND_MIN)

                    m_pos = pygame.mouse.get_pos()
                    m_c = pygame.mouse.get_pressed()

                    # Draw buttons

                    window.blit(titre_pause_shadow, (452
                                - int(titre_pause.get_width() / 2), 52))
                    window.blit(titre_pause, (450
                                - int(titre_pause.get_width() / 2), 50))

                    # resume animation

                    if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] \
                        > 250 and m_pos[1] < 340:
                        pygame.draw.rect(window, (255, 255, 255), (350,
                                250, 200, 90))
                        pygame.draw.rect(window, (255, 255, 255), (360,
                                260, 180, 70))
                        resume_txt = font.render('Resume', True, (0, 0,
                                0))
                    else:
                        pygame.draw.rect(window, (255, 255, 255), (350,
                                250, 200, 90))
                        pygame.draw.rect(window, (0, 0, 0), (360, 260,
                                180, 70))
                        resume_txt = font.render('Resume', True, white)

                    # menu animation

                    if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] \
                        > 360 and m_pos[1] < 450:
                        pygame.draw.rect(window, (255, 255, 255), (350,
                                360, 200, 90))
                        pygame.draw.rect(window, (255, 255, 255), (360,
                                370, 180, 70))
                        menu_txt = font.render('Menu', True, (0, 0, 0))
                    else:
                        pygame.draw.rect(window, (255, 255, 255), (350,
                                360, 200, 90))
                        pygame.draw.rect(window, (0, 0, 0), (360, 370,
                                180, 70))
                        menu_txt = font.render('Menu', True, white)

                    # exit animation

                    if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] \
                        > 470 and m_pos[1] < 560:
                        pygame.draw.rect(window, (255, 255, 255), (350,
                                470, 200, 90))
                        pygame.draw.rect(window, (255, 255, 255), (360,
                                480, 180, 70))
                        exit = font.render('Exit', True, (0, 0, 0))
                    else:
                        pygame.draw.rect(window, (255, 255, 255), (350,
                                470, 200, 90))
                        pygame.draw.rect(window, (0, 0, 0), (360, 480,
                                180, 70))
                        exit = font.render('Exit', True, white)

                    window.blit(resume_txt, (450
                                - int(resume_txt.get_width() / 2), 275))
                    window.blit(menu_txt, (450
                                - int(menu_txt.get_width() / 2), 385))
                    window.blit(exit, (450 - int(exit.get_width() / 2),
                                495))

                    # if resume is click

                    if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] \
                        > 250 and m_pos[1] < 340 and m_c == (1, 0, 0):
                        pause = False

                    # if menu is click

                    if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] \
                        > 360 and m_pos[1] < 450 and m_c == (1, 0, 0):
                        pong.x = 425
                        pong.y = 275
                        pause = False
                        LOOP = False
                        time.sleep(0.1)

                    # if exit is click

                    if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] \
                        > 470 and m_pos[1] < 560 and m_c == (1, 0, 0):
                        pause = False
                        LOOP = False
                        pygame.quit()
                        sys.exit()

                    pygame.display.update()
                    time.sleep(0.01)

            # game over

            counter_j1 = font.render(str(incremental_counter_j1), True,
                    (255, 255, 255))
            counter_j2 = font.render(str(incremental_counter_j2), True,
                    (255, 255, 255))
            render()
            if incremental_counter_j1 == 3 or incremental_counter_j2 \
                == 3:
                window.fill((0, 0, 0))
                window.blit(counter_j1, (400
                            - int(counter_j1.get_width()), 280))
                window.blit(counter_j2, (500, 280))
                window.blit(tiret, (435, 280))
                if incremental_counter_j1 == 3:
                    window.blit(player_1_win_font, (450
                                - int(player_1_win_font.get_width()
                                / 2), 220))
                else:
                    window.blit(player_2_win_font, (450
                                - int(player_2_win_font.get_width()
                                / 2), 220))
                pygame.display.update()
                pygame.time.wait(2000)
                LOOP = False

    # Game Menu

    menu_loop = True
    while menu_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_loop = False
        m_pos = pygame.mouse.get_pos()
        m_c = pygame.mouse.get_pressed()

        # if exit is click

        if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 360 \
            and m_pos[1] < 450 and m_c == (1, 0, 0):
            menu_loop = False

        # if play is click

        if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 250 \
            and m_pos[1] < 340 and m_c == (1, 0, 0):
            game_loop()

        window.fill((0, 0, 0))

        # animation play

        if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 250 \
            and m_pos[1] < 340:
            pygame.draw.rect(window, white, (350, 250, 200, 90))
            pygame.draw.rect(window, white, (360, 260, 180, 70))
            play = font.render('Play', True, black)
        else:
            pygame.draw.rect(window, white, (350, 250, 200, 90))
            pygame.draw.rect(window, black, (360, 260, 180, 70))
            play = font.render('Play', True, white)

        # animation exit

        if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 360 \
            and m_pos[1] < 450:
            pygame.draw.rect(window, white, (350, 360, 200, 90))
            pygame.draw.rect(window, white, (360, 370, 180, 70))
            exit = font.render('Exit', True, black)
        else:
            pygame.draw.rect(window, white, (350, 360, 200, 90))
            pygame.draw.rect(window, black, (360, 370, 180, 70))
            exit = font.render('Exit', True, white)

        window.blit(play, (450 - int(play.get_width() / 2), 275))
        window.blit(exit, (450 - int(play.get_width() / 2), 385))
        window.blit(titre, (450 - int(titre.get_width() / 2), 50))
        pygame.display.update()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
