import pygame

class Piece(pygame.Surface):
    def __init__(self, image, x_pos=-200, y_pos=-200):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = image.get_height()
        self.width = image.get_width()
        self.rect = pygame.Rect(x_pos, y_pos, image.get_width(), image.get_height())
        self.selected = False
        self.inserted = False

    def move(self, x, y):
        self.x_pos = x
        self.y_pos = y
        print(f'new pos x : {x} - y : {y}')
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)