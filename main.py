import pygame
from pygame import mixer
pygame.init()

# global constants
WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
dark_gray = (50, 50, 50)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Drum kit')
big_font = pygame.font.Font('fonts/Oswald-Heavy.ttf', 64)
label_font = pygame.font.Font('fonts/Oswald-Bold.ttf', 32)
medium_font = pygame.font.Font('fonts/Oswald-Medium.ttf', 24)

fps = 60
clock = pygame.time.Clock()
beats = 8
bpm = 240
instruments = 6
playing = True
active_length = 0
active_beat = 0
beat_changed = True
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_instruments = [1 for _ in range(instruments)]

# sounds
hi_hat = mixer.Sound('sounds/HiHat 002 - Matty.wav')
snare = mixer.Sound('sounds/Snare 009 - Modern.wav')
kick = mixer.Sound('sounds/Kick 016 - Discontinued.wav')
crash = mixer.Sound('sounds/Crash 001 - Oddity.wav')
triangle = mixer.Sound('sounds/Triangle 001 - Robo.wav')
floor_tom = mixer.Sound('sounds/tom (1).WAV')
pygame.mixer.set_num_channels(instruments * 3)

# functions
def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_instruments[i] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                triangle.play()
            if i == 5:
                floor_tom.play()

def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))
    triangle_text = label_font.render('Triangle', True, colors[actives[4]])
    screen.blit(triangle_text, (30, 430))
    floor_tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
    screen.blit(floor_tom_text, (30, 530))
    for i in range(instruments - 1):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (195, (i * 100) + 100), 5)
        
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, 
                                                  (j * 100) + 5, ((WIDTH - 200) // beats) - 10, 
                                                  ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, 
                                                  (j * 100), ((WIDTH - 200) // beats), 
                                                  ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, 
                                                  (j * 100), ((WIDTH - 200) // beats), 
                                                  ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))
        
        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return boxes


# main game loop
run = True
while run:
    clock.tick(fps)
    screen.fill(black)    
    boxes = draw_grid(clicked, active_beat, active_instruments)
    # lower menu
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_pause_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_pause_text, (70, HEIGHT - 130))
    if playing:
        play_pause_text2 = medium_font.render('Playing', True, blue)
    else:
        play_pause_text2 = medium_font.render('Paused', True, blue)
    screen.blit(play_pause_text2, (70, HEIGHT - 90))
    # bpm settings
    bpm_box = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats per minute', True, white)
    screen.blit(bpm_text, (320, HEIGHT - 142))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (376, HEIGHT - 107))
    bpm_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    add_text = big_font.render('+', True, white)
    sub_text = big_font.render('-', True, white)
    screen.blit(add_text, (519, HEIGHT - 169))
    screen.blit(sub_text, (521, HEIGHT - 121))
    # beats settings
    beats_box = pygame.draw.rect(screen, gray, [580, HEIGHT - 150, 200, 100], 5, 5)
    beats_text = medium_font.render('Beats in loop', True, white)
    screen.blit(beats_text, (620, HEIGHT - 142))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (668, HEIGHT - 107))
    beats_add_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [810, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = big_font.render('+', True, white)
    sub_text2 = big_font.render('-', True, white)
    screen.blit(add_text2, (819, HEIGHT - 169))
    screen.blit(sub_text2, (821, HEIGHT - 121))
    #instrument settings
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    
    if beat_changed:
        play_notes()
        beat_changed = False
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos) and bpm < 500:
                bpm += 10
            elif bpm_sub_rect.collidepoint(event.pos) and bpm > 10:
                bpm -= 10
            elif beats_add_rect.collidepoint(event.pos) and beats < 80:
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos) and beats > 1:
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_instruments[i] *= -1
    
    beat_length = (fps * 60) // bpm 
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
