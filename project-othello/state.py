from copy import deepcopy

direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]


class State(object):

    def __init__(self):

        self._board = []
        for i in range(0, 8):
            self._board.append([])
            for j in range(0, 8):
                self._board[i].append(0)
        self._board[3][3] = "B"
        self._board[3][4] = "W"
        self._board[4][3] = "W"
        self._board[4][4] = "B"

    def serialize(self):
        niska = ""
        for i in range(0, 8):
            for j in range(0, 8):
                niska += str(self.get_value(i, j)) + ","
        return niska

    def evaluate(self, player):
        # trenutno stanje table evaluira uneki broj
        if self.is_end(player):
            if player == 'W':
                return 1000000
            elif player == 'B':
                return -1000000

        return self.heuristic()

    def get_next_states(self, player):
        possible_directions = self.move_valid(player)
        next_states = []
        for x, y in possible_directions:
            stanje = deepcopy(self.flip_next_state(player, x, y))
            next_states.append((stanje, x, y))

        return next_states

    def get_value(self, i, j):
        return self._board[i][j]

    def set_value(self, i, j, value):
        self._board[i][j] = value

    def __str__(self):
        print("     0   1   2   3   4   5   6   7")
        hor = "   +---+---+---+---+---+---+---+---+\n"
        for i in range(0, 8):
            hor += str(i) + "  |"
            for j in range(0, 8):
                if self._board[i][j] == 0:
                    hor += "   |"
                else:
                    hor += " %s |" % self._board[i][j]
            hor += "\n   +---+---+---+---+---+---+---+---+\n"
        return hor

    def get_score(self):
        b_score = 0
        w_score = 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == "W":
                    w_score += 1
                elif self._board[i][j] == "B":
                    b_score += 1
        return b_score, w_score

    def is_end(self, player):
        end = False
        l = self.move_valid(player)
        if len(l) == 0:
            other_player = self.whoplayer(player)
            m = self.move_valid(other_player)
            if len(m) == 0:
                end = True
        return end

    # funkcija koja proverava da li igrac ima poteza,ako nema predji na sledeceg igraca
    def legal(self, player):
        l = self.move_valid(player)
        if len(l) == 0:
            return True
        return False

    def print_won(self):
        b, w = self.get_score()
        if b > w:
            print("Pobedio je crni igrač.")
        elif w > b:
            print("Pobedio je beli igrač.")
        else:
            print("Nerešeno je.")

    def move_valid(self, player):
        other_player = self.whoplayer(player)
        moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self._board[i][j] == 0:
                    moves.append([i, j])
        valid = []
        validate = []
        for x, y in direction:
            for i, j in moves:
                istart, jstart = i, j
                i += x
                j += y
                if self.on_board(i, j):
                    if self._board[i][j] == other_player:
                        while self.on_board(i, j):
                            if self._board[i][j] == other_player:
                                i += x
                                j += y
                                continue
                            if self._board[i][j] == player:
                                valid.append([istart, jstart])
                                break
                            else:
                                break
        #da ne bi doslo do dupliranja poteza
        for [k, l] in valid:
            if [k, l] not in validate:
                validate.append([k, l])

        return validate

    def flip_next_state(self, value, x, y):
        other_player = self.whoplayer(value)
        self._board[x][y] = value
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if self._board[i][j] != 0:
                    neighbours.append([i, j])
        convert = []

        for n in neighbours:
            ni = n[0]
            nj = n[1]
            if self._board[ni][nj] == other_player:
                # linija za konvertovanje
                path = []

                # smer kretanja
                di = ni - x
                dj = nj - y

                ti = ni
                temp_y = nj
                while 0 <= ti <= 7 and 0 <= temp_y <= 7:
                    path.append([ti, temp_y])
                    color = self._board[ti][temp_y]
                    # ako dodjemo do prazne plocice, ne krecemo se dalje
                    if color == 0:
                        break
                    # Ако дођемо до плочице боје играча, формира се линија
                    if value == color:
                        for p in path:
                            convert.append(p)
                        break
                    # pomeri
                    ti += di
                    temp_y += dj

        tmp_stanje = self

        for p in convert:
            tmp_stanje._board[p[0]][p[1]] = value
        return tmp_stanje

    def to_flip(self, value, x, y):
        other_player = self.whoplayer(value)
        self._board[x][y] = value
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if self._board[i][j] != 0:
                    neighbours.append([i, j])
        convert = []

        for n in neighbours:
            ni = n[0]
            nj = n[1]
            if self._board[ni][nj] == other_player:
                # linija za konvertovanje
                path = []

                # smer kretanja
                di = ni - x
                dj = nj - y

                ti = ni
                temp_y = nj
                while 0 <= ti <= 7 and 0 <= temp_y <= 7:
                    path.append([ti, temp_y])
                    color = self._board[ti][temp_y]
                    # ako dodjemo do prazne plocice, ne krecemo se dalje
                    if color == 0:
                        break
                    # Ако дођемо до плочице боје играча, формира се линија ms ako stignem do zetona
                    if value == color:
                        for p in path:
                            convert.append(p)
                        break
                    # pomeri
                    ti += di
                    temp_y += dj

        for p in convert:
            self._board[p[0]][p[1]] = value
        return self._board

    def whoplayer(self, player):
        if player == "B":
            other_player = "W"
        else:
            other_player = "B"
        return other_player

    def on_board(self, i, j):
        if 0 <= i < 8 and 0 <= j < 8:
            return True
        else:
            return False

    def heuristic(self):
        score = [
            [500, -150, 30, 10, 10, 30, -150, 500],
            [-150, -250, 0, 0, 0, 0, -250, -150],
            [30, 0, 1, 2, 2, 1, 0, 30],
            [10, 0, 2, 16, 16, 2, 0, 30],
            [10, 0, 2, 16, 16, 2, 0, 30],
            [30, 0, 1, 2, 2, 1, 0, 30],
            [-150, -250, 0, 0, 0, 0, -250, -150],
            [500, -150, 30, 10, 10, 30, -150, 500]
        ]

        all_score = 0
        for i in range(8):
            for j in range(8):
                if self._board[i][j] == 'W':
                    all_score += score[i][j]
                elif self._board[i][j] == 'B':
                    all_score -= score[i][j]

        return all_score
