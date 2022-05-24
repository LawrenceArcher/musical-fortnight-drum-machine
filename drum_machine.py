# Build your own beat maker!
import pygame
from pygame import mixer
pygame.init()

WIDTH=1400
HEIGHT=800

black = (0,0,0)
white = (255,255,255)
grey = (128, 128, 128)
dark_grey = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)


screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats=8
instruments = 6
boxes = []
# essentially full list of boxes clicked/not clicked = beats selected vs not
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] # = list of 8 -1s in a row and 6 rows
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

# load in sounds
hi_hat = mixer.Sound('sounds/hi hat.WAV')
snare = mixer.Sound('sounds/snare.WAV')
kick = mixer.Sound('sounds/kick.WAV')
crash = mixer.Sound('sounds/crash.WAV')
clap = mixer.Sound('sounds/clap.WAV')
tom = mixer.Sound('sounds/tom.WAV')
pygame.mixer.set_num_channels(instruments * 3) # by default for the pygame mixer only have 8 channels - i.e. 8 simultaneous sounds. Could run out of sounds then pygame picks the right sounds. 3*per channel should work as long as we don't have a really fast tempo
#

def play_notes():
	for i in range(len(clicked)):
		if clicked[i][active_beat] == 1:
			if i == 0:
				hi_hat.play()
			if i == 1:
				snare.play()
			if i == 2:
				kick.play()
			if i == 3:
				crash.play()
			if i == 4:
				clap.play()
			if i == 5:
				tom.play()

def draw_grid(clicks, beat):
	left_box = pygame.draw.rect(screen, grey, [0, 0, 200, HEIGHT- 200], 5)
	bottom_box = pygame.draw.rect(screen, grey, [0, HEIGHT-200, WIDTH, 200], 5)
	boxes = []
	colours = [grey, white, grey]
	hi_hat_text = label_font.render('Hi Hat', True, white)
	screen.blit(hi_hat_text, (30,30))
	snare_text = label_font.render('Snare', True, white)
	screen.blit(snare_text, (30,130))
	kick_text = label_font.render('Kick', True, white)
	screen.blit(kick_text, (30,230))
	crash_text = label_font.render('Crash', True, white)
	screen.blit(crash_text, (30,330))
	clap_text = label_font.render('Clap', True, white)
	screen.blit(clap_text, (30,430))
	floor_text = label_font.render('Floor Tom', True, white)
	screen.blit(floor_text, (30,530))
	for i in range(instruments):
		pygame.draw.line(screen, grey, (0, (i+1)*100), (200, (i+1)*100), 3)
		
	for i in range(beats):
		for j in range(instruments):
			if clicks[j][i] == -1:
				colour = grey
			else:
				colour = green	
			rect = pygame.draw.rect(screen, colour, [i * ((WIDTH-200)//beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10, ((HEIGHT-200)//instruments) - 10], 0, 3) # modifying slightly to sit inside below rect
			pygame.draw.rect(screen, gold, [i * ((WIDTH-200)//beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT-200)//instruments)], 5, 5) # outer rect
			pygame.draw.rect(screen, black, [i * ((WIDTH-200)//beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT-200)//instruments)], 2, 5) # outer rect line inside
			boxes.append((rect, (i, j)))
			
		active = pygame.draw.rect(screen, blue, [beat*((WIDTH-200)//beats) + 200, 0, ((WIDTH-200)//beats), instruments * 100], 5, 3)
			
	return boxes



run = True
while run:
	timer.tick(fps) #essentially saying here that we will run code once every 1/60th of a second
	screen.fill(black)
	
	boxes = draw_grid(clicked, active_beat)
	# lower menu buttons
	play_pause = pygame.draw.rect(screen, grey, [50, HEIGHT-150, 200, 100], 0, 5)
	
	# pause/play text
	if playing:
		play_text = label_font.render('Pause', True, white)
	else:
		play_text = label_font.render('Play', True, white)
	screen.blit(play_text, (100, HEIGHT - 115))
	
	# bpm stuff
	bpm_rect = pygame.draw.rect(screen, grey, [300, HEIGHT - 150, 200, 100], 5, 5)
	bpm_text = medium_font.render('Beats Per Minute', True, white)
	screen.blit(bpm_text, (308, HEIGHT - 130))
	bpm_text2 = label_font.render(f'{bpm}', True, white)
	screen.blit(bpm_text2, (370, HEIGHT - 100))
	bpm_add_rect = pygame.draw.rect(screen, grey, [510, HEIGHT-150, 48, 48], 0 , 5)
	bpm_asub_rect = pygame.draw.rect(screen, grey, [510, HEIGHT-100, 48, 48], 0 , 5)
	add_text = medium_font.render('+5', True, white)
	sub_text = medium_font.render('-5', True, white)
	screen.blit(add_text, (520, HEIGHT - 140))
	screen.blit(sub_text, (520, HEIGHT - 90))
	
	if beat_changed:
		play_notes()
		beat_changed = False
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i in range(len(boxes)):
				# essentially checking for the specific box we've clicked on + gathering mouse position at the time of click?
				if boxes[i][0].collidepoint(event.pos): #Essential [0] here because we want to select the rect
					# tracking what has been actively clicked
					coords = boxes[i][1]
					# going to need a new list. Confusing way round here
					clicked[coords[1]][coords[0]] *= -1 # need to set to opposite of what it was whenever clicked
		
		if event.type == pygame.MOUSEBUTTONUP:
			if play_pause.collidepoint(event.pos):
				if playing:
					playing = False
				elif not playing:
					playing = True
					
	beat_length = 3600//bpm
	
	if playing:
		if active_length < beat_length:
			active_length += 1
		else:
			active_length = 0
			if active_beat < beats - 1:
				active_beat += 1
				beat_changed = True
			else:
				active_beat = 0
				beat_changed = True
			
	pygame.display.flip()
pygame.quit()