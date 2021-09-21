import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption('Experimentation')
clock = pygame.time.Clock()
start_time = 0
screen_type = 'main_menu'
back_counter = 111
fps = 60
fps_presses = 0
volume = 5
vol_presses = 0
player_gravity = 0
front_speed = 0
back_speed = 0
checkpoint_room = 0

starting_structure = [[],[],[]]
for i in range(3):
    for j in range(16):
        starting_structure[i].append(0)
room_list = [starting_structure]

#Random Generation Function


def list_to_img(structure):
    counter_x = 0
    for x in structure:
        counter_y = 0
        for y in x:
            if y == 1:
                screen.blit(box_surf,(50*(counter_y)+100,50*(structure.index(x))+400))
            counter_y += 1
        counter_x += 1


def gen_random(structure):
    new_structure = [[],[],[]]
    counter = 0
    for x in structure:
        for y in x:
            random_num = randint(1,8)
            if random_num == 1:
                if y == 0:
                    new_structure[counter].append(1)
                else:
                    new_structure[counter].append(0)
            else:
                new_structure[counter].append(y)
        counter += 1
    return new_structure


#Colors
white = (255,255,255)
light_blue = (173,216,230)

#Font
crimson = pygame.font.Font('font/CrimsonText-Roman.ttf',48)
crimson_medium = pygame.font.Font('font/CrimsonText-Roman.ttf',26)

#Surfaces
main_menu = pygame.image.load('graphics/main_bg.jpg')
main_menu_rect = main_menu.get_rect(topleft=(0,0))
game_bg = pygame.image.load('graphics/game_bg1.jpg')
game_bg_rect = game_bg.get_rect(topleft=(0,0))
ground_bg = pygame.image.load('graphics/ground_bg.jpg')
ground_bg_rect = ground_bg.get_rect(topleft=(0,550))
title_text = crimson.render('Neverending',True,white)
title_text_rect = title_text.get_rect(center=(500,100))
play_button_surf = crimson_medium.render('Play',True,white)
play_button_rect = play_button_surf.get_rect(center=(500,200))
settings_button_surf = crimson_medium.render('Settings',True,white)
settings_button_rect = settings_button_surf.get_rect(center=(500,250))
quit_button_surf = crimson_medium.render('Quit',True,white)
quit_button_rect = quit_button_surf.get_rect(center=(500,300))
back_button_surf = crimson_medium.render('Back',True,white)
back_button_rect = back_button_surf.get_rect(bottomleft=(0,60))

player_surf = pygame.image.load('graphics/player/spirit_nobg.png')
player_rect = player_surf.get_rect(bottomleft=(0,550))

box_surf = pygame.image.load('graphics/enemies/box.jpg')
box_rect = box_surf.get_rect()
checkpoint_surf = crimson.render('Checkpoint Room',True,light_blue)
checkpoint_rect = checkpoint_surf.get_rect(center=(500,100))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 550:
                player_gravity = -20
            if event.key == pygame.K_a:
                back_speed = 4
            if event.key == pygame.K_d:
                front_speed = 4
            if event.key == pygame.K_BACKSLASH:
                print('Developer settings enabled.')
                front_speed = 10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a or event.key == pygame.K_BACKSLASH:
                front_speed = 0
                back_speed = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_type == 'main_menu':
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 0
                elif settings_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'settings'
                elif quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
            elif screen_type == 'settings':
                if fps_rect.collidepoint(pygame.mouse.get_pos()):
                    if fps_presses % 3 == 0:
                        fps = 144
                    elif fps_presses % 3 == 1:
                        fps = 30
                    else:
                        fps = 60
                    fps_presses += 1
                elif vol_rect.collidepoint(pygame.mouse.get_pos()):
                    volume = vol_presses % 6
                    vol_presses += 1
                elif back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'main_menu'
    if screen_type == 'main_menu':
        if main_menu_rect.x > -111 and back_counter % 111 == 0:
            main_menu_rect.x -= 1
        elif main_menu_rect.x < 0:
            main_menu_rect.x += 1
            back_counter += 1
        screen.blit(main_menu,main_menu_rect)
        screen.blit(title_text,title_text_rect)
        screen.blit(play_button_surf,play_button_rect)
        screen.blit(settings_button_surf,settings_button_rect)
        screen.blit(quit_button_surf,quit_button_rect)
    elif type(screen_type) == int:
        screen.blit(game_bg,game_bg_rect)
        screen.blit(ground_bg,ground_bg_rect)

        #Random Generation
        list_to_img(room_list[screen_type])
        if screen_type % 5 == 0:
            screen.blit(checkpoint_surf,checkpoint_rect)
        checkpoint_room = screen_type

        #Physics Engine
        player_gravity += 1
        player_rect.y += player_gravity
        player_rect.x += front_speed
        player_rect.x -= back_speed
        screen.blit(player_surf, player_rect)
        if player_rect.bottom >= 550:
            player_rect.bottom = 550
            player_gravity = 0

        #Exit Detection
        if player_rect.x > 1050:
            if len(room_list) == screen_type+1:
                if len(room_list) % 5 != 0:
                    room_list.append(gen_random(room_list[screen_type]))
                else:
                    room_list.append(starting_structure)
            screen_type += 1
            player_rect.x = 0
        elif player_rect.x < -50:
            if screen_type == 0:
                player_rect.x = -25
            else:
                screen_type -= 1
                player_rect.x = 950

    elif screen_type == 'settings':
        if main_menu_rect.x > -111 and back_counter % 111 == 0:
            main_menu_rect.x -= 1
        elif main_menu_rect.x < 0:
            main_menu_rect.x += 1
            back_counter += 1
        screen.blit(main_menu,main_menu_rect)
        screen.blit(title_text,title_text_rect)
        screen.blit(back_button_surf,back_button_rect)
        vol_surf = crimson_medium.render(f'Volume: {volume*20}',True,white)
        vol_rect = vol_surf.get_rect(center=(500,300))
        fps_surf = crimson_medium.render(f'FPS: {fps}',True,white)
        fps_rect = fps_surf.get_rect(center=(500,250))
        screen.blit(fps_surf,fps_rect)
        screen.blit(vol_surf,vol_rect)

    pygame.display.update()
    clock.tick(fps)