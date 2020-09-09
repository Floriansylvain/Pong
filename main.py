import time, random, sys, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *

#Initialisation

WIDTH = 900
HEIGHT = 600
pathTxt = os.path.abspath(os.path.dirname(sys.argv[0])) + r'/'
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
window = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("consolas", 48)
clock = pygame.time.Clock()
icon = pygame.image.load(pathTxt + 'icon/icon1.jpg')
pygame.display.set_caption('Le pong de Fallen')
pygame.display.set_icon(icon)

class player(object):
	def __init__(self, x, y, width, height, vel):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = vel

	def draw(self, window):
		pygame.draw.rect(window, (255, 255, 255), (int(self.x), int(self.y), self.width, self.height))

joueur_1 = player(10, 224, 25, 150, 1)
joueur_2 = player(865, 225, 25, 150, 1)
pong = player(425, 275, 50, 50, 7)

s_ping = pygame.mixer.Sound(pathTxt + 'songs/ping.ogg')
s_pong = pygame.mixer.Sound(pathTxt + 'songs/pong.ogg')
s_lose = pygame.mixer.Sound(pathTxt + 'songs/lose.ogg')

n = (0, 0, 0)
b = (255,255,255)

Hfont = pygame.font.SysFont("consolas", 128)
font = pygame.font.SysFont("consolas", 48)

titre = Hfont.render('Pong', True, (255, 255, 255))
titre_pause = Hfont.render('Pause', True, b)
titre_pause_shadow = Hfont.render('Pause', True, n)

exit = font.render('Exit', True, b)
play = font.render('Play', True, b)
resume_txt = font.render('Resume', True, b)
menu_txt = font.render('Menu', True, b)
P1 = font.render('P1', True, b)
P2 = font.render('P2', True, b)
P1_win = font.render(' P1 has win !', True, b)
P2_win = font.render(' P2 has win !', True, b)

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
		pygame.draw.line(window, (255, 255, 255), [450,tracage_y], [450,tracage_y + 20], 5)
		tracage_y += 40

def pongDirection(dir):
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

def GameLoop():
	def render():
		window.fill((0, 0, 0))
		joueur_1.draw(window)
		joueur_2.draw(window)
		pong.draw(window)
		dashed_line()
		window.blit(counter_j1, ((425 - counter_j1.get_width()), 0))
		window.blit(counter_j2, (475, 0))
		window.blit(P1, (425 - P1.get_width(), 600 - P1.get_height()))
		window.blit(P2, (475, 600 - P2.get_height()))
		pygame.display.update()

	incremental_counter_j1 = 0
	incremental_counter_j2 = 0
	game_state = 0
	direction = 0
	old_direction = 0
	pongDV = ''
	direction = random.randint(1,2)
	
	joueur_1.x = 10
	joueur_1.y = 224
	joueur_2.x = 865
	joueur_2.y = 225

	global loop
	loop = True
	while loop:
		tiret = font.render('-', True, (255, 255, 255))

		def resetGame():
			play_sound('lose')
			game_state = 0
			pong.x = 425
			pong.y = 275
			pong.vel = 7

		dt = clock.tick(60)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				loop = False
				pygame.quit()
				sys.exit()

		keys = pygame.key.get_pressed()

		if joueur_1.y + joueur_1.height < HEIGHT: 
			if keys[K_s]:
				joueur_1.y += joueur_1.vel * dt
		if joueur_1.y > joueur_1.vel:
			if keys[K_w] or keys[K_z]:
				joueur_1.y -= joueur_1.vel * dt
		if joueur_2.y + joueur_2.height < HEIGHT: 
			if keys[K_DOWN]:
				joueur_2.y += joueur_2.vel * dt
		if joueur_2.y > joueur_2.vel:
			if keys[K_UP]:
				joueur_2.y -= joueur_2.vel * dt

		if game_state == 0:
			game_state = 1

		#collisions joueur 1 debut de partie
		if direction == 1 and old_direction == 0:
			if pong.x > joueur_1.x + joueur_1.width:
				pongDV = 'left'
				pongDirection(pongDV)
			elif pong.y + pong.height > joueur_1.y and pong.y + pong.height/2 < joueur_1.y + joueur_1.height/2:
				play_sound('ping')
				pongDV = 'topRight'
				direction = 2
				old_direction = 1
			elif pong.y < joueur_1.y + joueur_1.height and pong.y + pong.height/2 > joueur_1.y + joueur_1.height/2:
				play_sound('ping')
				pongDV = 'botRight'
				direction = 2
				old_direction = 1
			#condition de fin
			else:
				incremental_counter_j2 += 1
				direction = 2
				old_direction = 0
				resetGame()

		#collisions joueur 2 debut de partie
		if direction == 2 and old_direction == 0:
			if pong.x + pong.width < joueur_2.x:
				pongDV = 'right'
				pongDirection(pongDV)
			elif pong.y + pong.height > joueur_2.y and pong.y + pong.height/2 < joueur_2.y + joueur_2.height/2:
				play_sound('pong')
				pongDV = 'topLeft'
				direction = 1
				old_direction = 2
			elif pong.y < joueur_2.y + joueur_2.height and pong.y + pong.height/2 > joueur_2.y/2 + joueur_2.height:
				play_sound('pong')
				pongDV = 'botLeft'
				direction = 1
				old_direction = 2
			#condition de fin
			else:
				incremental_counter_j1 += 1
				direction = 1
				old_direction = 0
				resetGame()

		#collisions joueur 1 en partie
		if direction == 2 and old_direction == 1:
			if pong.x + pong.width < joueur_2.x:
				pongDirection(pongDV)
			elif pong.y + pong.height > joueur_2.y and pong.y < joueur_2.y + joueur_2.height:
				play_sound('pong')
				if pongDV == 'topRight':
					pongDV = 'topLeft'
				if pongDV == 'botRight':
					pongDV = 'botLeft'
				direction = 1
				old_direction = 2
				pong.vel += 1
			#condition de fin
			else:
				incremental_counter_j1 += 1
				direction = 2
				old_direction = 0
				resetGame()

		#collisions joueur 2 en partie
		if direction == 1 and old_direction == 2:
			if pong.x > joueur_1.x + joueur_1.width:
				pongDirection(pongDV)
			elif pong.y + pong.height > joueur_1.y and pong.y < joueur_1.y + joueur_1.height:
				play_sound('ping')
				if pongDV == 'topLeft':
					pongDV = 'topRight'
				if pongDV == 'botLeft':
					pongDV = 'botRight'
				direction = 2
				old_direction = 1
				pong.vel += 1
			#lose condition
			else:
				incremental_counter_j2 += 1
				direction = 1
				old_direction = 0
				resetGame()

		#collisions bords
		if pong.y <= pong.vel:
			if direction == 1:
				pongDV = 'botLeft'
				pongDirection(pongDV)
			if direction == 2:
				pongDV = 'botRight'
				pongDirection(pongDV)
		if pong.y >= HEIGHT - pong.height:
			if direction == 1:
				pongDV = 'topLeft'
				pongDirection(pongDV)
			if direction == 2:
				pongDV = 'topRight'
				pongDirection(pongDV)

		#Pause Menu
		if keys[K_ESCAPE]:
			pause = True
			while pause:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pause = False
						pygame.quit();
						sys.exit();

				s = pygame.Surface((900,600))
				
				if os.name == 'posix':
					s.set_alpha(50)
					s.fill((20,20,20))
				else:
					s.set_alpha(2)
					s.fill((50,50,50))
				
				window.blit(s, (0,0), special_flags=BLEND_MIN)

				m_pos = pygame.mouse.get_pos()
				m_c = pygame.mouse.get_pressed()

				#Draw buttons
				window.blit(titre_pause_shadow, ((452 - int(titre_pause.get_width()/2)), 52))
				window.blit(titre_pause, ((450 - int(titre_pause.get_width()/2)), 50))

				#resume animation
				if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 250 and m_pos[1] < 340:
					pygame.draw.rect(window, (200, 200, 200), (350, 250, 200, 90))
					pygame.draw.rect(window, (200, 200, 200), (360, 260, 180, 70))
					resume_txt = font.render('Resume', True, (20, 20, 20))
				else:
					pygame.draw.rect(window, (200, 200, 200), (350, 250, 200, 90))
					pygame.draw.rect(window, (20, 20, 20), (360, 260, 180, 70))
					resume_txt = font.render('Resume', True, b)
				#menu animation
				if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 360 and m_pos[1] < 450:
					pygame.draw.rect(window, (200, 200, 200), (350, 360, 200, 90))
					pygame.draw.rect(window, (200, 200, 200), (360, 370, 180, 70))
					menu_txt = font.render('Menu', True, (20, 20, 20))
				else:
					pygame.draw.rect(window, (200, 200, 200), (350, 360, 200, 90))
					pygame.draw.rect(window, (20, 20, 20), (360, 370, 180, 70))
					menu_txt = font.render('Menu', True, b)
				#exit animation
				if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 470 and m_pos[1] < 560:
					pygame.draw.rect(window, (200, 200, 200), (350, 470, 200, 90))
					pygame.draw.rect(window, (200, 200, 200), (360, 480, 180, 70))
					exit = font.render('Exit', True, (20, 20, 20))
				else:
					pygame.draw.rect(window, (200, 200, 200), (350, 470, 200, 90))
					pygame.draw.rect(window, (20, 20, 20), (360, 480, 180, 70))
					exit = font.render('Exit', True, b)

				window.blit(resume_txt, ((450 - int(resume_txt.get_width()/2)), 275))
				window.blit(menu_txt, ((450 - int(menu_txt.get_width()/2)), 385))
				window.blit(exit, ((450 - int(exit.get_width()/2)), 495))

				#if resume is click
				if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 250 and m_pos[1] < 340 and m_c == (1, 0, 0):
					pause = False

				#if menu is click
				if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 360 and m_pos[1] < 450 and m_c == (1, 0, 0):
					pong.x = 425
					pong.y = 275
					pause = False
					loop = False
					time.sleep(0.1)

				#if exit is click
				if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 470 and m_pos[1] < 560 and m_c == (1, 0, 0):
					pause = False
					loop = False
					pygame.quit();
					sys.exit();

				pygame.display.update()
				time.sleep(0.01)

		#game over
		counter_j1 = font.render(str(incremental_counter_j1), True, (255, 255, 255))
		counter_j2 = font.render(str(incremental_counter_j2), True, (255, 255, 255))
		render()
		if incremental_counter_j1 == 3 or incremental_counter_j2 == 3:
			window.fill((0, 0, 0))
			window.blit(counter_j1, ((400 - int(counter_j1.get_width()), 280)))
			window.blit(counter_j2, (500, 280))
			window.blit(tiret, (435, 280))
			if incremental_counter_j1 == 3:
				window.blit(P1_win, (450 - int(P1_win.get_width()/2), 220))
			else:
				window.blit(P2_win, (450 - int(P2_win.get_width()/2), 220))
			pygame.display.update()
			pygame.time.wait(2000)
			loop = False

#Game Menu
menuLoop = True
while menuLoop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			menuLoop = False
	m_pos = pygame.mouse.get_pos()
	m_c = pygame.mouse.get_pressed()

	#if exit is click
	if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 360 and m_pos[1] < 450 and m_c == (1, 0, 0):
		menuLoop = False

	#if play is click
	if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 250 and m_pos[1] < 340 and m_c == (1, 0, 0):
		GameLoop()

	window.fill((0, 0, 0))

	#animation play
	if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 250 and m_pos[1] < 340:
		pygame.draw.rect(window, b, (350, 250, 200, 90))
		pygame.draw.rect(window, b, (360, 260, 180, 70))
		play = font.render('Play', True, n)
	else:
		pygame.draw.rect(window, b, (350, 250, 200, 90))
		pygame.draw.rect(window, n, (360, 260, 180, 70))
		play = font.render('Play', True, b)
	#animation exit
	if m_pos[0] > 350 and m_pos[0] < 550 and m_pos[1] > 360 and m_pos[1] < 450:
		pygame.draw.rect(window, b, (350, 360, 200, 90))
		pygame.draw.rect(window, b, (360, 370, 180, 70))
		exit = font.render('Exit', True, n)
	else:
		pygame.draw.rect(window, b, (350, 360, 200, 90))
		pygame.draw.rect(window, n, (360, 370, 180, 70))
		exit = font.render('Exit', True, b)

	window.blit(play, ((450 - int(play.get_width()/2)), 275))
	window.blit(exit, ((450 - int(play.get_width()/2)), 385))
	window.blit(titre, ((450 - int(titre.get_width()/2)), 50))
	pygame.display.update()
	time.sleep(0.01)