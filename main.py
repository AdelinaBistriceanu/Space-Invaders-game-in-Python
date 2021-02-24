"""
                          Dezvoltare Jocuri PyGame

    Bistriceanu Adelina, Facultatea EtcTi, An 2, Seria A , Grupa 1.1

                         - Joc NAVETELE SPATIALE -

"""

#Biblioteci necesare
import math
import random
import pygame

from pygame import mixer                                # Importarea mixer-ului din modulul pygame, folosit pentru muzica de fundal


# Initializarea jocului
pygame.init()


# Crearea ferestrei
screen = pygame.display.set_mode((800, 600))            # Marimea ferestrei jocului este de 800x600


# Fundalul
background = pygame.image.load('Fundal.png')            # Incarcarea Imaginii de fundal


# Muzica
mixer.music.load("background.wav")                      # Incarcarea muzicii pe fundal
mixer.music.play(-1)


# Titlul si Iconita
pygame.display.set_caption("- Navetele Spatiale -")     # Scrierea titlului din TAB-ul jocului
icon = pygame.image.load('Iconita.png')                 # Incarcarea Inonitei
pygame.display.set_icon(icon)                           # Afisarea Iconitei


# Jucator
playerImg = pygame.image.load('Ufo.png')                # Incarcarea imaginii jucatorului
playerX = 370                                           # Pozitia initiala a jucatorului pe axa X la rularea jocului
playerY = 480                                           # Pozitia initiala a jucatorului pe axa Y la rularea jocului
playerX_change = 0


# Inamic
enemyImg = []                                           # Aceste coordonate sunt lasate goale,pentru ca prin functia matematica random,
enemyX = []                                             # coordonatele vor lua valori aleatoare pentru a nu putea prezice miscarile inamicilor
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5                                      # Numarul de inamici=5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Inamic.png'))    # Incarcarea si Alocarea imaginii pentru inamic
    enemyX.append(random.randint(0, 768))               # Inamicii apar in locuri aleatoare => o coordonata aleatoare pt X intre 0 si 736 ( nu putem pune maxim 800 pentru ca inamicii au in plus 32 pixeli pentru imagine)
    enemyY.append(random.randint(50, 150))              # Coordonata Y a inamicilor este aleatoare intre 50 (nu vrem ca inamicii sa treaca de nava jucatorului pana in marginea de jos a ferestrei) si 150
    enemyX_change.append(4)
    enemyY_change.append(40)                            # Cand pe axa X inamicul ajunge la coordonatele


# Glont                                                 # "ready" - Nu se poate vedea glontul pe ecran
bulletImg = pygame.image.load('glont.png')              # "fire" - Glontul se misca
bulletX = 0                                             # Coordonata de inceput pe axa X a glontului
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"                                  # Valoare de stare pentru glont


# Scorul
score_value = 0                                         # Valoare de inceput a scorului
font = pygame.font.Font('freesansbold.ttf', 32)         # Alegerea fontului si a marimii scrosului pentru scor
textX = 10                                              # Coordonatele X si Y de afisare a scorului
textY = 10



# Jocul s-a sfarsit
over_font = pygame.font.Font('freesansbold.ttf', 64)    #Alegerea fontului si marimii fontului pt afisarea

#Instructiuni
instr_font = pygame.font.Font('freesansbold.ttf', 14)

def show_score(x, y):                                   # Functia de afisare a scorului
    score = font.render("Scor : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():                                   # Functia cu afisarea mesajului "Jocul s-a sfarsit"
    over_text = over_font.render("JOCUL S-A SFARSIT", True, (255, 255, 255))
    screen.blit(over_text, (80, 250))

def show_instr():                                       # Cod adaugat de noi, afisarea intructiunilor de control
    instr1_text = instr_font.render("Control: Stanga - LeftArrowKey", True, (192, 192, 192))
    instr2_text = instr_font.render("         Dreapta - RightArrowKey", True, (192, 192, 192))
    instr3_text = instr_font.render("         Trage - Space", True, (192, 192, 192))
    instr4_text = instr_font.render("         Escape - Inchide Fereastra", True, (192, 192, 192))
    screen.blit(instr1_text, (550, 10))
    screen.blit(instr2_text, (577, 30))
    screen.blit(instr3_text, (577, 50))
    screen.blit(instr4_text, (577, 70))

def player(x, y):                                       # Definirea clasei jucator
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):                                     # Definirea clasei inamic
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):                                  # Definirea clasei glont
    global bullet_state
    bullet_state = "fire"                               # Daca starea glontului este "in tragere" atunci miscam imaginea glontului
    screen.blit(bulletImg, (x + 16, y + 10))            # Coordonatele pentru imaginea glontului, X-ul jucatorului + 16 pixeli pentru o prezentare aranjata, glontul vine de la mijlocul imaginii jucatorului

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:                                   # Formula de mai sus este formula matematica pentru distanta dintre 2 puncte
        return True                                     # Daca distanta calculata cu formula de mai sus este mai mica de 27 => cele 2 puncte se intersecteaza => are loc ciocnirea dintre glont si inamic
    else:
        return False



#bucla continua a jocului
running = True
while running:                                          # Toate variabilele care se modifica trebuiesc adaugate in while-ul jocului, pentru a fi totul actualizate

    # RVA= Rosu, Verde, Albastru
    screen.fill((0, 0, 0))                              # (0, 0, 0) = RVA ,colorarea fundalului sau a scrisului
    # Imaginea de fundal
    screen.blit(background, (0, 0))                     # Afisarea fundalului
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                   # Oprirea jocului
            running = False

        # Daca o tasta este apasata se verifica daca este in stanga sau in dreapta
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:              # Daca apasam ArrowKey-ul precizat => miscarea jucatorului in directic precizata
                playerX_change = -5                     # Instructiunile necesare pentru a se muta caracterul jucatorului in stanga, 5 = viteza optima pentru a nu se misca prea incet sau prea repede
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":             # Daca dorim sa tragem in inamici,se porneste sunetul de tragere al glontului
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX                   # Coordinata X a glontului este aceeasi cu coordonata x a jucatorului
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:                  # Miscarea jucatorului, daca apasam LeftArrowKey sau RightArrowKey ,acesta se misca in stanga sau in dreapta
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change                           # Secventa pentru miscarea jucatorului
    if playerX <= 0:                                    # Daca pe axa X suntem pe 0,pentru a nu merge inafara ferestrei jocului ramanem mereu pe minim 0
        playerX = 0
    elif playerX >= 736:                                # Daca pe axa X suntem pe 736 ( nu putem sa punem pe maxim 800 pentru ca imaginea jucatorului ocupa alti 64 de pixeli) ,pentru a nu merge inafara ferestrei jocului ramanem mereu pe maxim 736 + 64 marimea navei jucatorului
        playerX = 736

    # Miscarea inamicilor
    for i in range(num_of_enemies):                     # Toate schimbarile inamicilor se fac intr-un for pentru a se aplica tuturor inamicilor din cei 5

        #Sfarsitul Jocului
        if enemyY[i] > 440:                             # Cand inamicul a trecut de 440 de pizeli,mutam toti inamici dupa acesta
            for j in range(num_of_enemies):
                enemyY[j] = 2000                        # Cand jocul se sfarseste inamicii merg inafara ecranului => dispar pentru aparitia textului "Jocul s-a sfarsit"
            game_over_text()                            # Afisarea "Jocul s-a sfarsit"
            break

        enemyX[i] += enemyX_change[i]                   # Miscarea pe axa X a inamicilor
        if enemyX[i] <= 0:
            enemyX_change[i] = 4                        # Functiile necesare pentru ca inamicul sa nu poata iesi din fereastra jocului, similar cu conditia jucatorului ( boundries )
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]



        # Ciocnire
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:                                   # Folosim functia iscollision definita mai sus pentru a stii daca coordonata X sau Y a unui glont se intersecteaza cu coordonata x sau Y a unui inamic
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()                       # Secventa pentru pornirea sunetului de "ciocnire" atunci cand aceasta are loc
            bulletY = 480                               # Resetarea glontului la coordonata de start Y = 80
            bullet_state = "ready"                      # Dupa cionire putem trage alt glont daca il initializam din nou pe "ready"
            score_value += 1                            # Cand are loc o cionire => + 1 punct la scor
            enemyX[i] = random.randint(0, 768)          # Alt inamic apare in locul celui distrus, cu coordonate aleatoare
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)                  # Secventa pentru repetarea fiecarui inamic din cei 5

    # Miscarea Glontului
    if bulletY <= 0:                                    # Secventa pentru tragerea mai multor gloante
        bulletY = 480
        bullet_state = "ready"                          # Dupa ce am tras un glont, urmatorul glont este pe starea "ready" si gata sa fie pornit

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)                   # Desi doar coordonata Y se modifica la imaginea glontului care merge in sus, vrem ca coordonata X ca ramana aceeasi ca in momentul tragerii, nu sa urmareasca jucatorul pe axa X, de aceea includem si bulletX in secventa
        bulletY -= bulletY_change                       # Doar coordonata Y se modifica la glont atunci cand "tragem"

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = False                                 # Secventa pentru apasarea tastei ESCAPE = inchiderea ferestrei jocului

    player(playerX, playerY)                            # Afisarea jucatorului
    show_score(textX, textY)                            # Afisarea scorului
    show_instr()                                        # Afisarea
    pygame.display.update()                             # Display-ul trebuie mereu modificat dupa toate actiunile jucatorului

"""
      Bibliografie: https://www.youtube.com/watch?v=FfWpgLFMI7w&t=1928s
                    

"""
