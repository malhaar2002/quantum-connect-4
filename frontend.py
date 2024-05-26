"""
Importing important libraries
"""
import pygame, sys
from client import main
import webbrowser
"""
Setting up an environment to initialize pygame
"""
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Quantum Connect Four')
screen = pygame.display.set_mode((600, 400), 0, 32)  # Adjusted window size to fit all buttons
 
#setting font settings
font = pygame.font.SysFont(None, 30)
 
"""
A function that can be used to write text on our screen and buttons
"""
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
# A variable to check for the status later
click = False
 
# Main container function that holds the buttons and game functions
def main_menu():
    while True:
 
        screen.fill((0,190,255))
        draw_text('Game Options', font, (0,0,0), screen, 250, 40)
 
        mx, my = pygame.mouse.get_pos()

        #creating buttons
        button_1 = pygame.Rect(200, 100, 200, 50)
        button_2 = pygame.Rect(200, 180, 200, 50)
        button_3 = pygame.Rect(200, 260, 200, 50)
        button_4 = pygame.Rect(200, 340, 200, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        if button_3.collidepoint((mx, my)):
            if click:
                education()
        if button_4.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        
    
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        pygame.draw.rect(screen, (255, 0, 0), button_4)
 
        #writing text on top of button
        draw_text('PLAY', font, (255,255,255), screen, 280, 115)
        draw_text('RULES', font, (255,255,255), screen, 270, 195)
        draw_text('GATE GUIDE', font, (255,255,255), screen, 240, 275)
        draw_text('QUIT', font, (255,255,255), screen, 270, 355)


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
"""
This function is called when the "PLAY" button is clicked.
"""
def game():
    running = True
    while running:
        game_over = main()

        if game_over:
            running = False

"""
This function is called when the "OPTIONS" button is clicked.
"""
def options():
    running = True
    webbrowser.open(r'rules.html', new=2)
 
    draw_text('Rules for the game', font, (255, 255, 255), screen, 20, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
       
        pygame.display.update()
        mainClock.tick(60)

def education():
    running = True
    webbrowser.open(r'gate_guide.html', new=2)
 
    draw_text('Know more about Quantum Gates', font, (255, 255, 255), screen, 20, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
       
        pygame.display.update()
        mainClock.tick(60)


main_menu()
