from copy import deepcopy

class Piece:
    def __init__(self, piece, color):
        self.piece = piece
        self.color = color

    def __str__(self):
        if self.piece == 'knight':
            return 'N' if self.color == 1 else 'n'

        if self.color == 1:
            return self.piece[0].upper()
        elif self.color == -1:
            return self.piece[0]
        return '-'
    def __repr__(self):
        return str(self)

    def validate_move(self, move, buff_board):
        return 0<=move[0]<=7 and 0<=move[1]<=7 and buff_board[2 + move[0]][2 + move[1]].color != self.color

class Empty(Piece):
    def __init__(self):
        super().__init__(None, float('inf'))

    def valid_moves(self, pos, buff_board):
        return []

class Pawn(Piece):
    def __init__(self, color=1):
        super().__init__('pawn', color)
        self.prev_move = None

    def valid_moves(self, pos, buff_board):
        moves = []
        #MOVE
        if not buff_board[2 + pos[0]-1][2 + pos[1]].piece:
            moves.append((pos[0]-1, pos[1]))

            if pos[0] == 6 and not buff_board[2 + pos[0]-2][2 + pos[1]].piece:
                moves.append((pos[0]-2, pos[1]))
        
        
        #TAKE
        if buff_board[2 + pos[0]-1][2 + pos[1]-1].color == -1 * self.color:
            moves.append((pos[0]-1, pos[1]-1))
        if buff_board[2 + pos[0]-1][2 + pos[1]+1].color == -1 * self.color:
            moves.append((pos[0]-1, pos[1]+1))
        
        #en passant
        left, right = buff_board[2 + pos[0]][2 + pos[1]-1], buff_board[2 + pos[0]][2 + pos[1]+1]
        if left.color == -1 * self.color and left.piece == 'pawn' and left.prev_move == (pos[0]-2, pos[1]-1):
            moves.append((pos[0]-1, pos[1]-1))
        if right.color == -1 * self.color and right.piece == 'pawn' and right.prev_move == (pos[0]-2, pos[1]+1):
            moves.append((pos[0]-1, pos[1]+1))

        return moves

class Knight(Piece):
    def __init__(self, color=1):
        super().__init__('knight', color)

    def valid_moves(self, pos, buff_board):
        moves = [(pos[0]+i, pos[1]+j) for i in [-2,-1,1,2] for j in [-2,-1,1,2] if abs(i)+abs(j)==3]
        return [move for move in moves if self.validate_move(move, buff_board)]

class Bishop(Piece):
    def __init__(self, color=1):
        super().__init__('bishop', color)

    def valid_moves(self, pos, buff_board):
        moves = []

        for i in [-1,1]:
            for j in [-1,1]:
                for k in range(1,8):
                    if self.validate_move((pos[0]+i*k, pos[1]+j*k), buff_board):
                        moves.append((pos[0]+i*k, pos[1]+j*k))

                        if buff_board[2 + pos[0]+i*k][2 + pos[1]+j*k].color == -1*self.color:
                            break
                    else:
                        break
        return moves
        
class Rook(Piece):
    def __init__(self, color=1):
        super().__init__('rook', color)

    def valid_moves(self, pos, buff_board):
        moves = []

        for i,j in [(1,0),(-1,0),(0,1),(0,-1)]:
            for k in range(1,8):
                if self.validate_move((pos[0]+i*k, pos[1]+j*k), buff_board):
                    moves.append((pos[0]+i*k, pos[1]+j*k))

                    if buff_board[2 + pos[0]+i*k][2 + pos[1]+j*k].color == -1*self.color:
                        break
                else:
                    break

        return moves

class Queen(Piece):
    def __init__(self, color=1):
        super().__init__('queen', color)

    def valid_moves(self, pos, buff_board):
        return Bishop.valid_moves(self, pos, buff_board)+Rook.valid_moves(self, pos, buff_board)

class King(Piece):
    def __init__(self, pos=None, color=1):
        super().__init__('king', color)
        
        if pos:
            if color == 1:
                Chess.white_king_pos = pos
            else:
                Chess.black_king_pos = pos

    def valid_moves(self, pos, buff_board):
        moves = [(pos[0]+i, pos[1]+j) for i in [-1,0,1] for j in [-1,0,1] if not i==j==0]
        return [move for move in moves if self.validate_move(move, buff_board)]




class Chess:
    board = []
    buff_board = []
    abbr = {'N': Knight, 'B': Bishop, 'R': Rook, 'Q': Queen, 'K': King}
    king_pos = {1: (7,4), -1: (0,4)}
    piece_values = {Empty: 0, Pawn: 1, Knight: 3, Bishop: 3, Rook: 5, Queen: 9, King: 0}

    def __init__(self, board=[]):
        self.reset_board(board)

    def reset_board(self, board=[]):
        if len(board) == 0:
            board = [
                [Rook(), Knight(), Bishop(), Queen(), King((0,4)), Bishop(), Knight(), Rook()],
                [Pawn()]*8,
                [Empty()]*8, [Empty()]*8, [Empty()]*8, [Empty()]*8,
                [Pawn()]*8,
                [Rook(), Knight(), Bishop(), Queen(), King((7,4)), Bishop(), Knight(), Rook()]
            ]

            for piece in board[0]+board[1]:
                if piece.piece:
                    piece.color = -1
        
        self.board = board
        self.buff_board = [[Empty()]*12]*2 + [[Empty()]*2 + row + [Empty()]*2 for row in board]+ [[Empty()]*12]*2

    def display_board(self):
        for i in range(8):
            for j in range(8):
                print(self.board[i][j], end='')
            print()

    def display_available_moves(self, pos, piece=None):
        if not piece:
            piece = self.board[pos[0]][pos[1]]
        moves = piece.valid_moves(pos, self.buff_board)

        for i in range(8):
            for j in range(8):
                if (i,j) in moves:
                    print('*', end='')
                else:
                    print(self.board[i][j], end='')
            print()

    def translate(self, move, turn):
        move = move.replace('x', '')
        move = move.replace('+', '')
        move = move.replace('#', '')

        if turn == -1:
            temp_move = move
            move = ''
            for i in temp_move:
                if i in '12345678':
                    move += str(9-int(i))
                elif i in 'abcdefgh':
                    move += 'hgfedcba'['abcdefgh'.index(i)]
                else:
                    move += i

        if len(move) == 2: #pawn move
            target = (8-int(move[1]), int(chr(ord(move[0])-49)))
            below = self.buff_board[2 + target[0]+1][2 + target[1]]
            if below.color == turn and below.piece == 'pawn':
                pos = (target[0]+1, target[1])
                return pos, target
            elif not below.piece:
                below_below = self.buff_board[2 + target[0]+2][2 + target[1]]
                if target[0]==4 and below_below.color == turn and below_below.piece == 'pawn':
                    pos = (target[0]+2, target[1])
                    return pos, target
            return None
        elif len(move) == 3: #other move
            target = (8-int(move[2]), int(chr(ord(move[1])-49)))
            
            if move[:2] in 'abcdefgh' or move[:2] in 'hgfedcba': #pawn takes
                pos = (9-int(move[2]), 'abcdefgh'.index(move[0]))
                piece = self.buff_board[2 + pos[0]][2 + pos[1]]

                if piece.piece == 'pawn' and piece.color == turn:
                    moves = piece.valid_moves(pos, self.buff_board)

                    if target in moves:
                        return pos, target
                return None
                
            piece = self.abbr[move[0]](color=-1 * turn)
            moves = piece.valid_moves(target, self.buff_board)

            for tup in moves:
                adj = self.buff_board[2 + tup[0]][2 + tup[1]]
                if adj.color == turn and adj.piece == piece.piece:
                    if piece.piece == 'king':
                        self.king_pos[turn] = target
                    return tup, target
            return None
        elif len(move) == 4:
            target = (8-int(move[2]), int(chr(ord(move[1])-49)))
            piece = self.abbr[move[0]](-1 * turn)
            moves = piece.valid_moves(target, self.buff_board)

            if move[1] in '12345678':
                for tup in moves:
                    adj = self.buff_board[2 + tup[0]][2 + tup[1]]
                    if tup[0] == 8-int(move[1]) and adj.color == turn and adj.piece == piece.piece:
                        return tup, target
            elif move[1] in 'abcdefgh':
                for tup in moves:
                    adj = self.buff_board[2 + tup[0]][2 + tup[1]]
                    if tup[1] == 'abcdefgh'.index(move[1]) and adj.color == turn and adj.piece == piece.piece:
                        return tup, target
            return None
    
    def get_piece(self, pos):
        return self.board[pos[0]][pos[1]]

    def place_piece(self, pos, piece):
        self.board[pos[0]][pos[1]] = piece
        self.buff_board[2 + pos[0]][2 + pos[1]] = piece

    def move(self, pos, target): #move should be valid already
        self.place_piece(target, self.get_piece(pos))
        self.place_piece(pos, Empty())

    def switch_sides(self):
        self.board = self.board[::-1]
        self.board = [row[::-1] for row in self.board]
        self.buff_board = self.buff_board[::-1]
        self.buff_board = [row[::-1] for row in self.buff_board]

        self.king_pos[1] = (7-self.king_pos[1][0], 7-self.king_pos[1][1])
        self.king_pos[-1] = (7-self.king_pos[-1][0], 7-self.king_pos[-1][1])

    def play(self):
        player = 1

        while True:
            print('-'*20)
            self.display_board()

            moves = input('Move: ').split()

            if not moves:
                break

            init_board = [[deepcopy(piece) for piece in row] for row in self.board]
            init_player = player

            for move in moves:
                m = self.translate(move, player)
                if m:
                    self.move(m[0], m[1])

                    checked = self.in_check(player, self.king_pos[player])
                    if checked:
                        checked_piece = self.board[checked[0]][checked[1]]
                        print('The', checked_piece.piece, 'has you in check.')
                        m = None
                    else:
                        player = -1 * player

                        if self.in_checkmate(player):
                            print("CHECKMATED")

                        self.switch_sides()
                if not m:
                    print(move, 'WAS AN INVALID MOVE')
                    self.reset_board(init_board)
                    player = init_player
                    break

    def in_check(self, color, pos=None):
        king = King(color=color)
        if pos is None:
            pos = self.king_pos[color]

        #pawns
        down_left, down_right = self.buff_board[2 + pos[0]+1][2 + pos[1]-1], self.buff_board[2 + pos[0]+1][2 + pos[1]+1]
        if down_left.piece == 'pawn' and down_left.color == -1*color:
            return pos[0]-1, pos[1]-1
        if down_right.piece == 'pawn' and down_right.color == -1*color:
            return pos[0]-1, pos[1]+1
        
        knight, bishop, rook = Knight(color), Bishop(color), Rook(color)
        for move in knight.valid_moves(pos, self.buff_board):
            if self.buff_board[2 + move[0]][2 + move[1]].piece == 'knight':
                return move[0], move[1]
        for move in bishop.valid_moves(pos, self.buff_board):
            if self.buff_board[2 + move[0]][2 + move[1]].piece in ['bishop', 'queen']:
                return move[0], move[1]
        for move in rook.valid_moves(pos, self.buff_board):
            if self.buff_board[2 + move[0]][2 + move[1]].piece in ['rook', 'queen']:
                return move[0], move[1]
        for move in king.valid_moves(pos, self.buff_board):
            if self.buff_board[2 + move[0]][2 + move[1]].piece == 'king':
                return move[0], move[1]

        return None

    def in_checkmate(self, color):
        checked = self.in_check(color)
        if checked:
            pos = self.king_pos[color]
            king = self.board[pos[0]][pos[1]]

            #can king move and not be in check?
            for move in king.valid_moves(pos, self.buff_board):
                init_board = [[deepcopy(piece) for piece in row] for row in self.board]

                self.move(pos, move)

                if not self.in_check(color, move):
                    return False

                self.reset_board(init_board)

            #can the piece be taken?
            if self.in_check(-1 * color, checked):
                return False

            return True