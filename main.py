from numpy import array, zeros, flip
from random import randint


class KeyMap(dict):
    def get_in_list(self, value):
        for k, v in self.items():
            if value in k:
                return v
        return None


class Mapa:
    def __init__(self, y, x):
        self.size = (x, y)
        self.size_grid = (x + 2, y + 2)
        self.grid = zeros(self.size_grid)

    def mapa(self):
        return self.grid[1:-1, 1:-1]

    def update(self, positions):
        self.grid = zeros(self.size_grid)
        for i, position in enumerate(positions):
            self.grid[tuple(position)] = 1
            if i == len(positions)-1:
                self.grid[tuple(position)] = 2

    def spot(self):
        spots = []
        for x, colum in enumerate(self.mapa(), start=1):
            for y, cell in enumerate(colum, start=1):
                if cell == 0:
                    spots.append(array([x, y]))
        return spots


class Cobra:
    def __init__(self):
        self.body = [array([1, 1])]
        self.velocity = array([0, 1])

    def change_velocity(self, direction):
        velocity = {
            'w': array([-1, 0]),
            's': array([1, 0]),
            'd': array([0, 1]),
            'a': array([0, -1])
        }
        if (self.velocity + velocity[direction] != array([0, 0])).any():
            self.velocity = velocity[direction]

    def move(self):
        self.body.append(self.body[-1]+self.velocity)
        del self.body[0]

    def grow(self):
        self.body.insert(0, self.body[0])


class CobrinhaJogo:
    def __init__(self, mapa=Mapa(5, 5), cobra=Cobra()):
        self.score = 0
        self.item = None
        self.mapa: Mapa = mapa
        self.cobra: Cobra = cobra
        self.mapa.update(self.cobra.body)
        self.spawn_item()

        self.keymap: KeyMap = KeyMap()
        self.keymap[('s', 'w', 'a', 'd')] = self.cobra.change_velocity

    def spawn_item(self):
        if self.mapa.spot():
            self.item: array = self.mapa.spot()[randint(0, len(self.mapa.spot())-1)]

    def pick_item(self):
        self.cobra.grow()
        self.spawn_item()
        self.score += 1

    def input_keyboard(self):
        choice = input().strip().lower()
        if self.keymap.get_in_list(choice):
            self.keymap.get_in_list(choice)(choice)

    def timeout(self):
        self.cobra.move()
        self.mapa.update(self.cobra.body)
        print(self.mapa.mapa())

    def play(self):
        print(self.mapa.mapa())

        while True:
            print('-' * 100)
            print(f'Item:{flip(self.item)}      Score: {self.score}')
            print('-' * 100)

            self.input_keyboard()

            self.timeout()

            if self.mapa.mapa().sum() != len(self.cobra.body)+1:
                print(f'{"Game Over":-^100}')
                print(f'Score: {self.score}')
                print('-' * 100)
                break

            if (self.cobra.body[-1] == self.item).all():
                self.pick_item()

            if self.score == self.mapa.size[0]*self.mapa.size[1]:
                print(f'{"WIN":-^100}')
                print(f'Score: {self.score}')
                print('-' * 100)
                break


game = CobrinhaJogo()
game.play()
