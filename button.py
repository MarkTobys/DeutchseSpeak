import pygame as pg
class Button():
    def __init__(self, image, hoverImage):
        self.image = image
        self.hoverImage = hoverImage
        self.rect = self.image.get_rect()
        self.clicked = False

    #surface to draw on, x and y location of button
    def draw(self, win, x, y):
        #set button's rect center to x,y coords
        self.rect.center = (x, y)
        #get mouse position
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            win.blit(self.hoverImage, self.rect.topleft)
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
        else:
            win.blit(self.image, self.rect.topleft)


        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw button on screen



