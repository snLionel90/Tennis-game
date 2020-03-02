#impotar pauqtetes, random
import pygame, sys
import random

#declaracion de constantes
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
BLACK = (0,0,0)
AMARILLO = (240, 200, 20)
ROJO = (251,51,90)
VERDE = (21,255,255)

BALL_RADIO = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
RIGHT=True
LEFT = False

marcador_1 = 0
marcador_2 = 0

#------------------------------------------------------------
#DECLARACION DE VARIABLES
running = True
tiempo = pygame.time.Clock()  
pelota = pygame.image.load('imagenes/bola.png')
bg = pygame.image.load('imagenes/pista.jpg')

#------------------------------------------------------------
#declaramos las funciones
#Pantalla de inicio

#Lanzo una bola desde el centro de la imagen
def lanza_bola(direccion):
    global ball_pos, ball_velocidad
    ball_pos = [ANCHO_VENTANA//2,ALTO_VENTANA//2]
    x_dir = random.randint(3,3)
    if direccion == LEFT:
        x_dir = -x_dir
    ball_velocidad=[x_dir, random.randint(-2,-1)]

def presion_tecla(tecla):
    global pala_1_incremento_y, pala_2_incremento_y

    if tecla == pygame.K_w:
        pala_1_incremento_y = -4
    if tecla == pygame.K_s:
        pala_1_incremento_y = 4
    
    if tecla == pygame.K_UP:
        pala_2_incremento_y = -4
    if tecla == pygame.K_DOWN:
        pala_2_incremento_y = 4
    
def teclaSuelta(tecla):
    global pala_1_incremento_y, pala_2_incremento_y
    if tecla == pygame.K_w or tecla == pygame.K_s:
        pala_1_incremento_y = 0

    if tecla == pygame.K_UP or tecla == pygame.K_DOWN:
        pala_2_incremento_y = 0

def moverPalasYbola():
    global marcador_1,marcador_2,ball_pos,ball_velocidad,pala_1_pos,pala_2_pos,pala_1_incremento_y,pala_2_incremento_y

    #contro de la bola limite derecho
    if ball_pos[0] + BALL_RADIO > ANCHO_VENTANA-pelota.get_width()+PAD_WIDTH:
        pygame.mixer.music.load('sonidos/toque.wav')
        pygame.mixer.music.play()
        if ball_pos[1] + BALL_RADIO < pala_2_pos[1] or ball_pos[1]-BALL_RADIO > pala_2_pos[1]+ PAD_HEIGHT:
            pygame.mixer.music.load('sonidos/out.mp3')
            pygame.mixer.music.play()
            marcador_1 +=1 
            lanza_bola(LEFT)
            
        else:
            ball_velocidad[0] = -ball_velocidad[0]

    #contro de la bola limite izquierdo
    if ball_pos[0] + BALL_RADIO < pelota.get_width()-20 - PAD_WIDTH:
        pygame.mixer.music.load('sonidos/toque.wav')
        pygame.mixer.music.play()
        if ball_pos[1] + BALL_RADIO < pala_1_pos[1] or ball_pos[1]-BALL_RADIO > pala_1_pos[1]+ PAD_HEIGHT:
            pygame.mixer.music.load('sonidos/out.mp3')
            pygame.mixer.music.play()
            marcador_2 +=1            
            lanza_bola(RIGHT)
            
        else:
            ball_velocidad[0] = -ball_velocidad[0]

    #actualizamos posicion de la bola
    ball_pos[0] = ball_pos[0]+ball_velocidad[0]
    ball_pos[1] = ball_pos[1]+ball_velocidad[1]

    #comprobar limites inferior y superior
    if ball_pos[1] <= BALL_RADIO or ball_pos[1] >= ALTO_VENTANA-BALL_RADIO:
        ball_velocidad[1] = -ball_velocidad[1]

    if (pala_1_pos[1]+pala_1_incremento_y) >=0 and (pala_1_pos[1] +pala_1_incremento_y) <=ALTO_VENTANA-PAD_HEIGHT:
        pala_1_pos[1] += pala_1_incremento_y
        

    if (pala_2_pos[1]+pala_2_incremento_y) >=0 and (pala_2_pos[1] +pala_2_incremento_y) <=ALTO_VENTANA-PAD_HEIGHT:
        pala_2_pos[1] += pala_2_incremento_y

def palas():
    #LAs palas
    pygame.draw.rect(canvas, ROJO,(pala_1_pos[0],pala_1_pos[1], PAD_WIDTH,PAD_HEIGHT))
    pygame.draw.rect(canvas, BLACK,(pala_2_pos[0],pala_2_pos[1],PAD_WIDTH,PAD_HEIGHT))

def pelotita(ball_pos,BALL_RADIO):
    canvas.blit(pelota, ball_pos)
    
def nuevoJuego():
    global pala_1_pos, pala_2_pos,pala_1_incremento_y,pala_2_incremento_y,marcador_1,marcador_2
    pala_1_pos= [0, (ALTO_VENTANA-PAD_HEIGHT)//2]
    pala_2_pos =[ANCHO_VENTANA-PAD_WIDTH,(ALTO_VENTANA-PAD_HEIGHT)//2]
    pala_1_incremento_y = 0
    pala_2_incremento_y = 0
    marcador_1 = 0
    marcador_2 = 0

    lanza_bola(RIGHT)
    lanza_bola(LEFT)

def inserta_texto():
    fuente1 =  pygame.font.SysFont("Calibri",24)
    titulo = fuente1.render('Juego Tenis by Lionel Sanchez',1,(ROJO))
    canvas.blit(titulo, (ANCHO_VENTANA//2+70,14))   
#------------------------------------------------------------
#Iniciando Juego y crea la pantalla
pygame.init()
nuevoJuego()
canvas = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption('Juego Tenis, Version de Lionel Sanchez')

#------------------------------------------------------------
#buclaso while
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        if evento.type == pygame.KEYDOWN:
            presion_tecla(evento.key)
        if evento.type == pygame.KEYUP:
            teclaSuelta(evento.key)

    #dibujando las pantallas
    canvas.blit (bg,[0,0])
    
    #inserta los puntos
    #JUGADOR 1
    fuente = pygame.font.SysFont("Arial", 40)
    texto1 = fuente.render(""+str(marcador_1), 1, (ROJO))
    canvas.blit(texto1, (ANCHO_VENTANA//2-70,50))
    txtJugador = fuente.render('J1',1,(ROJO))
    canvas.blit(txtJugador, (300,450))

    #JUGADOR 2
    texto2 = fuente.render(""+str(marcador_2), 1, (BLACK))
    canvas.blit(texto2, (ANCHO_VENTANA//2+70, 50)) 
    txtJugador2 = fuente.render('J2',1,(BLACK))
    canvas.blit(txtJugador2, (500,450))
    
    #Condicion de los marcadores
    #Cuando llege a 10 puntos, saldra una imagen en pantalla una copa y un texto con el nombre del jugador ganador
    if marcador_1 == 10:
        txt_ganador = fuente.render('Ha Ganado el jugador 1',1,(ROJO))
        canvas.blit(txt_ganador, (222,215))
        imagen = pygame.image.load('imagenes/copa.png')
        canvas.blit (imagen,[280,ALTO_VENTANA//2])
        pygame.mixer.music.load('./sonidos/corneta.wav')
        pygame.mixer.music.play(3)  
        ball_velocidad[0] = 0
        ball_velocidad[1] = 0       
    #Cuando llege a 10 puntos, saldra una imagen en pantalla una copa y un texto con el nombre del jugador ganador
    if marcador_2 == 10:
        txt_ganador = fuente.render('Ha Ganado el jugador 2',1,(BLACK))
        canvas.blit(txt_ganador, (222,215))
        imagen = pygame.image.load('imagenes/copa.png')
        canvas.blit (imagen,[280,ALTO_VENTANA//2])
        pygame.mixer.music.load('./sonidos/corneta.wav')
        pygame.mixer.music.play(3)      
        ball_velocidad[0] = 0
        ball_velocidad[1] = 0       
    #llamando a las funciones
    inserta_texto()       
    moverPalasYbola()
    palas()
    pelotita(ball_pos,BALL_RADIO)
    pygame.display.update()
    tiempo.tick(60)
    
pygame.quit()
sys.exit(0)