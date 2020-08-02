from src.load import *
from src.parameters import *
from src.position import *


class Board(object):
    # Board images.
    BALL = load_board_image('ball.png')
    BRICK = load_board_image('brick.png')
    EMPTY = load_board_image('empty.png')
    FLAG = load_board_image('flag.png')
    FLOOR = load_board_image('floor.png')
    PYRAMID = load_board_image('pyramid.png')
    QUESTION_MARK = load_board_image('qm.png')
    LEFT_BODY_PIPE = load_board_image('left_body_pipe.png')
    LEFT_HEAD_PIPE = load_board_image('left_head_pipe.png')
    RIGHT_BODY_PIPE = load_board_image('right_body_pipe.png')
    RIGHT_HEAD_PIPE = load_board_image('right_head_pipe.png')
    CASTLE = load_board_image('castle.png')

    VECTOR_CASTLE_POSITION = 4 * ELEMENT_SIZE, -(188 - ELEMENT_SIZE)

    def __init__(self, path_world):
        self.blocks = get_list_blocks(path_world)
        self.changed_blocks = []

    def draw(self, screen, game_position):
        castle_position = None
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                block = self.blocks[i][j]
                position = Position((j * ELEMENT_SIZE - game_position.get_x(), i * ELEMENT_SIZE))
                if block == 'b':
                    screen.blit(Board.BRICK, position.get_position())
                elif block == 'f':
                    if self.blocks[i + 1][j] == '#':
                        screen.blit(Board.PYRAMID, position.get_position())
                        castle_position = Position((j * ELEMENT_SIZE - game_position.get_x(), i * ELEMENT_SIZE))
                    else:
                        box = pygame.Rect(position.get_x() + ELEMENT_SIZE // 2 - 3, position.get_y(), 6, ELEMENT_SIZE)
                        pygame.draw.rect(screen, GREEN, box)
                    if self.blocks[i - 1][j] == '*':
                        screen.blit(Board.BALL, (position.get_x() + 8, position.get_y()))
                    elif self.blocks[i - 2][j] == '*':
                        screen.blit(Board.FLAG, (position.get_x() - ELEMENT_SIZE // 2,
                                                 position.get_y() - (ELEMENT_SIZE // 2 - 1)))

                elif block == '#':
                    screen.blit(Board.FLOOR, position.get_position())
                elif block == 'p':
                    screen.blit(Board.PYRAMID, position.get_position())
                elif block == '?':
                    screen.blit(Board.QUESTION_MARK, position.get_position())
                elif block == 't':
                    if self.blocks[i - 1][j] == 't':
                        if self.blocks[i][j + 1] == 't':
                            screen.blit(Board.LEFT_BODY_PIPE, position.get_position())
                        else:
                            screen.blit(Board.RIGHT_BODY_PIPE, position.get_position())
                    else:
                        if self.blocks[i][j + 1] == 't':
                            screen.blit(Board.LEFT_HEAD_PIPE, position.get_position())
                        else:
                            screen.blit(Board.RIGHT_HEAD_PIPE, position.get_position())

                if (j, i) in self.changed_blocks:
                    screen.blit(Board.EMPTY, position.get_position())
        castle_position.change_position(Board.VECTOR_CASTLE_POSITION[0], Board.VECTOR_CASTLE_POSITION[1])
        screen.blit(Board.CASTLE, castle_position.get_position())

    def get_block(self, x, y):
        return self.blocks[y][x]

    def add_changed_block(self, point):
        self.changed_blocks.append((point[0], point[1]))

    def is_in_changed_blocks(self, point):
        return point in self.changed_blocks
