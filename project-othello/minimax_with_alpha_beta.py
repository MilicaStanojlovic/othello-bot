from copy import deepcopy
from state import State
from tree import TreeNode
import time


def max(cvor: TreeNode, player, depth, alpha=float('-inf'), beta=float('inf'), hashMapa=dict()):
    current_state = cvor.data

    if depth == 0 or current_state.is_end('B'):

        serializovano = current_state.serialize()

        if serializovano not in hashMapa:
            hashMapa[serializovano] = current_state.evaluate(player)

        return current_state, hashMapa[serializovano], 0, 0

    curr_max = float('-inf')
    curr_best_move = None
    curr_x = 0
    curr_y = 0

    for next_state, x, y in current_state.get_next_states(player):

        novi_cvor = TreeNode(next_state)
        novi_cvor.parent = cvor
        cvor.add_child(novi_cvor)
        possible_move, vr, _, _ = min(novi_cvor, 'B', depth - 1, alpha, beta, hashMapa)

        if vr > curr_max:
            curr_max = vr
            curr_x = x
            curr_y = y
            curr_best_move = possible_move

        if curr_max >= beta:
            return curr_best_move, curr_max, curr_x, curr_y

        if curr_max > alpha:
            alpha = curr_max

    return curr_best_move, curr_max, curr_x, curr_y


def min(cvor: TreeNode, player, depth, alpha=float('-inf'), beta=float('inf'), hashMapa=dict()):
    current_state = cvor.data

    if depth == 0 or current_state.is_end('W'):

        serializovano = current_state.serialize()
        if serializovano not in hashMapa:
            hashMapa[serializovano] = current_state.evaluate(player)

        return current_state, hashMapa[serializovano], 0, 0

    curr_min = float('inf')
    curr_x = 0
    curr_y = 0
    curr_best_move = None

    for next_state, x, y in current_state.get_next_states(player):
        novi_cvor = TreeNode(next_state)
        novi_cvor.parent = cvor
        cvor.add_child(novi_cvor)

        possible_move, vr, _, _ = max(novi_cvor, 'W', depth - 1, alpha, beta, hashMapa)
        if vr < curr_min:
            curr_min = vr
            curr_x = x
            curr_y = y
            curr_best_move = possible_move

        if curr_min <= alpha:
            return curr_best_move, curr_min, curr_x, curr_y

        if curr_min < beta:
            beta = curr_min

    return curr_best_move, curr_min, curr_x, curr_y


class Game(object):
    __slots__ = ['_current_state', '_player_turn']

    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        # na potezu je crni igrac
        self._current_state = State()
        self._player_turn = 'B'

    def play(self):
        print("Zabavite se uz igru Reversi/Othello!\n")
        print(self._current_state)
        self.initialize_game()
        p = 0
        while True:
            if self._current_state.is_end(self._player_turn):
                self._current_state.print_won()
                break

            if self._player_turn == "B":
                if len(self._current_state.move_valid("B")) == 0:
                    self._player_turn = "W"
                    break
                print("Na potezu ste.")
                print("Ovo su koordinate koje mozete da unesete:")
                for i, j in self._current_state.move_valid("B"):
                    print("\tx=" + str(i) + " " "y= " + str(j))

                x = eval(input("Unesite koordinatu x: "))
                y = eval(input("Unesite koordinatu y: "))

                while not [x, y] in self._current_state.move_valid("B"):
                    print("Niste uneli dobru koordinatu!")
                    x = eval(input("Unesite koordinatu x: "))
                    y = eval(input("Unesite koordinatu y: "))

                self._current_state.to_flip("B", x, y)
                print(self._current_state)
                p += 1
                self._player_turn = "W"
                sc1, sc2 = self._current_state.get_score()
                print("\tIgrac: " + str(sc1) + "\t\t" + "Kompjuter: " + str(sc2))


            else:
                self._player_turn = "W"
                if len(self._current_state.move_valid("W")) == 0:
                    self._player_turn = "B"
                    break
                p += 1
                pocetak = time.time()
                x, y = self.getComputerMove(p)
                self._current_state.to_flip("W", x, y)
                print(self._current_state)
                kraj = time.time() - pocetak
                print("Vreme izvršavanja poteza kompjutera:" + str(kraj))
                sc1, sc2 = self._current_state.get_score()
                print("\tIgrac: " + str(sc1) + "\t\t" + "Kompjuter: " + str(sc2))
                self._player_turn = "B"

    def getComputerMove(self, p):
        depth = self.get_depth(p)
        stanje = deepcopy(self._current_state)
        cvor = TreeNode(stanje)
        next_state, _, x, y = max(cvor, 'W', depth)
        return x, y

    def get_depth(self, p):
        if p < 3:
            depth = 5
        elif p > 54:
            depth = 64 - p
        else:
            depth = 4
        return depth


if __name__ == '__main__':
    g = Game()
    g.play()
