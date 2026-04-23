import pygame as pg
import os
import random as rd
import time


pg.init()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

if ".venv" in BASE_PATH:
    BASE_PATH = os.path.dirname(BASE_PATH)

IMG_PATH = os.path.join(BASE_PATH, "images")
os.chdir(IMG_PATH)
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Zombie Rabbit")
burrows = [(100,90),(320,90),(550,90),(85,315), (320,315), (550,315)]
back = pg.image.load("bg.png").convert_alpha()
front1 = pg.image.load("fg1.png").convert_alpha()
target_size = (150,150)
start = pg.image.load("start.png").convert_alpha()
won = pg.image.load("won.png").convert_alpha()

star = pg.image.load("star.png").convert_alpha()
star_p = pg.transform.scale(star,(30,30))

front2 = pg.image.load("fg2.png").convert_alpha()
rabbit_original = pg.image.load("rabbit.png").convert_alpha()
rabbit = pg.transform.scale(rabbit_original, target_size)

rabbit_zombie_original = pg.image.load("rabbit_zombie.png").convert_alpha()
rabbit_zombie = pg.transform.scale(rabbit_zombie_original, target_size)

rabbit_dead_original = pg.image.load("rabbit_dead.png").convert_alpha()
rabbit_dead = pg.transform.scale(rabbit_dead_original, target_size)

rabbit_half_original = pg.image.load("rabbit_halfzombie.png").convert_alpha()
rabbit_half = pg.transform.scale(rabbit_half_original, target_size)

exit_game = pg.image.load("exit.png").convert_alpha()
restart = pg.image.load("restart.png").convert_alpha()
game_over = pg.image.load("game_over.png").convert_alpha()

rabbits = []

game_state = "playing"

for index, pos in enumerate(burrows):
    if index < 3:
        current_layer = 0
    else:
        current_layer = 1

    rabbit_data = {
        "image": rabbit,
        "x": pos[0],
        "y": pos[1] + 150,
        "target_y" : pos[1] + 150,
        "base_y": pos[1],
        "hidden_y" : pos[1] + 150,
        "pos": pos,
        "layer": current_layer,
        "status" : "normal",
        "timer" : rd.randint(1000,3000),
        "pause" : 0
    }
    rabbits.append(rabbit_data)



clock = pg.time.Clock()
spawn_time = 0
delay = 2000


score = 0



screen.blit(start,(0,0))
pg.display.flip()
time.sleep(3)

x_st = 750
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False





        if event.type == pg.MOUSEBUTTONDOWN:
            if game_state =="playing":
                for r in rabbits:
                    rect = r["image"].get_rect(topleft=(r["x"],r["y"]))
                    if rect.collidepoint(event.pos):
                        if r['y'] < r['hidden_y'] - 20:
                            if r['status'] == "half":
                                score += 1


                                r['image'] = rabbit_zombie
                                r['status']= "dead"
                                r["timer"] = 1000
                                r['target_y'] = r['hidden_y']
                                r['pause']=700

                            elif r['status'] == "normal":
                                r['image'] = rabbit_dead
                                r['status'] = "dead_rabbit"

                                r["pause"] = 700

            elif game_state == "game over":
                screen.blit(game_over, (0, 0))
                restart_rect = restart.get_rect(center=(320, 360))
                exit_rect = exit_game.get_rect(center=(510, 360))
                if restart_rect.collidepoint(event.pos):
                    score = 0
                    game_state = "playing"
                    for r in rabbits:
                        r['y'] = r['hidden_y']
                        r['target_y'] = r['hidden_y']
                        r['timer'] = rd.randint(3000,7000)
                        r['pause'] =0
                elif exit_rect.collidepoint(event.pos):
                    running = False



    dt = clock.tick(60)

    if game_state == "playing":
        for r in rabbits:
            r["timer"] -= dt
            if r['pause'] > 0:
                r['pause'] -= dt
                if r['status'] == 'dead_rabbit' and r['pause'] <= 0:
                    game_state = "game over"


            if r["timer"] <= 0:
                if r["status"] == "dead":
                    r["target_y"] = r["hidden_y"]
                    r["timer"] = rd.randint(8000,9000)
                    r["status"] = "normal"

                if r['target_y'] == r ["hidden_y"]:
                    r['target_y'] = r['base_y']

                    r['timer'] = rd.randint(3000,7000)
                    if rd.random() < 0.2:
                        r['image'] = rabbit_half
                        r['status'] = "half"
                    else:
                        r['image'] = rabbit
                        r['status'] = "normal"
                else:
                    r['target_y'] = r['hidden_y']
                    r['timer'] = rd.randint(3000,7000)

            if r['pause'] <= 0:
                if r["y"] < r['target_y']:
                    r['y'] += 10
                if r["y"] > r["target_y"]:
                    r["y"] -= 10

        screen.blit(back, (0, 0))
        for r in rabbits:
            if r['layer'] == 0 :
                screen.blit(r["image"], (r["x"], r["y"]))
        screen.blit(front1,(0,0))

        for r in rabbits:
            if r["layer"] == 1:
                screen.blit(r["image"], (r["x"], r["y"]))
        screen.blit(front2, (0, 0))
        for s in range(score):
            current_s = x_st - (s * 30)
            screen.blit(star_p, (current_s, 15))
    elif game_state == "game over":
        screen.blit(game_over, (0, 0))
        restart_rect = restart.get_rect(center=(320, 360))
        exit_rect = exit_game.get_rect(center=(510, 360))

        screen.blit(exit_game, exit_rect)
        screen.blit(restart, restart_rect)
    if score >= 10:
        screen.blit(won, (0,0))
        game_state = "won"
        pg.display.flip()
        


    pg.display.flip()
pg.quit()



