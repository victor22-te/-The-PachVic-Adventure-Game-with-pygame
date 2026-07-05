#Importar librerías que se utilizan
#pgame(Biblioteca para la creación de videojuegos y multimedia)
#os(Módulo para tener el directorio del archivo actual en ejecución)
#random(Generación de elementos aleatorios)
#json(Hace muchas cosas como guardar y cargar datos del juego y configurarlo)
#datetime(Utiliza la fecha y hora actual del dispositivo utilizado

import pygame, os, random, json
from datetime import datetime

#Inicializa pygame
pygame.init()
#Controla la velocidad de los fotogramas del juego
clock=pygame.time.Clock()
#Ruta completa del directorio donde se encuentra el archivo actual
directory = os.path.dirname(os.path.realpath(__file__))

########## VENTANA ########## 

#Se definene las dimensiones de la ventana
SCREENWIDTH=800
SCREENHEIGHT=500
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
#Se establece el título de la ventana
pygame.display.set_caption("THE PACHVIC ADVENTURE")
#Se centra la ventaja del juego en la pantalla
os.environ['SDL_VIDEO_CENTERED'] = '1'
                   

RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (194,9,84)

#Se carga una imagen de fondo para el menú del juego
menuBg = pygame.transform.scale(pygame.image.load(directory + "\\sprites\\Porta.png").convert_alpha(), (size))

#Se crea un objeto de fuente de texto
myfont = pygame.font.SysFont('Lucida Console', 20)

#Se definen variables
userName = str
energy = 100
points = 0
date = str
speed = 5
first = True
fullscreen = False

########## SONIDOS ########## 

#Efectos de sonido utilizados en el juego
soundCrash = pygame.mixer.Sound(directory + "\\sounds\\crash.wav")
soundPoints = pygame.mixer.Sound(directory + "\\sounds\\success-1-6297.wav")
soundGameOver = pygame.mixer.Sound(directory + "\\sounds\\gameOver.wav")

##########  

#Representa un enemigo
class enemyCar(pygame.sprite.Sprite):
    #Inicializa las propiedades del enemigo
    def __init__(self, kind, lane):
        super().__init__()
        #Velocidad del enemigo
        global speed
        #Dimensiones del enemigo
        self.size = (50, 50)
        #Carga la imagen, la redimensiona y la rota 180°
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha(),self.size),180)
        #Manipula la posición y el tamaño del objeto
        self.rect = self.image.get_rect()
        #Crea máscara de colisión basada en los pixeles de la imagen
        self.mask = pygame.mask.from_surface(self.image)

        self.kind = kind
        self.lane = lane

        if self.kind == 1:
            self.image = pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha()
        elif self.kind == 2:
            self.image = pygame.image.load(directory + "\\sprites\\m2.jpg").convert_alpha()
        elif self.kind == 3:
            self.image = pygame.image.load(directory + "\\sprites\\m3.jpg").convert_alpha()
        elif self.kind == 4:
            self.image = pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha()
        elif self.kind == 5:
            self.image = pygame.image.load(directory + "\\sprites\\m3.jpg").convert_alpha()
        elif self.kind == 6:
            self.image = pygame.image.load(directory + "\\sprites\\m1.png").convert_alpha()
            
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.lane
        self.rect.y = -100
    #Se encarga de mover el objeto hacia adelante a una velocidad determinada    
    def moveForward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
            #Desaparece cuando sale de la pantalla
            self.kill()

enemyCar1 = enemyCar(1, 200)
enemyCarGroup = pygame.sprite.Group()
enemyCarGroup.add(enemyCar1)

#Representa las monedas
class thing(pygame.sprite.Sprite):

    def __init__(self, lane):
        super().__init__()
          
        self.image = pygame.transform.scale(pygame.image.load(directory + "\\sprites\\moneda.png").convert_alpha(), (50, 50))
        self.rect = self.image.get_rect()
        
        self.rect.y = -100
        self.rect.x = lane

    def moveForward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
           self.kill()
          
thing1 = thing(-200) 
thingGroup = pygame.sprite.Group()
thingGroup.add(thing1)

#Representa el burrito politécnico controlado por nosotres          
class kar(pygame.sprite.Sprite):
    #Ininicializa el burrito y la posición inicial
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load(directory + "\\sprites\\Nave2.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
    #Permite mover el burrito de derecha a izquierda respectivamente    
    def moveRight(self, pixels):
        if self.rect.x < 550:
            self.rect.x += pixels
 
    def moveLeft(self, pixels):
        if self.rect.x > 200:
            self.rect.x -= pixels

playerKar = kar() 
kar_group = pygame.sprite.Group() 
kar_group.add(playerKar)

#Representa el fondo del juego
class landscape(pygame.sprite.Sprite):
    
    global speed
    #Establece la posición inicial del paisaje en la pantalla
    def __init__(self, y):
        super().__init__()
       
        self.image = pygame.image.load(directory + "\\sprites\\levelBackground.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y
    #Mueve el paisaje hacia abajo a una velocidad establecida   
    def play(self):
        if self.rect.y < 500:
            self.rect.y += speed
        else:
            self.rect.y = -500
            
lands01 = landscape(-500) 
lands02 = landscape(0) 
lands_group = pygame.sprite.Group() 
lands_group.add(lands01) 
lands_group.add(lands02)

#Representa un botón en la interfaz del juego
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    #Dibuja el botón en la pantalla y cambia su color si el cursor del mouse está sobre el
    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = myfont.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = pygame.mouse.get_pos()
        if self.isOver(pos):
            self.color = WHITE
        else:
            self.color = GREY

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
                
        return False    

okBtn = button(RED, 250, 300, 200, 25, "ok")

#Representa una caja de texto en la interfaz del juego (Agregar nombre)
class InputBox:
    
    COLOR_INACTIVE = BLUE
    COLOR_ACTIVE = WHITE

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = myfont.render(text, True, BLACK)
        self.active = False
    #Maneja los eventos del mouse para activar y desactivar la caja de texto
    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                self.txt_surface = myfont.render(self.text, True, self.color)
    #Ajusta el ancho de la caja de texto en función del texto ingresado            
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    #Dibuja la caja de texto en la pantalla    
    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2) 
    
input_box1 = InputBox(100, 300, 140, 32)  

##### FUNCIONES #####

##### CAMBIO A LA PANTALLA

#Cambia la escena del juego
def changescn(scn, text="", btnfnc=""):
    
    #Establece variables globales
    # ~ continuar haciendo lo mismo que abajo
    global menu_s, enterName_s, mainLoop_s, instructions_s, msg_s, scores_s
    menu_s = enterName_s = mainLoop_s = instructions_s = msg_s = scores_s = False

   #scn cambia la escena del juego dependiendo del argumento y llama a la función correspondiente a la escena especificada 
    if scn == "menu":
        menu_s = True
        menu()
    
    elif scn == "enterName":
        enterName_s = True
        enterName()
        
    elif scn == "mainLoop":
        mainLoop_s = True
        mainLoop()
        
    elif scn == "instructions":
        instructions_s = True
        instructions()
        
    elif scn == "msg":
        msg_s = True
        msg(text,btnfnc)
        
    elif scn == "scores":
        scores_s = True
        scores()
        
#Esta función muestra un mensaje en la pantalla
msg_s = True
def msg(text,btnfnc):
    
    global msg_s, first
    
    #Se crea un botón y se renderiza una etiqueta con el texto del mensaje
    msgOkBtn = button(RED, SCREENWIDTH/2 - 100, SCREENHEIGHT/2, 200, 25, "ok")
    label = pygame.font.SysFont('Lucida Console', 30).render(text, 1, BLACK)
    
    #Si el texto del mensaje es "Game over" se detiene la reprodución de la música, se reinicica el juego y se reproduce un sonido de game over
    if text == "Game Over!":
        playMusic("stop")
        resetGame()
        first = True
        soundGameOver.play()
        
    while msg_s:
            
        screen.fill(MAGENTA)
        screen.blit(label, (SCREENWIDTH/2 - label.get_width()/2, SCREENHEIGHT/2 - label.get_height()/2 - 50))
        msgOkBtn.draw(screen, BLACK)
        
        
        pygame.display.flip()
        
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type==pygame.QUIT:
                msg_s = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if msgOkBtn.isOver(pos):
                    if text == "Game Over!":
                        playMusic("main")
    
                    changescn(btnfnc)
                    
            if event.type == pygame.KEYDOWN:
                                
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)

##### Cambio de Musica

#Se utiliza para controlar la reprodución de música
def playMusic(music):

    if music == "main":
        pygame.mixer.music.load(directory + "\\sounds\\music.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "engine":
        pygame.mixer.music.load(directory + "\\sounds\\the-limits-of-the-cosmos-43066.wav")
        pygame.mixer.music.play(-1)
        
    elif music == "stop":
        pygame.mixer.music.stop()
        
          
#Se utiliza para cambiar el modo de pantalla entre pantalla completa y ventana
def fnc(): 
    
    
    global fullscreen
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_f] and (all_keys[pygame.K_LSHIFT] or all_keys[pygame.K_RSHIFT]):
        
        fullscreen = not fullscreen
        if fullscreen == True:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(size)
            

            
          
            
##### Guardar puntos

sortedData = []
data = {}
#Se utiliza para guardar los datos del juego en un archivo de puntuaciones
def saveGame():
    
    global sortedData, data, date, points, userName
    
    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)

    data.update({date:{"name":userName, "points":points, "energy":energy}} )
    
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios
    try:
        del data[sortedData[10][0]]

    except IndexError:
        pass

    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)

#Se utiliza para incrementar los puntos y realizar acciones relacionadas con la aparición de objetos en el juego  
def things():
    
    global points, speed
     
    points += 1
    soundPoints.play()
    thing1.rect.y = 600
    thingGroup.add(thing1)
    speed += 1
    
#Se utiliza para mostrar la interfaz del usuario
def hud():

    global energy, userName, points
    
    label0 = myfont.render("Nombre: " + str(userName), 1, WHITE, BLACK)
    screen.blit(label0, (610, 20))     
    
    label1 = myfont.render("Vidas: " + str(energy), 1, WHITE, BLACK)
    screen.blit(label1, (610, 50))

    label2 = myfont.render("Puntos: " + str(points), 1, WHITE, BLACK)
    screen.blit(label2, (610, 80))
    
##### Lanzar carros y monedas

carsOut = 0
def launch():
    
    global carsOut
    kind = random.randint(1,6)
    laneRand = random.randint(1,8)
    lane = 0
  
    if laneRand == 1:
        lane = 200
    elif laneRand == 2:
        lane = 250
    elif laneRand == 3:
        lane = 300  
    elif laneRand == 4:
        lane = 350
    elif laneRand == 5:
        lane = 400
    elif laneRand == 6:
        lane = 450
    elif laneRand == 7:
        lane = 500
    elif laneRand == 8:
        lane = 550
        
    if carsOut < 5:

        enemyCar1 = enemyCar(kind, lane)
        enemyCarGroup.add(enemyCar1)
        carsOut += 1
        
    else: 
        
        thing1 = thing(lane)
        thingGroup.add(thing1)
        carsOut = 0
        

aux = False
#Se utilza para manejar las colisiones de los toros
def crash(value):
    
    global aux
    global energy

    if value == True and aux == False:
        energy -= 20
        soundCrash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if energy < 1:
        saveGame()
        changescn("msg", text="Valiste Brga!", btnfnc="menu")
        
##### resetear
#Restablece el juego a su estado inicial :D
def resetGame():
    global userName, energy, first, points, date, speed
    
    for i in enemyCarGroup:
        i.kill()
        
    for i in thingGroup:
        i.kill()
    
    userName = input_box1.text
    input_box1.text = "" 
    input_box1.txt_surface = myfont.render("", True, input_box1.color) 

    input_box1.update
    energy = 100
    points = 0
    speed = 5
   
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
        
########## ESCENAS ########## 

##### menu

menu_s = bool
#Define la escena del juego
def menu():
    
    global data, sortedData, menu_s, firts

    playBtn = button(RED, 450, 360, 200, 25, "JUGAR")
    scoresBtn = button(RED, 450, 390, 200, 25, "RECORDS")
    instBtn = button(RED, 450, 420, 200, 25, "INSTRUCCIONES")
    exitBtn = button(RED, 450, 450, 200, 25, "SALIR")
    backBtn = button(RED, 50, 35, 200, 25, "Regresar")

    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios

    while menu_s:
        
        fnc()
        
        ##### RENDER #####
        
        screen.blit(menuBg, (0, 0))
        playBtn.draw(screen, (0,0,0))
        scoresBtn.draw(screen, (0,0,0))
        instBtn.draw(screen, (0,0,0))
        exitBtn.draw(screen, (0,0,0))

        if first == False:
        
            backBtn.draw(screen, (0,0,0))

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # toma la posicion del mouse
 
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ control de los botones
                
                if playBtn.isOver(pos):         
                    changescn("enterName")
      
                if instBtn.isOver(pos):
                    changescn("instructions")
                
                if exitBtn.isOver(pos):
                    menu_s = False
                    
                if backBtn.isOver(pos):
                    changescn("mainLoop")
                    
                if scoresBtn.isOver(pos):
                    changescn("scores")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False
                    


        pygame.display.flip()
       
   
scores_s = bool
#Muestra la pantalla de puntuaciones
def scores():

    global data

    tag = "NOMBRE".ljust(10) + "PUNTOS".center(10) + "FECHA".rjust(10)

    #Muestra las puntuaciones de los primeros 10 registros
    if len(sortedData) > 0:
        place0 = str(data[(sortedData[0][0])]["name"].ljust(10) + str(data[(sortedData[0][0])]["points"]).center(10) + str(sortedData[0][0]).rjust(25))
    else:
        place0 = "Vaciooooo"
        
    if len(sortedData) > 1:
        place1 = str(data[(sortedData[1][0])]["name"].ljust(10) + str(data[(sortedData[1][0])]["points"]).center(10) + str(sortedData[1][0]).rjust(25))
    else:
        place1 = "Vaciooooo"
        
    if len(sortedData) > 2:
        place2 = str(data[(sortedData[2][0])]["name"].ljust(10) + str(data[(sortedData[2][0])]["points"]).center(10) + str(sortedData[2][0]).rjust(25))
    else:
        place2 = "Vaciooooo"
        
    if len(sortedData) > 3:
        place3 = str(data[(sortedData[3][0])]["name"].ljust(10) + str(data[(sortedData[3][0])]["points"]).center(10) + str(sortedData[3][0]).rjust(25))
    else:
        place3 = "Vaciooooo"
        
    if len(sortedData) > 4:
        place4 = str(data[(sortedData[4][0])]["name"].ljust(10) + str(data[(sortedData[4][0])]["points"]).center(10) + str(sortedData[4][0]).rjust(25))
    else:
        place4 = "Vaciooooo"
        
    if len(sortedData) > 5:
        place5 = str(data[(sortedData[5][0])]["name"].ljust(10) + str(data[(sortedData[5][0])]["points"]).center(10) + str(sortedData[5][0]).rjust(25))
    else:
        place5 = "Vaciooooo"
        
    if len(sortedData) > 6:
        place6 = str(data[(sortedData[6][0])]["name"].ljust(10) + str(data[(sortedData[6][0])]["points"]).center(10) + str(sortedData[6][0]).rjust(25))
    else:
        place6 = "Vaciooooo" 

    if len(sortedData) > 7:
        place7 = str(data[(sortedData[7][0])]["name"].ljust(10) + str(data[(sortedData[7][0])]["points"]).center(10) + str(sortedData[7][0]).rjust(25))
    else:
        place7 = "Vaciooooo"
        
    if len(sortedData) > 8:
        place8 = str(data[(sortedData[8][0])]["name"].ljust(10) + str(data[(sortedData[8][0])]["points"]).center(10) + str(sortedData[8][0]).rjust(25))
    else:
        place8 = "Vaciooooo"
        
    if len(sortedData) > 9:
        place9 = str(data[(sortedData[9][0])]["name"].ljust(10) + str(data[(sortedData[9][0])]["points"]).center(10) + str(sortedData[9][0]).rjust(25))
    else:
        place9 = "Vaciooooo"

    #Botón de regresar y restablecer
    scoresOk = button(RED, 150, 450, 200, 25, "Regresar")
    scoresClear = button(RED, 450, 450, 200, 25, "Restablecer")
    scoresTitle = myfont.render("RECORDS - TOP10", 1, WHITE, BLUE)
    tag2 = myfont.render(tag, 1, WHITE, BLUE)
    #Objetos de texto para renderizar las cadenas de texto en diferentes posiciones de la pantalla
    score0 = myfont.render(place0, 1, WHITE)
    score1 = myfont.render(place1, 1, WHITE)
    score2 = myfont.render(place2, 1, WHITE)
    score3 = myfont.render(place3, 1, WHITE)
    score4 = myfont.render(place4, 1, WHITE)
    score5 = myfont.render(place5, 1, WHITE)
    score6 = myfont.render(place6, 1, WHITE)
    score7 = myfont.render(place7, 1, WHITE)
    score8 = myfont.render(place8, 1, WHITE)
    score9 = myfont.render(place9, 1, WHITE)

    global scores_s
    while scores_s:
        
        fnc()
        
        
        screen.fill(BLUE)
        
        pygame.draw.rect(screen,BLACK,(90,20,600,400))
        #Dibuja cada objeto de texto en la superficie de la pantalla en las posiciones especificadas
        screen.blit(scoresTitle, (100, 30))
        screen.blit(tag2, (100, 80))
        screen.blit(score0, (100, 120))
        screen.blit(score1, (100, 150))
        screen.blit(score2, (100, 180))
        screen.blit(score3, (100, 210))
        screen.blit(score4, (100, 240))
        screen.blit(score5, (100, 270))
        screen.blit(score6, (100, 300))
        screen.blit(score7, (100, 330))
        screen.blit(score8, (100, 360))
        screen.blit(score9, (100, 390))
        
        scoresOk.draw(screen, (0,0,0))
        scoresClear.draw(screen, (0,0,0))

        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
 
            if event.type == pygame.QUIT:
                scores_s = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

            if event.type == pygame.MOUSEBUTTONDOWN:          
                if scoresOk.isOver(pos):
                    changescn("menu")
                    
                elif scoresClear.isOver(pos):
                    clearScores()

        pygame.display.flip()
        
def clearScores():
    
    global data, sortedData
    data.clear()
    sortedData.clear()
    
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)

    changescn("scores")
    
##### instrucciones

instructions_s = bool
#Mustra las instrucciones del juego en la pantalla
def instructions():
    
    global instructions_s
    
    backBtn = button(RED, 550, 450, 200, 25, "Regresar")

    label0 = myfont.render("Instrucciones:",  WHITE, BLUE)
    label1 = myfont.render("- Evita los meteoritos o mueres idiota", WHITE, BLUE)
    label2 = myfont.render("- Usa las letras 'A' y 'D' para esquivar los obstaculos", WHITE, BLUE)
    label3 = myfont.render("- Usa 'F' para hacer mas grande tu pantalla ",  WHITE, BLUE)
    label4 = myfont.render("- Tienes 5 vidas por juego",  WHITE, BLUE)
    label5 = myfont.render("- Recolecta las estrellas para obtener puntos", WHITE, BLUE)
    
    while instructions_s:
        
        fnc()
        
            
        screen.fill(BLUE)
        
        pygame.draw.rect(screen,BLACK,(25,20,750,400))
        
        screen.blit(label0, (30, 30))
        screen.blit(label1, (100, 100))
        screen.blit(label2, (100, 150))
        screen.blit(label3, (100, 200))
        screen.blit(label4, (100, 250))
        screen.blit(label5, (100, 300))

  
        backBtn.draw(screen, (0,0,0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                instructions_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")


enterName_s = False
#Muestra en la pantalla un apartado donde el jugador puede ingresar su nombre
def enterName():

    global enterName_s, user_text, first
    
    enterOkBtn = button(RED, 100, 350, 200, 25, "OK")
    enterBackBtn = button(RED, 550, 450, 200, 25, "Regresar")

    labelEnterName = myfont.render("Ingresa tu nombre:", 1, WHITE)

    while enterName_s:
        
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
                
                ############ control de los botones
                
                if enterOkBtn.isOver(pos):
                    
                    if input_box1.text == "":
                        changescn("msg", text="Que escribas tu nombre pndjo", btnfnc="enterName")
                            
                    else:
                        first = False
                        resetGame()
                        changescn("mainLoop")
         
                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                enterName_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
      
        ###########################

        pygame.display.flip()


count = 0
 
mainLoop_s = bool
#Variable global para controlar si el bucle del juego debe seguir ejecutandose
#En esta parte del código se establece el bucle principal del juego, maneja eventos de teclado y condiciones, actualiza los objetos en la pantalla y controla la música de fondo
def mainLoop():

    global mainLoop_s, first, count, fullscreen, size, speed
    
    playMusic("engine")
    
    while mainLoop_s:
        
        fnc()
        
        count += 1
        if count > 10:
            count = 0
            launch()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                mainLoop_s = False

 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            playerKar.moveLeft(5)
        if keys[pygame.K_d]:
            playerKar.moveRight(5)  

        if keys[pygame.K_t]:
            pass
            
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
        

        for car in enemyCarGroup:
            car.moveForward()
            
        for thing in thingGroup:
           thing.moveForward()

       
        car_collision_list = pygame.sprite.spritecollide(playerKar,enemyCarGroup,False,pygame.sprite.collide_mask)
        
        if car_collision_list:
            crash(True)
        else:
            crash(False)

        # cosas
        thing_collision = pygame.sprite.spritecollide(playerKar,thingGroup,True,pygame.sprite.collide_mask)
        
        if thing_collision:
            things()
   
        
        pygame.display.flip()
        clock.tick(60) 
        

playMusic("main")
menu()
pygame.quit()
