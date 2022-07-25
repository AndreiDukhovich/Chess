import pygame
from figures import Figure, all_sprites, create_figure
from pygame.locals import *
pygame.init()
move = Rect(0, 0, 0, 0)
width = 840
height = 680
background = (0, 0, 0)
color = [(0, 0, 0), (255, 255, 255)]
mate = False
screen = pygame.display.set_mode(((width, height)))
icon = pygame.image.load('icon.ico')
pygame.display.set_icon(icon)
pygame.display.set_caption('Chess')

font = pygame.font.SysFont('arial', 72)
mate_text = ''
place = (0, 0)

class Game_board(Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        board_y = top
        board_x = left
        dx = 0
        dy = 0
        for x in range(8):
            for y in range(8):
                color = (0, 0, 0)
                if (x+y)%2==0:
                    color = (255, 255, 255)
                cell = Rect(board_x+dx, board_y+dy, 70, 70)
                pygame.draw.rect(screen, color, cell)
                dy += height/8
            dx += width/8
            dy = 0


player_index = 1
index_figure = -1
running = True
sysfont = pygame.font.get_default_font()
clock=pygame.time.Clock()

def new_game():
    Figure.figures = []
    all_sprites.empty()
    create_figure()
    all_sprites.add(*Figure.figures)
    return False
    
new_game()
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        if event.type == MOUSEBUTTONDOWN:
            if not mate:
                if index_figure >= 0:
                    if Figure.figures[index_figure].is_possible_move(event.pos):
                        Figure.figures[index_figure].update(event.pos)
                        Figure.what_if(1-player_index) 
                        if Figure.figures[1-player_index].check():
                            if Figure.figures[1-player_index].mate(): 
                                mate = True
                                mate_text = font.render(f'{"Black" if player_index else "Wite"} lost.', True, (255, 0, 0))
                                press_text =  font.render('Press Space for new game.', True, (255, 0, 0))
                                place_mate = mate_text.get_rect(center=(420, 304))
                                place_text = press_text.get_rect(center=(420, 376))

                        player_index = 1-player_index
                    index_figure = -1
                    continue
                for i in range(len(Figure.figures)):
                    if Figure.figures[i].rect.collidepoint(event.pos) and Figure.figures[i].color == player_index:
                        index_figure = i
                        break
                    else:
                        index_figure = -1 
        if event.type == KEYUP and event.key == 32 and mate:
            mate = new_game()
            player_index = 1
                
    screen.fill(1)
    playboard = Game_board(140, 60, 560, 560)
    pygame.draw.rect(screen, (255, 255, 255), playboard, 2)
    if index_figure >= 0:
        Figure.figures[index_figure].choise_figure(screen)
    all_sprites.draw(screen)
    if mate:
        screen.blit(mate_text, place_mate)
        screen.blit(press_text, place_text)
    pygame.display.update() 
        
pygame.quit()