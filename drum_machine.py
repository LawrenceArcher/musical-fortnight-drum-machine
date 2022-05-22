# Build your own beat maker!
import pygame
from pygame import mixer
pygame.init()

WIDTH=1400
HEIGHT=800

black = (0,0,0)
white = (255,255,255)
grey = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)

fps = 60
timer = pygame.time.Clock()
beats=8
instruments = 6
boxes = []
# essentially full list of boxes clicked/not clicked = beats selected vs not
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)] # = list of 8 -1s in a row and 6 rows

def draw_grid(clicks):
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
			rect = pygame.draw.rect(screen, colour, [i * ((WIDTH-200)//beats) + 200, (j * 100) + 5, ((WIDTH - 200) // beats) - 10, ((HEIGHT-200)//instruments) - 10], 0, 3) # modifying slightly to sit inside below rect
			pygame.draw.rect(screen, gold, [i * ((WIDTH-200)//beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT-200)//instruments)], 5, 5) # outer rect
			pygame.draw.rect(screen, black, [i * ((WIDTH-200)//beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT-200)//instruments)], 2, 5) # outer rect line inside
			boxes.append((rect, (i, j)))
			
	return boxes



run = True
while run:
	timer.tick(fps) #essentially saying here that we will run code once every 1/60th of a second
	screen.fill(black)
	
	boxes = draw_grid(clicked)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			for i in range(len(boxes)):
				# essentially checking for the specific box we've clicked on + gathering mouse position at the time of click?
				if boxes[i][0].colliderect(event.pos): #Essential [0] here because we want to select the rect
					# tracking what has been actively clicked
					coords = boxes[i][1]
					# going to need a new list. Confusing way round here
					clicked[coords[1]][coords[0]] *= -1 # need to set to opposite of what it was whenever clicked
			
	pygame.display.flip()
pygame.quit()