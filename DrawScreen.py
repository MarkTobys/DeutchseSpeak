import pygame as pg
import textwrap
pg.font.init()
pg.init()

#updates the current character being displayed, if string is empty no charater is displayed
def changeChar(script, scriptloc):
    if script[scriptloc] != "none":
        dispChar = pg.image.load("images/characters/"+script[scriptloc])
        return dispChar

#draws a character to the screen
def draw_character(win, bg, dispChar, speaking, width, height, scaling):
    # clear screen
    if dispChar != None and scaling == True:
        charSize_x = dispChar.get_width()
        charSize_Y = dispChar.get_height()
        dispChar = pg.transform.scale(dispChar, (charSize_x/2, charSize_Y/2))
    win.blit(bg, (0, 0))
    if dispChar != None and speaking == False:
         win.blit(dispChar, get_center(dispChar, width, height))

#gets the center coordinates of an image
def get_center(image, width, height):
    image_rect = image.get_rect()
    center_x = width // 2
    center_y = height // 2
    image_rect.center = (center_x, center_y)
    return image_rect.topleft

#draw dialogue box and script
def draw_script(win, text, font, text_col, width, height, vertSpace):
    #draw text box (surface, colour, x, y, width, height, border radius)
    pg.draw.rect(win, (211, 211, 211), ((width * (1 / 20) / 10), (height / 4) * 3, width * (18 / 20), height / 4),
                 border_radius=30)
    #wrap the text to fit inside the maximum width
    wrapped_text = textwrap.fill(text, width=75)
    # Render the wrapped text
    lines = wrapped_text.split('\n')
    y_offset = (height / 4) * 3
    for line in lines:
        img = font.render(line, True, text_col)
        text_rect = img.get_rect()
        text_rect.topleft = (15, y_offset)
        win.blit(img, text_rect)
        y_offset += text_rect.height + vertSpace  #adjust the vertical spacing as needed
    pg.display.update()

#draw text to anywhere on the screen
def draw_text(win, text, font, colour, loc, wrapping, width, height):
    wrapped_text = textwrap.fill(text, width=wrapping)
    #render the wrapped text
    lines = wrapped_text.split('\n')
    y_offset = (height / 4) * 3
    for line in lines:
        img = font.render(line, True, colour)
        text_rect = img.get_rect()
        text_rect.topleft = (loc)
        win.blit(img, text_rect)
        y_offset += text_rect.height + 30  #adjusts gaps between text lines
    pg.display.update()


