import pygame
from pygame.locals import *

'''Uma série de objetos utilizados no jogo.'''

class Bird:

    '''Classe com atributos do pássaro - o jogador.'''

    def __init__(self, pos, frames, gravity=0.5, groundPointY=476):

        self.activated = False
        self.pos = list(pos)
        self.animFrame = 0
        self.ySpeed = 0
        self.isJumping = False
        self.frames = list(frames)
        self.angle = 0
        self.colliding = list()
        self.gravity = gravity
        self.hitboxSize = self.frames[0].get_rect().size
        self.groundPointY = groundPointY
        self.isDead = False
        self.angle = 0
        self.jumpCounter = 0
        self.rotateTarget = 0

    def manage(self):
        
        '''Uma função que automaticamente roda as funções que são verificadas a cada frame.'''
        if self.activated: self.movement()

    def render(self):

        if self.activated:
            self.jumpCounter += 1

        if self.isJumping:
            self.animFrame += 1
            if self.animFrame >= 2:
                self.isJumping = False
                self.animFrame = 0
            self.jumpCounter = 0

        if self.isDead:
            self.activated = False
            self.animFrame = 3

        if not self.isDead:

            # Achar ângulo
            if self.isJumping: self.rotateTarget = 30
            if self.jumpCounter >= 30: self.rotateTarget = -60

            # Girar o pássaro
            self.angle += (self.rotateTarget - self.angle) * 0.15

            self.rotateTarget = (self.rotateTarget + 360) % 360

        # Atualizar o ang. do pássaro
        old_center = (self.pos[0] + 15, self.pos[1] + 15)
        new_img = pygame.transform.rotate(self.frames[self.animFrame], self.angle)
        rect = new_img.get_rect()
        rect.center = old_center

        return (new_img, rect)

    def movement(self):

        '''Executa as rotinas de movimento de (supostamente) cada frame.'''

        self.pos[1] += self.ySpeed
        self.ySpeed += self.gravity

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.ySpeed = 0
        elif self.pos[1] >= ((self.groundPointY) - self.hitboxSize[1]):
            self.pos[1] = ((self.groundPointY) - self.hitboxSize[1])
            self.ySpeed = 0
            self.isDead = True

    def hitbox(self):
        
        rect = self.frames[0].get_rect().size
        return tuple(self.pos) + rect

class Pipe:

    '''Código relacionado ao cano.'''

    def __init__(self, pos, frames, speed=[-1]):
        self.pos = list(pos)
        self.frames = list(frames)
        self.hitboxSize = self.frames[0].get_rect().size
        if len(speed) != 1: raise ValueError('The speed list should only contain one element.')
        else: self.speed = speed

    def manage(self):
        
        # Atualizar a posição
        self.pos[0] += 2 * self.speed[0]

    def hitbox(self):

        rect = self.frames[0].get_rect().size
        return tuple(self.pos) + rect

    def render(self):
        return (self.frames[0], self.pos)

class RepeatingTile:

    def __init__(self, pos, frames, speed=[-1]):
        self.pos = list(pos)
        self.frames = list(frames)
        self.speed = speed

    def manage(self):
        self.pos[0] += self.speed[0]

    def render(self):
        return (self.frames[0], self.pos)

