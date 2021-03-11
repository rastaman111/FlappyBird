import pygame, random, json
from math import sqrt

class Constants:
    size = [576, 1024]

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))

def creat_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        return False

    return True

def rotation_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return  new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High core: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (288, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        write_file()
    return high_score

def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

def read_file():
    with open("data_file.json", "r") as read_file:
        data = json.load(read_file)
        return data.get("BestResult")

def write_file():
    result = {'BestResult': score}
    with open("data_file.json", "w") as write_file:
        json.dump(result, write_file)

#Button
def textObjekt(text, font):
    textFlaeche = font.render(text, True, (255, 255, 255))
    return textFlaeche,textFlaeche.get_rect()

def distance(punkt1,punkt2):
    return sqrt(((punkt2[0]-punkt1[0])**2)+((punkt2[1]-punkt1[1])**2))

aktiv = False

def buttonRoundCorners(bx,by,laenge,hoehe,radius,farbe_normal,farbe_aktiv,nachricht):
    global eing,start,aktiv
    topRect = maus[0]>=bx+radius and maus[0]<=bx+laenge-radius and maus[1]>=by and maus[1]<=by+radius
    midRect = maus[0]>=bx and maus[0]<=bx+laenge and maus[1]>=by+radius and maus[1]<=by+hoehe-radius
    bottomRect = maus[0]>=bx+radius and maus[0]<=bx+laenge-radius and maus[1]>=by+hoehe-radius and maus[1]<=by+hoehe
    midTopleft = distance((bx+radius,by+radius),(maus[0],maus[1]))<=radius
    midBottomleft = distance((bx+radius,by+hoehe-radius),(maus[0],maus[1]))<=radius
    midTopright = distance((bx+laenge-radius,by+radius),(maus[0],maus[1]))<=radius
    midBottomRight = distance((bx+laenge-radius,by+hoehe-radius),(maus[0],maus[1]))<=radius

    #rand
    pygame.draw.lines(screen, (0,0,0), False, [(bx+radius,by-1),(bx+laenge-radius,by-1),(bx+radius,by+hoehe),(bx+laenge-radius,by+hoehe)], 1)
    pygame.draw.rect(screen, (0,0,0), (bx-1,by+radius,laenge+2,int(hoehe-(2*radius))))
    pygame.draw.circle(screen, (0,0,0), (bx+radius,by+radius), radius+1, 0)
    pygame.draw.circle(screen, (0,0,0), (bx+radius,by+hoehe-radius), radius+1, 0)
    pygame.draw.circle(screen, (0,0,0), (bx+laenge-radius,by+radius), radius+1, 0)
    pygame.draw.circle(screen, (0,0,0), (bx+laenge-radius,by+hoehe-radius), radius+1, 0)

    if topRect or midRect or bottomRect or midTopright or midTopleft or midBottomleft or midBottomRight:
        pygame.draw.rect(screen, farbe_aktiv, (bx+radius,by,int(laenge-(2*radius)),radius))
        pygame.draw.rect(screen, farbe_aktiv, (bx,by+radius,laenge,int(hoehe-(2*radius))))
        pygame.draw.rect(screen, farbe_aktiv, (bx+radius,by+hoehe-radius,int(laenge-(2*radius)),radius))
        pygame.draw.circle(screen, farbe_aktiv, (bx+radius,by+radius), radius, 0)
        pygame.draw.circle(screen, farbe_aktiv, (bx+radius,by+hoehe-radius), radius, 0)
        pygame.draw.circle(screen, farbe_aktiv, (bx+laenge-radius,by+radius), radius, 0)
        pygame.draw.circle(screen, farbe_aktiv, (bx+laenge-radius,by+hoehe-radius), radius, 0)
        if aktiv == False:
            if klick[0] == 1 and aktiv == False:
                aktiv = True
                #Action
                if nachricht == "Start":
                    print("Hallo Welt")
        if klick[0] == 0:
            aktiv = False
    else:
        pygame.draw.rect(screen, farbe_normal, (bx+radius,by,int(laenge-(2*radius)),radius))
        pygame.draw.rect(screen, farbe_normal, (bx,by+radius,laenge,int(hoehe-(2*radius))))
        pygame.draw.rect(screen, farbe_normal, (bx+radius,by+hoehe-radius,int(laenge-(2*radius)),radius))
        pygame.draw.circle(screen, farbe_normal, (bx+radius,by+radius), radius, 0)
        pygame.draw.circle(screen, farbe_normal, (bx+radius,by+hoehe-radius), radius, 0)
        pygame.draw.circle(screen, farbe_normal, (bx+laenge-radius,by+radius), radius, 0)
        pygame.draw.circle(screen, farbe_normal, (bx+laenge-radius,by+hoehe-radius), radius, 0)

    textGrund, textKasten = textObjekt(nachricht, game_font)
    textKasten.center = ((bx+(laenge/2)),(by+(hoehe/2)))
    screen.blit(textGrund, textKasten)

#Game
pygame.init()

screen = pygame.display.set_mode(Constants.size)
programIcon = pygame.image.load("assets/favicon.ico").convert_alpha()
pygame.display.set_icon(programIcon)
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf", 40)

#FPS
font = pygame.font.SysFont("Arial", 18)
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text

#Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
bg_surface = pygame.transform.scale2x(pygame.image.load("assets/background-day.png").convert())

floor_surface = pygame.transform.scale2x(pygame.image.load("assets/base.png").convert())
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.transform.scale2x(pygame.image.load("assets/pipe-green.png"))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288, 512))

flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(creat_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    high_score = read_file()

    #FPS
    screen.blit(update_fps(), (10,0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotation_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

        maus = pygame.mouse.get_pos()
        klick = pygame.mouse.get_pressed()
        buttonRoundCorners(240,10,200,60,10,(255,0,70),(255,0,180),"Start")

    # Floor
    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)

pygame.quit()