import math
import random
import sys
import os
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import datetime

import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1920, 1080))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

# startscreen value
startscreen = True

# Background
background = pygame.image.load('img/background_own.png')
score_list = []

# Sound
music_base =pygame.mixer.Sound("sounds/music_base.wav")
music_level3 =pygame.mixer.Sound("sounds/music_level3.wav")
music_level4 =pygame.mixer.Sound("sounds/music_level4.wav")
music_level5 =pygame.mixer.Sound("sounds/music_level5.wav")
background_music = [music_base, music_base, music_level3, music_level4, music_level5]
background_music[0].play()

# Caption and Icon
pygame.display.set_caption("Safe the diasours")
#icon = pygame.image.load('ufo.png')
#pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('img/dino_klein2.png')
playerX = width / 2
playerY = height - 120
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4
enemies_speed = 0.5

lag_right = 5
lag_left = -5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/meteor.png'))
    enemyX.append(random.randint(120, width - 120))
    enemyY.append(random.randint(-50, 100))
    enemyX_change.append(enemies_speed)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('img/fireball.png')
bulletX = 0
bulletY = 480 *2
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Create user defined events
#freeze_event = pygame.USEREVENT + 1
#freeze_counter = 0

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_list = []

textX = 10
testY = 10

# lives

live_value = 3

liveX = 10
liveY = 70

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# User Event for freezing and lagging and timemanagement
freeze = pygame.USEREVENT + 0
lag = pygame.USEREVENT + 1
level_time = pygame.USEREVENT + 2

pygame.time.set_timer(level_time, 60000)

# Level
level = 1 

levelX = 10
levelY = 40

# boolean for enable/disable lagging and freezing
manipulationFunction = False

try: 
    manipulation = sys.argv[2]
except:
    manipulation = "Disabled"

if manipulation == "E":
    manipulation = "Enabled"
    manipulationFunction = True

# name variable for user name
name = ""

# input of the name via terminal like: python main.py your_name
try:
    name = sys.argv[1]
except:
    name = 'No_name'
score_list.append({'Name': str(name), 'Score': score_value})

# make a folder for the participant
if not os.path.exists(name):
    os.makedirs(name)

# questionaire
key_pressed_counter = 0
number_events = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]


# Create Webcrawler to obtain mionix mouse data
try:
    url = "http://localhost:8080/"
    driver_path = "C:\\Program Files\\chromedriver_win32\\chromedriver" # SET TO YOUR LOCAL PATH
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path = driver_path, options = chrome_options)
    driver.get(url)
except:
    print("could not connect to mionix hub\n")
    print("possible fixes: set chromedriver location\n start node server\n")

# loop setup to obtain biometric values
gsr_script = "return window.gsr;"
hr_script = "return window.hr;"
gsr_list = []
hr_list = []
gsr_list_time = []
hr_list_time = []
gsr = 0
hr = 0


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
    
def writeKeysToCsv(tempDict, fields, filename, username, manipulation, level):

    path = "".join((username, "/",filename, "_", username, "_", manipulation, "_level", str(level), ".csv"))
    print(path)
    if os.path.exists(path):
        # wenn der File schon existiert und das Level neu gestartet wird, werden die Daten an die alten angefuegt (evtl. aendern)
        with open(path, 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
            # writing data rows
            csvwriter.writerows(tempDict)
    else:
        with open(path, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
            # writing fields
            csvwriter.writeheader()
            # writing data rows
            csvwriter.writerows(tempDict)

def writeGSRToCsv(gsr_list):
    global name, manipulation, level 
    print("in gsr")
    path = "".join((name, "/", "grs_", name, "_", manipulation, "_level", str(level), ".csv"))
    print(path)
    if os.path.exists(path):
        # wenn der File schon existiert und das Level neu gestartet wird, werden die Daten an die alten angefuegt (evtl. aendern)
        with open(path, 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = ['Time [s]','GSR', 'actual_time'])
            # writing data rows
            csvwriter.writerows(gsr_list)
    else:
        with open(path, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = ['Time [s]','GSR','actual_time'])
            # writing fields
            csvwriter.writeheader()
            # writing data rows
            csvwriter.writerows(gsr_list)

def writeHRToCsv(hr_list):
    print("in hr")
    global name, manipulation, level 
    path = "".join((name,"/hr_", name, "_", manipulation, "_level", str(level), ".csv"))
    print(path)
    if os.path.exists(path):
        # wenn der File schon existiert und das Level neu gestartet wird, werden die Daten an die alten angefuegt (evtl. aendern)
        with open(path, 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = ['Time [s]','HR','actual_time'])
            # writing data rows
            csvwriter.writerows(hr_list)
    else:
        with open(path, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = ['Time [s]','HR','actual_time'])
            # writing fields
            csvwriter.writeheader()
            # writing data rows
            csvwriter.writerows(hr_list)


def writeQuestionsToCsv(array, fields, filename, username, manipulation, level):

    path = "".join((username, "/",filename, "_", username, "_", manipulation, "_level", str(level), ".csv"))
    print(path)
    if os.path.exists(path):
        # wenn der File schon existiert und das Level neu gestartet wird, werden die Daten an die alten angefuegt (evtl. aendern)
        with open(path, 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
            # writing data rows
            for i in array:
                csvwriter.writerows(i)
    else:
        with open(path, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
            # writing fields
            csvwriter.writeheader()
            # writing data rows
            for i in array:
                csvwriter.writerows(i)


def writeScoreToCsv(array, fields, filename, username, manipulation):

    row_count = 0

    path = "".join((username, "/",filename, "_", username, "_", manipulation,  ".csv"))
    print(path)
    if os.path.exists(path):
        # wenn der File schon existiert und das Level neu gestartet wird, werden die Daten an die alten angefuegt (evtl. aendern)
        with open(path, 'a') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
            # writing data 
            csvwriter.writerow(array)
            #for i in array:
             #   csvwriter.writerow(i)
    else:
        with open(path, 'w') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
            # writing fields
            csvwriter.writeheader()
            # writing data 
            csvwriter.writerow(array)
            #for i in array:
            #    csvwriter.writerow(i)

    # with open(filename, 'a') as csvfile:
    #     csvwriter = csv.DictWriter(csvfile, fieldnames = fields)
    #     if row_count == 0:
    #         csvwriter.writeheader()


    #     csvwriter.writerows(tempDict)

def show_level(x, y):
    score = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_lives(x, y):
    score = font.render("Lives : " + str(live_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def next_level_text(level):
    global score_value

    #specific level texts for maipulated case
    level_text = [" and his family. Game Over!","Well done!",
                    "Can you destroy some more?",
                    "That’s less than the average. :(",
                    "About 70% of the players are better than you!",
                    "Unfortunately you couldn’t save the dinosaur" ]
      
    over_text = over_font.render("You destroyed " + str(score_value) +" meteorites!", True, (255, 255, 255))
    screen.blit(over_text, (400, 350))

    if manipulationFunction:
        over_text = over_font.render(level_text[level-1], True, (255, 255, 255))
        screen.blit(over_text, (400, 450))      
    # in last level don't show space to continue    
    if manipulationFunction and level == 0:
        over_text = over_font.render(level_text[level], True, (255, 255, 255))
        screen.blit(over_text, (400, 550))
    else:
        over_text = over_font.render("Press space to continue.", True, (255, 255, 255))
        screen.blit(over_text, (400, 550))
    pygame.display.update()

    
def count_numbers(level):
    global key_pressed_counter
    actualized_level = level - 1

    mixer.pause()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in number_events:
                keyname = pygame.key.name(event.key)
                released_question = [{'question': str(key_pressed_counter + 1), 'value': keyname}]

                if actualized_level != 0:
                    writeKeysToCsv(released_question, ['question', 'value'], "questionaire", name, manipulation, int(level-1))

                key_pressed_counter += 1
                mixer.unpause()
                return
        
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    quit()


def questionaire_head_text():

    # erase the text, which is shown before
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    question_text = "A little questionnaire :)"
    between_text = over_font.render(question_text, True, (255, 255, 255))
    screen.blit(between_text, (400, 150))

    question_text = "How did you feel during the level?"
    between_text = over_font.render(question_text, True, (255, 255, 255))
    screen.blit(between_text, (400, 250))

    question_text = "-> Press 0 (not at all) up to 9 (very)."
    between_text = over_font.render(question_text, True, (255, 255, 255))
    screen.blit(between_text, (400, 350))


def questionaire_text():

    global key_pressed_counter

    questionaire_head_text()

    q1 = "I felt frustrated while playing."
    q2 = "I enjoyed playing the level."
    q3 = "The level was very difficult."

    # between_text = over_font.render(question_text, True, (255, 255, 255))
    # screen.blit(between_text, (400, 150))

    if key_pressed_counter == 0:
        question1 = over_font.render(q1, True, (108, 166, 205))
        question2 = over_font.render(q2, True, (255, 255, 255))
        question3 = over_font.render(q3, True, (255, 255, 255))
        # screen.blits((question1, (400, 450)), (question2, (400, 550)), (question3, (400, 650)))
        screen.blit(question1, (400, 550))
        screen.blit(question2, (400, 650))
        screen.blit(question3, (400, 750))
        # count_numbers()

    if key_pressed_counter == 1:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        questionaire_head_text()

        question1 = over_font.render(q1, True, (255, 255, 255))
        question2 = over_font.render(q2, True, (108, 166, 205))
        question3 = over_font.render(q3, True, (255, 255, 255))
        # screen.blits((question1, (400, 450)), (question2, (400, 550)), (question3, (400, 650)))
        screen.blit(question1, (400, 550))
        screen.blit(question2, (400, 650))
        screen.blit(question3, (400, 750))
        # count_numbers()

    if key_pressed_counter == 2:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        questionaire_head_text()

        question1 = over_font.render(q1, True, (255, 255, 255))
        question2 = over_font.render(q2, True, (255, 255, 255))
        question3 = over_font.render(q3, True, (108, 166, 205))
        # screen.blits((question1, (400, 450)), (question2, (400, 550)), (question3, (400, 650)))
        screen.blit(question1, (400, 550))
        screen.blit(question2, (400, 650))
        screen.blit(question3, (400, 750))
        # count_numbers()

    if key_pressed_counter == 3:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        space_text = over_font.render("Press space to continue.", True, (255, 255, 255))
        screen.blit(space_text, (400, 750))
        key_pressed_counter = 0

    pygame.display.update()


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))



def freezing():
    global enemyY, enemyY_change, gsr_time, name, manipulation, level
    print("freezing")
    random_value = random.randint(0, 1500)
    pygame.time.delay(random_value)

    freeze_data = [{'freeze_duration [ms]' : random_value, 'time [s]': time.time() - gsr_time, 'actual_time': datetime.now()}]

    writeKeysToCsv(freeze_data, ['freeze_duration [ms]','time [s]', 'actual_time'], "freezeLog", name, manipulation, level)

    # update meteors according to time it was freezing
    t = int(random_value / 10)
    #print(t)
    for x in range(1,t):
        for i in range(num_of_enemies):
            enemyY[i] += enemyX_change[i]

# pygame.time.set_timer(freeze, 5000)


def lagging(key):
    random_value1 = random.randint(-3, 0)
    random_value2 = random.randint(0, 3)
    if key == pygame.K_a:
        return random_value2
    if key == pygame.K_d:
        return random_value1


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27*2:
        return True
    else:
        return False

def next_level():
    global level, num_of_enemies, enemyX, enemyY, enemyImg, enemyX_change, enemyY_change, enemies_speed
    global live_value, score_value, gsr_list, hr_list, gsr_time, name, manipulation

    # write score list
    score_list=({'Name': str(name), 'Level': level, 'Score': score_value, 'Lives at end': live_value })

    writeScoreToCsv(score_list, ['Name','Level','Score','Lives at end'],  "scores", name, manipulation)

    try:
        writeGSRToCsv(gsr_list)
        writeHRToCsv(hr_list)
    except:
        pass

    # reset gsr and hr
    gsr_list = []
    hr_list = []

    # set to nex level, max 5
    if level < 5:
        background_music[level-1].stop()
        background_music[level].play()
        
        level = level + 1
        live_value = 3
    else :
        level = 0

    # "E" for enable manipulation
    if (manipulationFunction):

        # update lagging

        if level == 3 or level == 4 or level == 5:
            
            lag_left = lagging(pygame.K_a)
            lag_right = lagging(pygame.K_d)
            #live_value = 8


        # update freezing

        if level == 3:
            pygame.time.set_timer(freeze, 20000)
        
        if level == 4:
            pygame.time.set_timer(freeze, 15000)

        if level == 5:
            pygame.time.set_timer(freeze, 7500)

    # update enemies 

    num_of_enemies += 1

    num_of_enemies = 6 if (num_of_enemies >= 6) else 5

    enemies_speed += 0.08

    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('img/meteor.png'))
        enemyX.append(random.randint(120, width - 120))
        enemyY.append(random.randint(-100, 100))
        print(str(enemyY[-1]))
        enemyX_change.append(enemies_speed)
        enemyY_change.append(40)

    next_level_text(level)

    wait()

    # probably should improve this ^^
    # because the level is set +1 before showing the questionaire
    # this if case is needed
    if level in [2, 3, 4, 5, 0]:

        if level == 0:
            new_level = 6

            questionaire_text()
            count_numbers(new_level)
            questionaire_text()
            count_numbers(new_level)
            questionaire_text()
            count_numbers(new_level)
            questionaire_text()

        else:

            questionaire_text()
            count_numbers(level)
            questionaire_text()
            count_numbers(level)
            questionaire_text()
            count_numbers(level)
            questionaire_text()

    wait()

    # reset score
    score_value = 0

    # reset timer
    pygame.time.set_timer(level_time, 60000)
    gsr_time = time.time()

spacePressedTime = 0 

# waits and stops sound until space is pressed
def wait():
    global spacePressedTime
    mixer.pause()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spacePressedTime = time.time()
                mixer.unpause()
                return
            if event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    quit()

# Repeatly set timer for the freezing events, time in milliseconds
# pygame.time.set_timer(freeze_event, 3000)

def show_startscreen():
    over_text = over_font.render("Help! The dinosaurs are in danger.", True, (255, 255, 255))
    screen.blit(over_text, (400, 150))
    over_text = over_font.render("Meteorites are coming down.", True, (255, 255, 255))
    screen.blit(over_text, (400, 250))
    over_text = over_font.render("Use ''a'' to move left and ''d'' to move right.", True, (255, 255, 255))
    screen.blit(over_text, (400, 350))
    over_text = over_font.render("Clicking the left mousebutton fires a ", True, (255, 255, 255))
    screen.blit(over_text, (400, 450))
    over_text = over_font.render("destroying fireball.", True, (255, 255, 255))
    screen.blit(over_text, (400, 550))  
    over_text = over_font.render("Press ''space'' to start.", True, (255, 255, 255))
    screen.blit(over_text, (400, 650))
    pygame.display.update()

    wait()

# Game Loop
running = True
#define starttime to prevent errors if in first level no key is pressed
startTime = time.time()
pressedTime = datetime.now()

gsr_time = time.time()

while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    # startscreen
    if startscreen:
        show_startscreen()
        startscreen = False
        gsr_time = time.time() # reset time to get better results


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN :

            startTime = time.time()
            pressedTime = datetime.now()

            if event.key == pygame.K_a:
                playerX_change = -5
                
                # starting at level 3 lagging increases with each level
                rand = random.randrange(0,99)
                if (level >= 3) and (rand >= (99 - (3 * level))) and manipulationFunction:
                    lag_right = lagging(pygame.K_d)
                    #print('lagged ' + str(lag_right))
                    playerX_change = lag_right

            if event.key == pygame.K_d:
                playerX_change = 5

                rand = random.randrange(0,99)
                if (level >= 3) and (rand >= (99 - (3 * level))) and manipulationFunction:
                    #print('lagged')
                    playerX_change = lag_left
                    lag_left = lagging(pygame.K_a)
            
            # If pressed key is ESC quit program
            if event.key == pygame.K_ESCAPE:
                quit()

        # PRINTING KEYS AND GENERATING THE CSV
        elif event.type == pygame.KEYUP:
            durationOfTime = time.time() - startTime 
            spaceDurationOfTime = time.time() - spacePressedTime 
            k = event.key
            keyName = pygame.key.name(k)

            if event.key == pygame.K_SPACE:
                released_key = [{'value': keyName, 'time [s]': spaceDurationOfTime, 'pressed': str(pressedTime), 'playerX_change': playerX_change}]
                print("You pressed", keyName, "for", spaceDurationOfTime, 'seconds')
            else:
                released_key = [{'value': keyName, 'time [s]': durationOfTime, 'pressed': str(pressedTime), 'playerX_change': playerX_change}]
                print("You pressed", keyName, "for", durationOfTime, 'seconds')
            
            if level != 0:
                writeKeysToCsv(released_key, ['value','time [s]', 'pressed', 'playerX_change'], "pressedKeys", name, manipulation, level)

            playerX_change = 0
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if bullet_state == "ready":
                bulletSound = mixer.Sound("sounds/fireball.wav")
                bulletSound.play()
                # Get the current x cordinate of the spaceship
                bulletX = playerX + 15
                fire_bullet(bulletX, bulletY)
        elif event.type == freeze:
            freezing()

        # timer that aborts level after certain time
        elif event.type == level_time:
            print('time was up')
            next_level()

        #if event.type == pygame.KEYUP:

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= width - 110:
        playerX = width - 110

    # Enemy Movement
    
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > height - 100:

            live_value = live_value - 1
            enemyY[i] = -1 # set enemie out of this condition 

            if live_value < 1:
                
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                #game_over_text()
                #break
                next_level()

        if level == 0:           
            game_over_text()
            mixer.pause()
            break

        # enemy moves only vertically
        enemyY[i] += enemyX_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("sounds/explosion.wav")
            explosionSound.set_volume(0.6)
            explosionSound.play()
            bulletY = 480 *2 
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(120, width - 120)
            enemyY[i] = random.randint(0, 10)

            #maybe add more enemies here rather than in the update level art? maybe have a max?

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480 * 2
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    show_level(levelX, levelY)
    show_lives(liveX, liveY)
    pygame.display.update()
    
    # Obtain Mouse values
    tmp_time = time.time()
    try:
        #print("grs try")
        if driver.execute_script(gsr_script) != gsr:
            gsr = driver.execute_script(gsr_script)
            gsr_list.append({'Time [s]': time.time() - gsr_time, 'GSR': gsr, 'actual_time': datetime.now()})
            #gsr_list_time.append(time.time() - gsr_time)
            #print(gsr)
        if driver.execute_script(hr_script) != hr or (time.time() - tmp_time >= 1):
            hr = driver.execute_script(hr_script)
            hr_list.append({'Time [s]': time.time() - gsr_time, 'HR': hr, 'actual_time': datetime.now()})
            tmp_time = time.time() - gsr_time
            #hr_list_time.append(time.time() - gsr_time)
        # writeGSRToCsv(gsr_list)
        # writeHRToCsv(hr_list)
    except:
        pass

# # input of the name via terminal like: python main.py your_name
# try:
#     name = sys.argv[1]
# except:
#     name = 'No_name'
# score_list.append({'Name': str(name), 'Score': score_value})

#writeScoreToCsv(score_list, ['Name','Score'], "scores.csv")
