from src.parameters import *
from src.player import Player
from src.board import Board
from src.position import Position
from src.load import is_legal_block
import pygame


class Game(object):
    WORLD_PATH = '../worlds/world1-1.txt'
    JUMP_SOUND_PATH = '../sounds/jump.wav'
    COIN_SOUND_PATH = '../sounds/coin.wav'
    MAIN_THEME_PATH = '../sounds/main-theme.mp3'

    VELOCITY_SCALE = 50

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mario')
        pygame.mixer.music.load(Game.MAIN_THEME_PATH)
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0
        self.run = True
        self.player = Player()
        self.board = Board(Game.WORLD_PATH)
        self.position = Position((0, 0))
        self.jumpSound = pygame.mixer.Sound(Game.JUMP_SOUND_PATH)
        self.coinSound = pygame.mixer.Sound(Game.COIN_SOUND_PATH)
        self.execute()

    def execute(self):
        while self.run:
            self.handle_events()
            self.ticking()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not self.player.get_is_jump():
                self.player.begin_jump()
                self.jumpSound.play()

    def make_move(self, keys):
        if keys[pygame.K_RIGHT]:
            self.player.set_key(pygame.K_RIGHT)
            self.player.increase_velocity()
        elif keys[pygame.K_LEFT]:
            self.player.set_key(pygame.K_LEFT)
            self.player.increase_left_velocity()
        else:
            self.player.decrease_velocity()
            self.player.decrease_left_velocity()

        if self.player.get_key() == pygame.K_RIGHT:
            rescale_velocity = self.get_rescale_velocity()
            while not self.check_right(rescale_velocity):
                rescale_velocity -= 1
            if self.player.is_start_position():
                self.position.change_position(rescale_velocity, 0)
            else:
                difference = self.player.get_positions_difference()
                self.player.change_player_position((min(rescale_velocity, difference[0]), 0))
                if rescale_velocity - difference[0] > 0:
                    self.position.change_position(rescale_velocity - difference[0], 0)
        else:
            rescale_left_velocity = self.get_rescale_left_velocity()
            while not self.check_left(rescale_left_velocity):
                rescale_left_velocity -= 1
            self.player.change_player_position((-rescale_left_velocity, 0))

        self.player.increase_walk_count()

    def get_rescale_velocity(self):
        return self.player.get_velocity() // Game.VELOCITY_SCALE

    def get_rescale_left_velocity(self):
        return self.player.get_left_velocity() // Game.VELOCITY_SCALE

    def ticking(self):
        self.tps_delta += self.tps_clock.tick() / 1000.0
        while self.tps_delta > 1 / TPS_MAX:
            keys = pygame.key.get_pressed()
            if not self.player.get_is_jump():
                if self.check_down():
                    self.player.begin_jump()
                    self.player.gain_top_jump()
                    self.player.fall()
            else:
                self.set_player_height()
            self.make_move(keys)
            self.tps_delta -= 1 / TPS_MAX

    def set_player_height(self):
        if self.player.get_top_jump() and self.check_down():
            self.player.fall()
        if not self.player.get_top_jump() and not self.player.is_max_jump_count():
            self.player.jump()
        if not self.player.get_top_jump() and (self.player.is_max_jump_count() or not self.check_up()):
            self.player.gain_top_jump()
            if not self.check_up() and self.is_question_mark():
                if not self.board.is_in_changed_blocks(self.get_position_question_mark()):
                    self.coinSound.play()
                    self.board.add_changed_block(self.get_position_question_mark())
        if self.player.get_top_jump() and not self.check_down():
            self.player.end_fall()

    def is_question_mark(self):
        p1 = self.player.get_top_left_corner()
        p2 = self.player.get_top_right_corner()
        return self.get_char((p1[0], p1[1] - 1)) == '?' or self.get_char((p2[0], p2[1] - 1)) == '?'

    def get_position_question_mark(self):
        p1 = self.player.get_top_left_corner()
        p2 = self.player.get_top_right_corner()
        if self.get_char((p1[0], p1[1] - 1)) == '?':
            return self.get_position_char((p1[0], p1[1] - 1))
        else:
            return self.get_position_char((p2[0], p2[1] - 1))

    def get_char(self, p):
        point = Position((p[0], p[1]))
        point.change_position(self.position.get_x(), self.position.get_y())
        point.scale_position(ELEMENT_SIZE)
        return self.board.get_block(point.get_x(), point.get_y())

    def get_position_char(self, p):
        point = Position((p[0], p[1]))
        point.change_position(self.position.get_x(), self.position.get_y())
        point.scale_position(ELEMENT_SIZE)
        return point.get_x(), point.get_y()

    def check_up(self):
        p1 = self.player.get_top_right_corner()
        p2 = self.player.get_top_left_corner()
        return self.is_legal_point(p1[0], p1[1] - 1) and self.is_legal_point(p2[0], p2[1] - 1)

    def check_down(self):
        p1 = self.player.get_bottom_right_corner()
        p2 = self.player.get_bottom_left_corner()
        return self.is_legal_point(p1[0], p1[1] + 1) and self.is_legal_point(p2[0], p2[1] + 1)

    def check_right(self, distance):
        p1 = self.player.get_top_right_corner()
        p2 = self.player.get_bottom_right_corner()
        return self.is_legal_point(p1[0] + distance, p1[1]) and self.is_legal_point(p2[0] + distance, p2[1])

    def check_left(self, distance):
        p1 = self.player.get_top_left_corner()
        p2 = self.player.get_bottom_left_corner()
        return self.is_legal_point(p1[0] - distance, p1[1]) and self.is_legal_point(p2[0] - distance, p2[1])

    def is_legal_point(self, x, y):
        point = Position((x, y))
        point.change_position(self.position.get_x(), self.position.get_y())
        point.scale_position(ELEMENT_SIZE)
        return is_legal_block(self.board.get_block(point.get_x(), point.get_y()))

    def draw(self):
        self.screen.fill(SKY_COLOR)
        self.board.draw(self.screen, self.position)
        self.player.draw(self.screen)
        pygame.display.flip()


game = Game()
