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
playing = False
active_length = 0
active_beat = 0
beat_changed = True
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_instruments = [1 for _ in range(instruments)]
save_menu = False
load_menu = False
savelist = []
save_file = open('savelist.txt', 'r')
for line in save_file:
    savelist.append(line)
beat_name = ''
typing = False

# sounds
hi_hat = mixer.Sound('sounds/HiHat 002 - Matty.wav')
snare = mixer.Sound('sounds/Snare 009 - Modern.wav')
kick = mixer.Sound('sounds/Kick 016 - Discontinued.wav')
crash = mixer.Sound('sounds/Crash 001 - Oddity.wav')
donk = mixer.Sound('sounds/Perc 002 - Solomon.wav')
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
                donk.play()
            if i == 5:
                floor_tom.play()

def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 195], 5)
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
    donk_text = label_font.render('Donk', True, colors[actives[4]])
    screen.blit(donk_text, (30, 430))
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
                                                  ((HEIGHT - 200) // instruments) - 10], 0)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, 
                                                  (j * 100), ((WIDTH - 200) // beats), 
                                                  ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, 
                                                  (j * 100), ((WIDTH - 200) // beats), 
                                                  ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))
        
        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return boxes

def draw_save_menu(name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = big_font.render('SAVE MENU: Enter a name for save', True, white)
    screen.blit(menu_text, (285, 40))
    saving_box = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.75 - 5, 400, 100], 0, 5)
    saving_text = big_font.render('Save', True, white)
    screen.blit(saving_text, (WIDTH // 2 - 70, HEIGHT * 0.75))
    exit = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 155, HEIGHT - 75))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_box = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit, saving_box, entry_box

def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 155, HEIGHT - 75))
    return exit

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
    beats_add_rect = pygame.draw.rect(screen, gray, [790, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [790, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = big_font.render('+', True, white)
    sub_text2 = big_font.render('-', True, white)
    screen.blit(add_text2, (799, HEIGHT - 169))
    screen.blit(sub_text2, (801, HEIGHT - 121))
    #instrument settings
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    # save and load
    save_box = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 200, 48], 0, 5)
    load_box = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 200, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, white)
    load_text = label_font.render('Load Beat', True, white)
    screen.blit(save_text, (933, HEIGHT - 148))
    screen.blit(load_text, (933, HEIGHT - 98))
    # clear board
    clear_box = pygame.draw.rect(screen, gray, [1150, HEIGHT - 150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear Board', True, white)
    screen.blit(clear_text, (1170, HEIGHT - 120))

    if save_menu:
        exit_box, saving_box, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_box = draw_load_menu()
    if beat_changed:
        play_notes()
        beat_changed = False
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
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
            elif clear_box.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_box.collidepoint(event.pos):
                save_menu = True
                playing = False
            elif load_box.collidepoint(event.pos):
                load_menu = True
                playing = False
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_instruments[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_box.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = False
                beat_name = ''
                typing = False
            elif entry_rectangle.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            elif saving_box.collidepoint(event.pos):
                file = open('savelist.txt', 'w')
                savelist.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                for i in range(len(savelist)):
                    file.write(str(savelist[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
                playing = False

        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

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
