import pygame as pg
import button
import pygame.draw
import speech_recognition as sr
import DrawScreen as ds
import importScripts
from win32api import GetSystemMetrics
import os

pg.font.init()
pg.init()
screenWidth = GetSystemMetrics(0)

#create game window and set variables
if (screenWidth >= 1800):
    width = 1720
    height = 900
    text_font = pygame.font.SysFont("Arial", 50)
    subheading_font = pygame.font.SysFont("Arial", 100)
    heading_font = pygame.font.SysFont("Arial", 200)
    imageScale = False
    vertSpace = 10
else:
    width = 1000
    height = 510
    text_font = pygame.font.SysFont("Arial", 30)
    subheading_font = pygame.font.SysFont("Arial", 50)
    heading_font = pygame.font.SysFont("Arial", 100)
    imageScale = True
    vertSpace = 5

win = pg.display.set_mode((width, height))
pg.display.set_caption("DeutscheSpeak")

#Load global image assets and variables
mic1 = pg.image.load("images/assets/mic_unpressed.png").convert_alpha()
mic2 = pg.image.load("images/assets/mic_pressed.png").convert_alpha()
next1 = pg.image.load("images/assets/next_unpressed.png").convert_alpha()
next2 = pg.image.load("images/assets/next_pressed.png").convert_alpha()
prev1 = pg.image.load("images/assets/prev_unpressed.png").convert_alpha()
prev2 = pg.image.load("images/assets/prev_pressed.png").convert_alpha()
quit1 = pg.image.load("images/assets/quit_unpressed.png").convert_alpha()
quit2 = pg.image.load("images/assets/quit_pressed.png").convert_alpha()
select1 = pg.image.load("images/assets/select_unpressed.png").convert_alpha()
select2 = pg.image.load("images/assets/select_pressed.png").convert_alpha()

if imageScale == True:
    mic1 = pygame.transform.scale(mic1, (mic1.get_width() * 0.6, mic1.get_height() * 0.6))
    mic2 = pygame.transform.scale(mic2, (mic2.get_width() * 0.6, mic2.get_height() * 0.6))
    next1 = pygame.transform.scale(next1, (next1.get_width() * 0.6, next1.get_height() * 0.6))
    next2 = pygame.transform.scale(next2, (next2.get_width() * 0.6, next2.get_height() * 0.6))
    prev1 = pygame.transform.scale(prev1, (prev1.get_width() * 0.6, prev1.get_height() * 0.6))
    prev2 = pygame.transform.scale(prev2, (prev2.get_width() * 0.6, prev2.get_height() * 0.6))
    quit1 = pygame.transform.scale(quit1, (quit1.get_width() * 0.6, quit1.get_height() * 0.6))
    quit2 = pygame.transform.scale(quit2, (quit2.get_width() * 0.6, quit2.get_height() * 0.6))
    select1 = pygame.transform.scale(select1, (select1.get_width() * 0.6, select1.get_height() * 0.6))
    select2 = pygame.transform.scale(select2, (select2.get_width() * 0.6, select2.get_height() * 0.6))

#load SFX
click = pygame.mixer.Sound("Audio/SFX/text-click.wav")

#create speak button
speak_button = button.Button(mic1, mic2)
next_button = button.Button(next1, next2)
prev_button = button.Button(prev1, prev2)
select_button = button.Button(select1, select2)
quit_button = button.Button(quit1, quit2)

#load script (level select functionality to be added)
def readScript(scriptPath):
    file = open("Scripts/"+scriptPath, 'r')
    script = []
    for line in file:
        line = line.strip()
        script.append(line)
    file.close()
    return script

def TranscribeAudio(transcript):
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    # Speech recognition using Google Speech Recognition
    try:
        audioText = r.recognize_google(audio, language="de-DE")
        audioText = audioText.lower()
    except sr.UnknownValueError:
        return -1
    except sr.RequestError as e:
        return -1
    if (audioText.find(transcript) != -1):
        return 1
    else:
        return 0

    # #testing purposes
    # pygame.time.wait(100)
    # return -1

#Visual novel loop
def runGame(scriptPath):
    #load level information
    script = readScript(scriptPath)
    pygame.mixer.music.load(script[0])
    bg = pg.image.load(script[1]).convert_alpha()
    if imageScale == True:
        bg = pygame.transform.scale(bg, (bg.get_width() * 0.6, bg.get_height() * 0.6))
    else:
        bg = pygame.transform.scale(bg, (width, height))
    scriptloc = 3
    game_running = True
    pygame.mixer.music.play(fade_ms=5000)
    #initialise screen
    win.blit(bg, (0, 0))
    ds.draw_script(win, script[scriptloc], text_font, (0, 0, 0), width, height, vertSpace)
    pg.display.update()
    #initialise assets
    # speaking game variables
    speaking = False
    passedGame = True
    speechClip = None
    transcript = ""
    winPhrase = ""
    winGraphic = None
    failPhrase = ""
    failGraphic = None
    dispChar = None
    while game_running:
        if speaking == False:
            next_button.draw(win, width * (19 / 20), height * (18 / 20))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pygame.mixer.music.fadeout(1000)
                game_running = False
                #go back in script, for testing purposes
            # if event.key == pygame.K_LEFT and speaking != True:
            #     if scriptloc > 3:
            #         pygame.mixer.Sound.play(click)
            #         scriptloc -= 1
            #         ds.draw_character(win, bg, dispChar, speaking)
            #         ds.draw_script(win, script[scriptloc], text_font, (0, 0, 0))
            ##Code to initiate and run the speech minigame
            if event.type == pg.MOUSEBUTTONDOWN and speaking != True:
                if scriptloc < len(script) - 1:
                    pygame.mixer.Sound.play(click)
                    scriptloc += 1
                    if passedGame == False:
                        speaking = True
                        passedGame = True
                    if script[scriptloc] == "##%":
                        # change character
                        if script[scriptloc + 1] == "char":
                            scriptloc += 2
                            dispChar = ds.changeChar(script, scriptloc)
                            scriptloc += 2
                        # load variables for speaking minigame
                        elif script[scriptloc + 1] == "speak":
                            speechClip = pygame.mixer.Sound("Audio/voice_clips/" + script[scriptloc + 2])
                            transcript = script[scriptloc + 4]
                            winPhrase = script[scriptloc + 5]
                            winGraphic = ds.changeChar(script, scriptloc + 6)
                            failPhrase = script[scriptloc + 7]
                            failGraphic = ds.changeChar(script, scriptloc + 8)
                            speaking = True
                            pygame.mixer.music.fadeout(500)
                            pygame.mixer.Sound.play(speechClip)
                            scriptloc += 3
                    # update screen
                    ds.draw_character(win, bg, dispChar, speaking, width, height, imageScale)
                    ds.draw_script(win, script[scriptloc], text_font, (0, 0, 0), width, height, vertSpace)
                else:
                    pygame.mixer.music.fadeout(500)
                    game_running = False
        if speak_button.clicked == True:
            audiodata = TranscribeAudio(transcript)
            ##if the player passes the test, the script progresses
            if audiodata == 1:
                speak_button.clicked = False
                speaking = False
                scriptloc += 6
                dispChar = winGraphic
                ds.draw_character(win, bg, winGraphic, speaking, width, height, imageScale)
                ds.draw_script(win, winPhrase, text_font, (0, 0, 0), width, height, vertSpace)
                pygame.mixer.music.play(fade_ms=5000)
            elif audiodata == 0:
                speak_button.clicked = False
                speaking = False
                passedGame = False
                scriptloc -= 1
                ds.draw_character(win, bg, failGraphic, speaking, width, height, imageScale)
                ds.draw_script(win, failPhrase, text_font, (0, 0, 0), width, height, vertSpace)
            elif audiodata == -1:
                speak_button.clicked = False
                speaking = False
                passedGame = False
                scriptloc -= 1
                speak_button.draw(win, width / 2, height * (3 / 8))
                next_button.draw(win, width * (19 / 20), height * (18 / 20))
                ds.draw_script(win, "Try again, speaking slower and clearer into the microphone", text_font,
                               (0, 0, 0), width, height, vertSpace)
        if speaking == True:
            speak_button.draw(win, width/2, height*(3/8))
            pg.display.update()
        pg.display.update()
    return

#draw the level select screen
def levelSelect():
    selected = False
    select_button.clicked = False
    next_button.clicked = False
    prev_button.clicked = False
    loc = 0
    scripts, backgrounds = importScripts.getScripts()
    numScripts = len(scripts)
    while(selected == False):
        bg = pg.image.load("Scripts/" + backgrounds[loc]).convert_alpha()
        if imageScale == True:
            bg = pygame.transform.scale(bg, (bg.get_width()*0.6, bg.get_height()*0.6))
        else:
            bg = pygame.transform.scale(bg, (width, height))
        levelname = scripts[loc].split('/', 1)[-1].replace('.txt', '')
        win.blit(bg, (0, 0))
        ds.draw_text(win, levelname, subheading_font, (0, 0, 0), (60, 10), 100, width, height)
        next_button.draw(win, width * (19 / 20), height * (3 / 4))
        prev_button.draw(win, width * (1 / 20), height * (3 / 4))
        select_button.draw(win, width/2, height * (3 / 4))
        pg.display.update()
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                return True, ""
        if next_button.clicked == True and loc < numScripts - 1:
            pygame.mixer.Sound.play(click)
            loc += 1
        if prev_button.clicked == True and loc > 0:
            pygame.mixer.Sound.play(click)
            loc -= 1
        if select_button.clicked == True:
            selected = True
    return False, scripts[loc]

#draw the title screen
def mainScreen():
    start = False
    title_screen = pg.image.load("images/background_images/german-flag-cropped-watermark.png").convert_alpha()
    title_screen = pygame.transform.scale(title_screen, (width, height))
    while start == False:
        win.blit(title_screen, (0,0))
        ds.draw_text(win, "DeutscheSpeak", heading_font, (225, 225, 225 ), (50,0), 100, width, height)
        pg.display.update()
        for event in pygame.event.get():
            if event.type == pg.QUIT:
                return True
            if event.type == pg.MOUSEBUTTONDOWN:
                start = True
    return False

#game loop logic
if __name__ == '__main__':
    quit = mainScreen()
    finished = False
    if quit != True:
        while (finished == False):
            finished, scriptPath = levelSelect()
            if (finished == False):
                runGame(scriptPath)

