import pygame, os, random, json
from datetime import datetime

import settings
import state
from sprites import enemyCar, thing, kar, landscape
from ui import button, InputBox

# Inicializa pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(settings.size)
pygame.display.set_caption("THE PACHVIC ADVENTURE")
os.environ['SDL_VIDEO_CENTERED'] = '1'

menuBg = pygame.transform.scale(pygame.image.load(settings.directory + "\\sprites\\Porta.png").convert_alpha(), settings.size)
myfont = pygame.font.SysFont('Lucida Console', 20)

soundCrash = pygame.mixer.Sound(settings.directory + "\\sounds\\crash.wav")
soundPoints = pygame.mixer.Sound(settings.directory + "\\sounds\\success-1-6297.wav")
soundGameOver = pygame.mixer.Sound(settings.directory + "\\sounds\\gameOver.wav")

enemyCarGroup = pygame.sprite.Group()
thingGroup = pygame.sprite.Group()
kar_group = pygame.sprite.Group()
lands_group = pygame.sprite.Group()

playerKar = kar()
kar_group.add(playerKar)

lands01 = landscape(-500)
lands02 = landscape(0)
lands_group.add(lands01)
lands_group.add(lands02)

okBtn = button(settings.RED, 250, 300, 200, 25, myfont, "ok")
input_box1 = InputBox(100, 300, 140, 32, myfont)

def changescn(scn, text="", btnfnc=""):
    state.menu_s = state.enterName_s = state.mainLoop_s = state.instructions_s = state.msg_s = state.scores_s = False

    if scn == "menu":
        state.menu_s = True
        menu()
    elif scn == "enterName":
        state.enterName_s = True
        enterName()
    elif scn == "mainLoop":
        state.mainLoop_s = True
        mainLoop()
    elif scn == "instructions":
        state.instructions_s = True
        instructions()
    elif scn == "msg":
        state.msg_s = True
        msg(text, btnfnc)
    elif scn == "scores":
        state.scores_s = True
        scores()

def msg(text, btnfnc):
    msgOkBtn = button(settings.RED, settings.SCREENWIDTH/2 - 100, settings.SCREENHEIGHT/2, 200, 25, myfont, "ok")
    label = pygame.font.SysFont('Lucida Console', 30).render(text, 1, settings.BLACK)
    
    if text == "Game Over!":
        playMusic("stop")
        resetGame()
        state.first = True
        soundGameOver.play()
        
    while state.msg_s:
        screen.fill(settings.MAGENTA)
        screen.blit(label, (settings.SCREENWIDTH/2 - label.get_width()/2, settings.SCREENHEIGHT/2 - label.get_height()/2 - 50))
        msgOkBtn.draw(screen, settings.BLACK)
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
                state.msg_s = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if msgOkBtn.isOver(pos):
                    if text == "Game Over!":
                        playMusic("main")
                    changescn(btnfnc)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)

def playMusic(music):
    if music == "main":
        pygame.mixer.music.load(settings.directory + "\\sounds\\music.wav")
        pygame.mixer.music.play(-1)
    elif music == "engine":
        pygame.mixer.music.load(settings.directory + "\\sounds\\the-limits-of-the-cosmos-43066.wav")
        pygame.mixer.music.play(-1)
    elif music == "stop":
        pygame.mixer.music.stop()

def fnc(): 
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_f] and (all_keys[pygame.K_LSHIFT] or all_keys[pygame.K_RSHIFT]):
        state.fullscreen = not state.fullscreen
        if state.fullscreen:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(settings.size)

def saveGame():
    try:
        with open(settings.directory + "\\save\\" + "scores.txt", "r") as f:
            state.data = json.load(f)
    except FileNotFoundError:
        state.data = {}

    state.data.update({state.date:{"name":state.userName, "points":state.points, "energy":state.energy}})
    state.sortedData = sorted(state.data.items(), key=lambda x: x[1]['points'], reverse=True)
    try:
        del state.data[state.sortedData[10][0]]
    except IndexError:
        pass

    with open(settings.directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(state.data, f)

def things():
    state.points += 1
    soundPoints.play()
    thing1 = thing(-200)
    thing1.rect.y = 600
    thingGroup.add(thing1)
    state.speed += 1

def hud():
    label0 = myfont.render("Nombre: " + str(state.userName), 1, settings.WHITE, settings.BLACK)
    screen.blit(label0, (610, 20))     
    label1 = myfont.render("Vidas: " + str(state.energy), 1, settings.WHITE, settings.BLACK)
    screen.blit(label1, (610, 50))
    label2 = myfont.render("Puntos: " + str(state.points), 1, settings.WHITE, settings.BLACK)
    screen.blit(label2, (610, 80))

def launch():
    kind = random.randint(1,6)
    laneRand = random.randint(1,8)
    lane = 0
    if laneRand == 1: lane = 200
    elif laneRand == 2: lane = 250
    elif laneRand == 3: lane = 300  
    elif laneRand == 4: lane = 350
    elif laneRand == 5: lane = 400
    elif laneRand == 6: lane = 450
    elif laneRand == 7: lane = 500
    elif laneRand == 8: lane = 550
        
    if state.carsOut < 5:
        enemyCar1 = enemyCar(kind, lane)
        enemyCarGroup.add(enemyCar1)
        state.carsOut += 1
    else: 
        thing1 = thing(lane)
        thingGroup.add(thing1)
        state.carsOut = 0

def crash(value):
    if value == True and state.aux == False:
        state.energy -= 20
        soundCrash.play()
        state.aux = True
    if value == False and state.aux == True:
        state.aux = False

    if state.energy < 1:
        saveGame()
        changescn("msg", text="Valiste Brga!", btnfnc="menu")

def resetGame():
    for i in enemyCarGroup: i.kill()
    for i in thingGroup: i.kill()
    
    state.userName = input_box1.text
    input_box1.text = "" 
    input_box1.txt_surface = myfont.render("", True, input_box1.color) 
    input_box1.update()
    
    state.energy = 100
    state.points = 0
    state.speed = 5
   
    now = datetime.now()
    state.date = now.strftime("%d/%m/%Y %H:%M:%S")

def menu():
    playBtn = button(settings.RED, 450, 360, 200, 25, myfont, "JUGAR")
    scoresBtn = button(settings.RED, 450, 390, 200, 25, myfont, "RECORDS")
    instBtn = button(settings.RED, 450, 420, 200, 25, myfont, "INSTRUCCIONES")
    exitBtn = button(settings.RED, 450, 450, 200, 25, myfont, "SALIR")
    backBtn = button(settings.RED, 50, 35, 200, 25, myfont, "Regresar")

    try:
        with open(settings.directory + "\\save\\" + "scores.txt", "r") as f:
            state.data = json.load(f)
    except FileNotFoundError:
        state.data = {}
    state.sortedData = sorted(state.data.items(), key=lambda x: x[1]['points'], reverse=True)

    while state.menu_s:
        fnc()
        screen.blit(menuBg, (0, 0))
        playBtn.draw(screen, (0,0,0))
        scoresBtn.draw(screen, (0,0,0))
        instBtn.draw(screen, (0,0,0))
        exitBtn.draw(screen, (0,0,0))

        if not state.first:
            backBtn.draw(screen, (0,0,0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                state.menu_s = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playBtn.isOver(pos):         
                    changescn("enterName")
                if instBtn.isOver(pos):
                    changescn("instructions")
                if exitBtn.isOver(pos):
                    state.menu_s = False
                if backBtn.isOver(pos) and not state.first:
                    changescn("mainLoop")
                if scoresBtn.isOver(pos):
                    changescn("scores")
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    state.menu_s = False
        pygame.display.flip()

def scores():
    tag = "NOMBRE".ljust(10) + "PUNTOS".center(10) + "FECHA".rjust(10)
    def get_place(i):
        if len(state.sortedData) > i:
            key = state.sortedData[i][0]
            val = state.data[key]
            return str(val["name"].ljust(10) + str(val["points"]).center(10) + str(key).rjust(25))
        return "Vaciooooo"

    places = [get_place(i) for i in range(10)]

    scoresOk = button(settings.RED, 150, 450, 200, 25, myfont, "Regresar")
    scoresClear = button(settings.RED, 450, 450, 200, 25, myfont, "Restablecer")
    scoresTitle = myfont.render("RECORDS - TOP10", 1, settings.WHITE, settings.BLUE)
    tag2 = myfont.render(tag, 1, settings.WHITE, settings.BLUE)
    
    score_renders = [myfont.render(p, 1, settings.WHITE) for p in places]

    while state.scores_s:
        fnc()
        screen.fill(settings.BLUE)
        pygame.draw.rect(screen,settings.BLACK,(90,20,600,400))
        
        screen.blit(scoresTitle, (100, 30))
        screen.blit(tag2, (100, 80))
        for i, render in enumerate(score_renders):
            screen.blit(render, (100, 120 + i*30))
            
        scoresOk.draw(screen, (0,0,0))
        scoresClear.draw(screen, (0,0,0))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            if event.type == pygame.QUIT:
                state.scores_s = False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")
            if event.type == pygame.MOUSEBUTTONDOWN:          
                if scoresOk.isOver(pos):
                    changescn("menu")
                elif scoresClear.isOver(pos):
                    clearScores()
                    return
        pygame.display.flip()
        
def clearScores():
    state.data.clear()
    state.sortedData.clear()
    with open(settings.directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(state.data, f)
    changescn("scores")

def instructions():
    backBtn = button(settings.RED, 550, 450, 200, 25, myfont, "Regresar")
    labels = [
        myfont.render("Instrucciones:",  settings.WHITE, settings.BLUE),
        myfont.render("- Evita los meteoritos o mueres idiota", settings.WHITE, settings.BLUE),
        myfont.render("- Usa las letras 'A' y 'D' para esquivar los obstaculos", settings.WHITE, settings.BLUE),
        myfont.render("- Usa 'F' para hacer mas grande tu pantalla ",  settings.WHITE, settings.BLUE),
        myfont.render("- Tienes 5 vidas por juego",  settings.WHITE, settings.BLUE),
        myfont.render("- Recolecta las estrellas para obtener puntos", settings.WHITE, settings.BLUE)
    ]
    
    while state.instructions_s:
        fnc()
        screen.fill(settings.BLUE)
        pygame.draw.rect(screen,settings.BLACK,(25,20,750,400))
        
        screen.blit(labels[0], (30, 30))
        for i, lbl in enumerate(labels[1:]):
            screen.blit(lbl, (100, 100 + i*50))

        backBtn.draw(screen, (0,0,0))
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backBtn.isOver(pos):
                    changescn("menu")
            if event.type == pygame.QUIT:
                state.instructions_s = False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

def enterName():
    enterOkBtn = button(settings.RED, 100, 350, 200, 25, myfont, "OK")
    enterBackBtn = button(settings.RED, 550, 450, 200, 25, myfont, "Regresar")
    labelEnterName = myfont.render("Ingresa tu nombre:", 1, settings.WHITE)

    while state.enterName_s:
        fnc()
        screen.blit(menuBg, (0, 0)) 
        enterOkBtn.draw(screen, (0,0,0)) 
        enterBackBtn.draw(screen, (0,0,0))
        screen.blit(labelEnterName, (100, 270))  
        
        input_box1.update()
        input_box1.draw(screen) 
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box1.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if enterOkBtn.isOver(pos):
                    if input_box1.text == "":
                        changescn("msg", text="Que escribas tu nombre pndjo", btnfnc="enterName")
                    else:
                        state.first = False
                        resetGame()
                        changescn("mainLoop")
                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                state.enterName_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
        pygame.display.flip()

count = 0
def mainLoop():
    global count
    playMusic("engine")
    
    while state.mainLoop_s:
        fnc()
        count += 1
        if count > 10:
            count = 0
            launch()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.mainLoop_s = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            playerKar.moveLeft(5)
        if keys[pygame.K_d]:
            playerKar.moveRight(5)  
        if keys[pygame.K_ESCAPE]:
            saveGame()
            playMusic("main")
            changescn("menu")

        lands_group.draw(screen)
        enemyCarGroup.draw(screen)
        kar_group.draw(screen)        
        thingGroup.draw(screen)

        hud()
        lands01.play()
        lands02.play()

        for car in enemyCarGroup: car.moveForward()
        for t in thingGroup: t.moveForward()

        car_collision_list = pygame.sprite.spritecollide(playerKar, enemyCarGroup, False, pygame.sprite.collide_mask)
        if car_collision_list: crash(True)
        else: crash(False)

        thing_collision = pygame.sprite.spritecollide(playerKar, thingGroup, True, pygame.sprite.collide_mask)
        if thing_collision: things()
   
        pygame.display.flip()
        clock.tick(60) 

if __name__ == "__main__":
    playMusic("main")
    state.menu_s = True
    menu()
    pygame.quit()
