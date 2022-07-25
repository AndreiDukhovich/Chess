import pygame 
all_sprites = pygame.sprite.Group()


class Figure(pygame.sprite.Sprite):
    figures = []
    del_figure = 0
    def __init__(self, position, img, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.color = color
        self.rect.center = position
        self.first_move = True
        self.over_color = False
        self.to_move = ()
        self.moves = []

    def is_figure_on_way(self, x, pawn=False):
        if (140 >= x[0] or x[0] >= 700) or (60 >= x[1] or x[1] >= 620):
            return True
        for figure in Figure.figures:
            if x == figure.rect.center:
                if self.color != figure.color:
                    self.over_color = True
                    if pawn:
                        return True
                elif self.color == figure.color:
                    return True
        return False

    def is_possible_move(self, click):
        for move in self.moves:
            if move[0]-35 <= click[0] <= move[0]+35 and move[1]-35 <= click[1] <= move[1]+35:
                self.to_move = move
                return True
        return False

    def update(self, finish):
        index = -1
        if self.is_possible_move(finish):
            for i in range(len(Figure.figures)):
                if self.to_move == Figure.figures[i].rect.center and self.color != Figure.figures[i].color:
                    index = i
                elif self.to_move == Figure.figures[i].rect.center and self.color == Figure.figures[i].color:
                    return 
            if index >= 0:
                Figure.figures[index].kill()
                del Figure.figures[index]  
            self.first_move = False
            self.rect.move_ip(self.to_move[0]-self.rect.center[0], self.to_move[1]-self.rect.center[1])
            Figure.rotate()
            Figure.update_moves([0, 1])

    def make_move_but_not(self, finish, color):
        index = -1
        for i in range(len(Figure.figures)):
            if finish == Figure.figures[i].rect.center and self.color != Figure.figures[i].color:
                index = i
        if index >= 0:
            Figure.del_figure = Figure.figures[index]
            del Figure.figures[index]  
        self.rect.move_ip(finish[0]-self.rect.center[0], finish[1]-self.rect.center[1])
        Figure.update_moves([0 if color else 1])
    
    def remake_move(self, old_location, color):
        if Figure.del_figure:
            Figure.figures.append(Figure.del_figure)
        self.rect.move_ip(old_location[0]-self.rect.center[0], old_location[1]-self.rect.center[1])
        Figure.update_moves([0 if color else 1])
        Figure.del_figure = 0

    def choise_figure(self, screen):
        for i in self.rect.center, *self.moves:
            move = pygame.Rect(i[0]-35, i[1]-35, 70, 70)
            pygame.draw.rect(screen, (200, 200, 200), move)
            pygame.draw.rect(screen, (79, 79, 79), move, 3)
    
    def rotate_figure(self):
        self.rect.center = (840-self.rect.center[0], 680-self.rect.center[1])

    @classmethod
    def what_if(cls, color):
        flag = True
        for figure in filter(lambda x: x.color == color, cls.figures):
            now_location = figure.rect.center
            possible_moves = figure.moves
            figure.moves = []
            for possible_move in possible_moves:
                figure.make_move_but_not(possible_move, color)
                if not cls.figures[color].check():
                    figure.moves.append(possible_move)
                    flag = False
                figure.remake_move(now_location, color)
        return flag

    @classmethod
    def update_moves(cls, colors):
        for color in colors:
            for figure in filter(lambda x: x.color == color, cls.figures):
                figure.possible_moves()

    @classmethod
    def rotate(cls):
        for figure in cls.figures:
            figure.rotate_figure()


class Pawn(Figure):

    def __init__(self, position, img, color):
        super().__init__(position, img, color)
        self.possible_moves()

    def possible_moves(self):
        self.moves = []
        d = -1
        r = 3 if self.first_move else 2
        for i in range(1, r):
                x = (self.rect.center[0], self.rect.center[1]+70*d*i)
                if self.is_figure_on_way(x, pawn=True):
                    self.over_color = False
                    break
                self.moves.append(x)
        for i in [-1, 1]:
            x = (self.rect.center[0]+70*i, self.rect.center[1]+70*d)
            self.is_figure_on_way(x)
            if self.over_color:
                self.moves.append(x)
                self.over_color = False

    def update(self, finish):
        super().update(finish)
        if self.rect.center[1] in (75, 565):
            index = Figure.figures.index(self)
            Figure.figures[index].kill()
            Figure.figures[index] = Queen(self.rect.center, f'{self.color}_queen.png', self.color)
            all_sprites.add(Figure.figures[index])


class Knight(Figure):

    def __init__(self, position, img, color):
        super().__init__(position, img, color)
        self.possible_moves()

    def possible_moves(self):
        self.moves = []
        for dx, dy in zip([1, -1, 1, -1], [-1, 1, 1, -1]):
            for cx, cy in zip([140, 70], [70, 140]):
                x = (self.rect.center[0]+dx*cx, self.rect.center[1]+dy*cy)
                if self.is_figure_on_way(x):
                    continue
                self.moves.append(x)
    

class King(Figure):
    def __init__(self, position, img, color):
        super().__init__(position, img, color)
        self.on_check = False
        self.on_mate = False

    def is_unpossible_castling(self, x):
        for figure in Figure.figures:
            if x == figure.rect.center:
                if self.color == figure.color and isinstance(figure, Rook) and figure.first_move:
                    self.fields.append(1)
                else:
                    self.fields.append(2)
            else:
                self.fields.append(0)
                
    def possible_moves(self):
        self.moves = []
        for dx, dy in zip([1, -1, 1, -1], [-1, 1, 1, -1]):
            x = (self.rect.center[0]+70*dx, self.rect.center[1]+70*dy)
            if self.is_figure_on_way(x):
                continue
            self.moves.append(x)
        for dx, dy in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
            x = (self.rect.center[0]+70*dx, self.rect.center[1]+70*dy)
            if self.is_figure_on_way(x):
                continue
            self.moves.append(x)
        if self.first_move and not self.check():
            for dx in [1, -1]:
                self.fields = []
                for i in range(1, 5):
                    x = (self.rect.center[0]+70*dx*i, self.rect.center[1])
                    self.is_unpossible_castling(x)
                if sum(self.fields) == 1:
                    self.moves.append((self.rect.center[0]+140*dx, self.rect.center[1]))

    def check(self):
        for figure in filter(lambda x: x.color != self.color, Figure.figures):
            if self.rect.center in figure.moves:
                self.on_check = True
                return True
        return False

    def mate(self):
        if self.moves == []:
            return True

    def update(self, finish):
        target_rook = self.to_move[0]-self.rect.center[0]
        super().update(finish)
        if abs(target_rook) == 140:   
            for figure in filter(lambda x: x.color == self.color, Figure.figures):
                if isinstance(figure, Rook) and figure.rect.center[0]-self.rect.center[0] <= target_rook:
                    figure.update((self.rect.center[0]-70*target_rook/abs(target_rook), self.rect.center[1]))
            

class Bishop(Figure):

    def possible_moves(self):
        self.moves = []
        for dx, dy in zip([1, -1, 1, -1], [-1, 1, 1, -1]):
            self.over_color = False
            for i in range(1, 8):
                x = (self.rect.center[0]+70*i*dx, self.rect.center[1]+70*i*dy)
                if self.is_figure_on_way(x):
                   self.over_color = False
                   break
                self.moves.append(x)
                if self.over_color:
                    break


class Rook(Figure):

    def possible_moves(self):
        self.moves = []
        for dx, dy in zip([-1, 1, 0, 0], [0, 0, 1, -1]):
            self.over_color = False
            for i in range(1, 8):
                x = (self.rect.center[0]+70*i*dx, self.rect.center[1]+70*i*dy)
                if self.is_figure_on_way(x):
                    self.over_color = False
                    break
                self.moves.append(x)
                if self.over_color:
                    break


class Queen(Rook, Bishop):
    
    def possible_moves(self):
        Rook.possible_moves(self)
        moves = self.moves
        Bishop.possible_moves(self)
        self.moves.extend(moves)


def create_figure():
    figure_class = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    Figure.figures.append(King((455, 95), '0_king.png', 0))
    Figure.figures.append(King((455, 585), '1_king.png', 1))
    Figure.figures.extend([Pawn((175+70*i, 165), 'b_pawn.png', 0) for i in range(8)])
    Figure.figures.extend([Pawn((175+70*i, 515), 'w_pawn.png', 1) for i in range(8)])
    y = [95, 585]
    for j in range(2):
        x = 175
        for i in figure_class:
            if i != King:
                Figure.figures.append(i((x, y[j]), f'{str(j)}_{i.__name__.lower()}.png', j))
            x += 70
