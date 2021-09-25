import pygame
from sys import exit
from random import randint
import math

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('Neverending')
clock = pygame.time.Clock()
start_time = 0
screen_type = 'main_menu'
back_counter = 111
diff_presses = 2
difficulty = 'Normal'
volume = 5
vol_presses = 0
player_gravity = 0
player_speed = 0
isjump = False
checkpoint_room = 0
max_room = 0
v = 5
m = 1
dev_tools = False
dead = False
bg_music = pygame.mixer.Sound('audio/Voyage.ogg')

# Lives System
hp = 300
max_hp = 300
invincibility = 0

# Shop Variables
lv_5_upgrade = False
lv_10_upgrade = False
lv_15_upgrade = False
lv_20_upgrade = False
lv_25_upgrade = False

# Speed
add_speed = 0

starting_structure = [[], [], []]
for i in range(3):
    for j in range(16):
        starting_structure[i].append(0)

# tutorial_structure = starting_structure.copy()
# for i in range(3):
#     tutorial_structure[i].pop(-1)
#     tutorial_structure[i].insert(-1, 1)
room_list = [starting_structure]


# Random Generation Function
def follow_mouse(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    self.image = pygame.transform.rotate(self.original_image, int(angle))
    self.rect = self.image.get_rect(center=self.position)


def list_to_img(structure):
    counter_x = 0
    for x in structure:
        counter_y = 0
        for y in x:
            if y == 1:
                screen.blit(box_surf, (50 * counter_y + 100, 50 * (structure.index(x)) + 400))
            counter_y += 1
        counter_x += 1


def gen_random(structure):
    new_structure = [[], [], []]
    counter = 0
    for x in structure:
        for y in x:
            random_num = randint(1, 8)
            if random_num == 1:
                if y == 0:
                    new_structure[counter].append(1)
                else:
                    new_structure[counter].append(0)
            else:
                new_structure[counter].append(y)
        counter += 1
    return new_structure


def display_hp(enemies_killed):
    global current_room_number
    score_surface = crimson_medium.render(f'Health: {hp}',True,white)
    score_rectangle = score_surface.get_rect(topleft=(0,0))
    screen.blit(score_surface,score_rectangle)
    score1_surface = crimson_medium.render('Enemies Killed: '+str(enemies_killed),True,white)
    score1_rectangle = score1_surface.get_rect(topleft=(150,0))
    room_number_surf = crimson_medium.render(f'Room {current_room_number}', True, light_blue)
    room_number_rect = room_number_surf.get_rect(center=(500, 150))
    screen.blit(room_number_surf, room_number_rect)
    screen.blit(score1_surface,score1_rectangle)


def check_if_collision(room_list, player_rect, room_number):
    for y in range(len(room_list[room_number])):
        for x in range(len(room_list[room_number][y])):
            if room_list[room_number][y][x]:
                obstacle = pygame.Rect(x * 50 + 100, y * 50 + 400, 50, 50)
                if obstacle.colliderect(player_rect):
                    return True
    return False


def check_if_collision_bullet(room_list,room_number,red_bullets):
    for y in range(len(room_list[room_number])):
        for x in range(len(room_list[room_number][y])):
            if room_list[room_number][y][x]:
                obstacle = pygame.Rect(x*50+100,y*50+400,50,50)
                for bullet in red_bullets:
                    if obstacle.colliderect(bullet[0]):
                         red_bullets.remove(bullet)


def check_if_collision_bullet_enemy(enemy_rect,red_bullets,spawn_timer):
    for bullet in red_bullets:
        if enemy_rect.colliderect(bullet[0]):
            red_bullets.remove(bullet)
            spawn_timer=True
            return True


def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect


def handle_bullets(red_bullets):
    for bullet in red_bullets:
        angle = bullet[1]
        bullet[0].y+=int(math.sin(angle)*bullet_velocity)
        bullet[0].x+=int(math.cos(angle)*bullet_velocity)
        if bullet[0].x>1000 or bullet[0].x<0 or bullet[0].y>600 or bullet[0].y<0:
            red_bullets.remove(bullet)


# Enemy


def move_towards_player(enemy, player, diff):
    dx, dy = player.x - enemy.x, player.y - enemy.y
    dist = math.hypot(dx, dy)
    if dist <= 40:
        return True
    dx, dy = dx / dist, dy / dist
    if diff == 'Easy':
        fly_speed = 3
    elif diff == 'Normal':
        fly_speed = 3.5
    elif diff == 'Hard':
        fly_speed = 4
    enemy.x += dx * fly_speed
    enemy.y += dy * fly_speed


# Colors
white = (255, 255, 255)
light_blue = (173, 216, 230)

# Font
crimson = pygame.font.Font('font/CrimsonText-Roman.ttf', 48)
crimson_medium = pygame.font.Font('font/CrimsonText-Roman.ttf', 26)

# Surfaces
current_room_number = 0
max_bullets=100
bullet_velocity=7
main_menu = pygame.image.load('graphics/main_bg.jpg')
main_menu_rect = main_menu.get_rect(topleft=(0, 0))
game_bg = pygame.image.load('graphics/game_bg1.jpg')
game_bg_rect = game_bg.get_rect(topleft=(0, 0))
ground_bg = pygame.image.load('graphics/ground_bg.jpg')
ground_bg_rect = ground_bg.get_rect(topleft=(0, 550))
title_text = crimson.render('Neverending', True, white)
title_text_rect = title_text.get_rect(center=(500, 100))
shop_title_text = crimson.render('Shop', True, white)
shop_title_text_rect = shop_title_text.get_rect(center=(500, 100))
play_button_surf = crimson_medium.render('Play', True, white)
play_button_rect = play_button_surf.get_rect(center=(500, 200))
settings_button_surf = crimson_medium.render('Settings', True, white)
settings_button_rect = settings_button_surf.get_rect(center=(500, 250))
back_button_surf = crimson_medium.render('Back', True, white)
back_button_rect = back_button_surf.get_rect(bottomleft=(0, 60))
shop_button_surf = crimson_medium.render('Shop', True, white)
shop_button_rect = shop_button_surf.get_rect(center=(500, 300))
tutorial_button_surf = crimson_medium.render('Tutorial', True, white)
tutorial_button_rect = tutorial_button_surf.get_rect(center=(500,350))
quit_button_surf = crimson_medium.render('Quit', True, white)
quit_button_rect = quit_button_surf.get_rect(center=(500, 400))

tutorial_txt1 = crimson_medium.render('Welcome to Purgatory. Move with the left and right arrows.',True,white)
tutorial_txt1_rect = tutorial_txt1.get_rect(center=(500,200))
tutorial_txt2 = crimson_medium.render('Press space to jump.',True,white)
tutorial_txt2_rect = tutorial_txt1.get_rect(center=(500,250))
tutorial_txt3 = crimson_medium.render('Wall-hold with the arrows when you are next to a wall.',True,white)
tutorial_txt3_rect = tutorial_txt1.get_rect(center=(500,300))
tutorial_txt4 = crimson_medium.render('As you progress and reach checkpoint rooms, shop upgrades unlock.',True,white)
tutorial_txt4_rect = tutorial_txt1.get_rect(center=(500,350))
tutorial_txt5 = crimson_medium.render('Mind your health. Strange spirits lurk here...',True,white)
tutorial_txt5_rect = tutorial_txt1.get_rect(center=(500,400))

player_surf = pygame.image.load('graphics/player/player.png')
player_rect = player_surf.get_rect(bottomleft=(0, 550))
enemy_surf = pygame.image.load('graphics/enemies/melee_enemy.png')
enemy_center = (randint(0, 1000), 200)
enemy_rect = enemy_surf.get_rect(center=enemy_center)

gun_surf = pygame.image.load('graphics/player/ship_nobg.png')
gun_rect = gun_surf.get_rect(bottomleft=(0, 550))
gun_surf = pygame.transform.scale(gun_surf, (50, 10))

box_surf = pygame.image.load('graphics/enemies/box.jpg')
box_rect = box_surf.get_rect()
checkpoint_surf = crimson.render('Checkpoint Room', True, light_blue)
checkpoint_rect = checkpoint_surf.get_rect(center=(500, 100))
red_bullets = []

pygame.display.set_icon(enemy_surf)
now_move = False
spawn_timer = True
enemies_killed = 0

while True:
    # if isjump == False:
    #     if keys_pressed[pygame.K_SPACE] and player_rect.bottom>=550:
    #         isjump=True
    # if isjump:
    #     f = (1/2)*m*(v**2)
    #     player_rect.y -= f
    #     v = v-1
    #     if v<0:
    #         m =- 1
    #     if v == -6:
    #         isjump = False
    #         v = 5
    #         m = 1
    # print(isjump,player_rect.bottom)
    gun_rect.x = player_rect.x
    gun_rect.y = player_rect.y
    gun_rect.width = 30
    gun_rect.height = 20
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y=mouse_x-player_rect.x,mouse_y-player_rect.y
    angle=(180/math.pi)*-math.atan2(rel_y,rel_x)
    angle1=(math.atan2(rel_y,rel_x))
    z,n=rot_center(gun_surf,angle,player_rect.x+player_rect.width/2,player_rect.y+player_rect.height/2)
    if spawn_timer==True and type(screen_type) == int:
        enemy_surf = pygame.image.load('graphics/enemies/melee_enemy.png')
        enemy_center = (randint(0, 1000), -100)
        enemy_rect = enemy_surf.get_rect(center=enemy_center)
        spawn_timer=False
    for event in pygame.event.get():
        keys_pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if keys_pressed[pygame.K_SPACE]:
                now_move = True
                if player_rect.bottom == 550 or player_rect.bottom == 501 or player_rect.bottom == 451 \
                        or player_rect.bottom == 401:
                    player_gravity = -20
            if keys_pressed[pygame.K_LEFT]:
                player_speed = -4 - add_speed
            if keys_pressed[pygame.K_RIGHT]:
                player_speed = 4 + add_speed
            if keys_pressed[pygame.K_BACKSLASH]:
                print('Developer tools enabled.')
                dev_tools = True
            if keys_pressed[pygame.K_SLASH]:
                print('Developer tools disabled.')
                dev_tools = False
            if keys_pressed[pygame.K_RIGHTBRACKET] and dev_tools:
                player_speed = 12
            if keys_pressed[pygame.K_LEFTBRACKET] and dev_tools:
                player_speed = -12
            if keys_pressed[pygame.K_s] and dev_tools:
                max_room = 25
                print('All shop upgrades unlocked.')
            if keys_pressed[pygame.K_d] and dev_tools:
                dead = True
                print('Killed player.')
            if event.key==pygame.K_e and len(red_bullets)<max_bullets:
                bullet=[pygame.Rect(player_rect.x+player_rect.width/2,player_rect.y+player_rect.height/2,10,5), angle1]
                red_bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHTBRACKET \
                    or event.key == pygame.K_LEFTBRACKET:
                player_speed = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen_type == 'main_menu':
                if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 0
                elif settings_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'settings'
                elif shop_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'shop'
                elif tutorial_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'tutorial'
                elif quit_button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
            elif screen_type == 'settings':
                if diff_rect.collidepoint(pygame.mouse.get_pos()):
                    if diff_presses % 3 == 0:
                        difficulty = 'Hard'
                    elif diff_presses % 3 == 1:
                        difficulty = 'Easy'
                    else:
                        difficulty = 'Normal'
                    diff_presses += 1
                elif vol_rect.collidepoint(pygame.mouse.get_pos()):
                    volume = vol_presses % 6
                    vol_presses += 1
                elif back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'main_menu'
            elif screen_type == 'shop':
                if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'main_menu'
            elif type(screen_type) == int:
                if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'main_menu'
                    bg_music.stop()
            elif screen_type == 'tutorial':
                if back_button_rect.collidepoint(pygame.mouse.get_pos()):
                    screen_type = 'main_menu'
    if screen_type == 'main_menu':
        if main_menu_rect.x > -111 and back_counter % 111 == 0:
            main_menu_rect.x -= 1
        elif main_menu_rect.x < 0:
            main_menu_rect.x += 1
            back_counter += 1
        screen.blit(main_menu, main_menu_rect)
        screen.blit(title_text, title_text_rect)
        screen.blit(play_button_surf, play_button_rect)
        screen.blit(settings_button_surf, settings_button_rect)
        screen.blit(shop_button_surf, shop_button_rect)
        screen.blit(tutorial_button_surf,tutorial_button_rect)
        screen.blit(quit_button_surf, quit_button_rect)
    elif screen_type == 'tutorial':
        # list_to_img(tutorial_structure)
        screen.blit(game_bg, game_bg_rect)
        screen.blit(ground_bg, ground_bg_rect)
        screen.blit(tutorial_txt1, tutorial_txt1_rect)
        screen.blit(tutorial_txt2, tutorial_txt2_rect)
        screen.blit(tutorial_txt3, tutorial_txt3_rect)
        screen.blit(tutorial_txt4, tutorial_txt4_rect)
        screen.blit(tutorial_txt5, tutorial_txt5_rect)
        display_hp()

        # Movement
        player_next_step = pygame.Rect(player_rect.x + player_speed, player_rect.y + player_gravity, player_rect.width,
                                       player_rect.height)
        collision = check_if_collision(room_list, player_next_step, current_room_number)

        # Collision Detection
        if not collision:
            player_gravity += 1
            player_rect.y += player_gravity
            player_rect.x += player_speed
            screen.blit(player_surf, player_rect)
            screen.blit(z, n)
            if player_rect.bottom >= 550:
                player_rect.bottom = 550
                player_gravity = 0
        else:
            player_gravity = -1
            screen.blit(player_surf, player_rect)
            screen.blit(z, n)

        # Room
        if player_rect.x > 1050:
            player_rect.x = 975
        elif player_rect.x < -50:
            player_rect.x = -25

        screen.blit(back_button_surf, back_button_rect)
    elif type(screen_type) == int:
        bg_music.set_volume(volume/5)
        bg_music.play(-1)
        if dead:
            screen_type = checkpoint_room
            dead = False
            current_room_number = checkpoint_room
        screen.blit(game_bg, game_bg_rect)
        screen.blit(ground_bg, ground_bg_rect)

        # Random Generation
        list_to_img(room_list[screen_type])
        if screen_type % 5 == 0:
            screen.blit(checkpoint_surf, checkpoint_rect)
            checkpoint_room = screen_type

        # Physics Engine
        player_next_step = pygame.Rect(player_rect.x + player_speed, player_rect.y + player_gravity, player_rect.width,
                                       player_rect.height)
        collision = check_if_collision(room_list, player_next_step, current_room_number)

        # Collision Detection
        if not collision:
            player_gravity += 1
            player_rect.y += player_gravity
            player_rect.x += player_speed
            screen.blit(player_surf, player_rect)
            screen.blit(z, n)
            if player_rect.bottom >= 550:
                player_rect.bottom = 550
                player_gravity = 0
        else:
            player_gravity = -1
            screen.blit(player_surf, player_rect)
            screen.blit(z, n)
        # Exit Detection
        if player_rect.x > 1050:
            if len(room_list) == screen_type + 1:
                max_room += 1
                if len(room_list) % 5 != 0:
                    room_list.append(gen_random(room_list[screen_type]))
                else:
                    room_list.append(starting_structure)
            screen_type += 1
            player_rect.x = 0
            current_room_number+=1
        elif player_rect.x < -50:
            if screen_type == 0:
                player_rect.x = -25
            else:
                current_room_number -= 1
                screen_type -= 1
                player_rect.x = 950
        screen.blit(back_button_surf, back_button_rect)

        #Enemy Collision & Damage

        invincibility -= 1
        if move_towards_player(enemy_rect, player_rect, difficulty) and invincibility <= 0:
            hp -= 10
            spawn_timer=True
        if check_if_collision_bullet_enemy(enemy_rect,red_bullets,spawn_timer):
            spawn_timer=True
            enemies_killed+=1
            
        screen.blit(enemy_surf, enemy_rect)
        if hp <= 0:
            dead = True
            enemy_center = (1000,-100)
            hp = max_hp
            invincibility = 120

        display_hp(enemies_killed)

    elif screen_type == 'settings':
        if main_menu_rect.x > -111 and back_counter % 111 == 0:
            main_menu_rect.x -= 1
        elif main_menu_rect.x < 0:
            main_menu_rect.x += 1
            back_counter += 1
        screen.blit(main_menu, main_menu_rect)
        screen.blit(title_text, title_text_rect)
        screen.blit(back_button_surf, back_button_rect)
        vol_surf = crimson_medium.render(f'Volume: {volume * 20}', True, white)
        vol_rect = vol_surf.get_rect(center=(500, 300))
        diff_surf = crimson_medium.render(f'Difficulty: {difficulty}', True, white)
        diff_rect = diff_surf.get_rect(center=(500, 250))
        screen.blit(diff_surf, diff_rect)
        screen.blit(vol_surf, vol_rect)
    elif screen_type == 'shop':
        if main_menu_rect.x > -111 and back_counter % 111 == 0:
            main_menu_rect.x -= 1
        elif main_menu_rect.x < 0:
            main_menu_rect.x += 1
            back_counter += 1
        screen.blit(main_menu, main_menu_rect)
        screen.blit(shop_title_text, shop_title_text_rect)
        screen.blit(back_button_surf, back_button_rect)

        if max_room >= 25:
            if not lv_25_upgrade:
                lv_25_surf = crimson_medium.render('Increase Lives III', True, light_blue)
                lv_25_rect = lv_25_surf.get_rect(center=(500, 400))
                screen.blit(lv_25_surf, lv_25_rect)
                if lv_25_rect.collidepoint(pygame.mouse.get_pos()):
                    lv_25_upgrade = True
                    max_hp += 100
            else:
                lv_25_surf = crimson_medium.render('Increase Lives III (Claimed)', True, light_blue)
                lv_25_rect = lv_25_surf.get_rect(center=(500, 400))
                screen.blit(lv_25_surf, lv_25_rect)
        else:
            lv_25_surf = crimson_medium.render('Locked: Reach 25 Rooms', True, light_blue)
            lv_25_rect = lv_25_surf.get_rect(center=(500, 400))
            screen.blit(lv_25_surf, lv_25_rect)
        if max_room >= 20:
            if not lv_20_upgrade:
                lv_20_surf = crimson_medium.render('Increase Speed II', True, light_blue)
                lv_20_rect = lv_20_surf.get_rect(center=(500, 350))
                screen.blit(lv_20_surf, lv_20_rect)
                if lv_20_rect.collidepoint(pygame.mouse.get_pos()):
                    lv_20_upgrade = True
                    add_speed += 1
            else:
                lv_20_surf = crimson_medium.render('Increase Speed II (Claimed)', True, light_blue)
                lv_20_rect = lv_20_surf.get_rect(center=(500, 350))
                screen.blit(lv_20_surf, lv_20_rect)
        else:
            lv_20_surf = crimson_medium.render('Locked: Reach 20 Rooms', True, light_blue)
            lv_20_rect = lv_20_surf.get_rect(center=(500, 350))
            screen.blit(lv_20_surf, lv_20_rect)
        if max_room >= 15:
            if not lv_15_upgrade:
                lv_15_surf = crimson_medium.render('Increase Lives II', True, light_blue)
                lv_15_rect = lv_15_surf.get_rect(center=(500, 300))
                screen.blit(lv_15_surf, lv_15_rect)
                if lv_15_rect.collidepoint(pygame.mouse.get_pos()):
                    lv_15_upgrade = True
                    max_hp += 100
            else:
                lv_15_surf = crimson_medium.render('Increase Lives II (Claimed)', True, light_blue)
                lv_15_rect = lv_15_surf.get_rect(center=(500, 300))
                screen.blit(lv_15_surf, lv_15_rect)
        else:
            lv_15_surf = crimson_medium.render('Locked: Reach 15 Rooms', True, light_blue)
            lv_15_rect = lv_15_surf.get_rect(center=(500, 300))
            screen.blit(lv_15_surf, lv_15_rect)
        if max_room >= 10:
            if not lv_10_upgrade:
                lv_10_surf = crimson_medium.render('Increase Speed', True, light_blue)
                lv_10_rect = lv_10_surf.get_rect(center=(500, 250))
                screen.blit(lv_10_surf, lv_10_rect)
                if lv_10_rect.collidepoint(pygame.mouse.get_pos()):
                    lv_10_upgrade = True
                    add_speed += 1
            else:
                lv_10_surf = crimson_medium.render('Increase Speed (Claimed)', True, light_blue)
                lv_10_rect = lv_10_surf.get_rect(center=(500, 250))
                screen.blit(lv_10_surf, lv_10_rect)
        else:
            lv_10_surf = crimson_medium.render('Locked: Reach 10 Rooms', True, light_blue)
            lv_10_rect = lv_10_surf.get_rect(center=(500, 250))
            screen.blit(lv_10_surf, lv_10_rect)
        if max_room >= 5:
            if not lv_5_upgrade:
                lv_5_surf = crimson_medium.render('Increase Lives', True, light_blue)
                lv_5_rect = lv_5_surf.get_rect(center=(500, 200))
                screen.blit(lv_5_surf, lv_5_rect)
                if lv_5_rect.collidepoint(pygame.mouse.get_pos()):
                    lv_5_upgrade = True
                    max_hp += 100
            else:
                lv_5_surf = crimson_medium.render('Increase Lives (Claimed)', True, light_blue)
                lv_5_rect = lv_5_surf.get_rect(center=(500, 200))
                screen.blit(lv_5_surf, lv_5_rect)
        else:
            lv_5_surf = crimson_medium.render('Locked: Reach 5 Rooms', True, light_blue)
            lv_5_rect = lv_5_surf.get_rect(center=(500, 200))
            screen.blit(lv_5_surf, lv_5_rect)
    for bullet in red_bullets:
        pygame.draw.rect(screen,(255,255,255),bullet[0])
    check_if_collision_bullet(room_list,current_room_number,red_bullets)

    handle_bullets(red_bullets)
    pygame.display.update()
    clock.tick(60)
