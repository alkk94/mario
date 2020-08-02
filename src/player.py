from src.parameters import *
from src.position import *
from src.load import *


class Player(object):
    ACCELERATION = 1
    VELOCITY_MAX = 200 * ACCELERATION
    JUMP_MAX = 4 * ELEMENT_SIZE
    JUMP_SPEED = 2
    WALK_COUNT_RANGE = 7
    WALK_COUNT_MAX = 3 * WALK_COUNT_RANGE
    START_POSITION = WIDTH // 2, HEIGHT - 3 * ELEMENT_SIZE
    # GRAVITY_ACCELERATION = 1

    # Mario images.
    WALK_RIGHT = [load_mario_image('r1.png'), load_mario_image('r2.png'), load_mario_image('r3.png')]
    STAND_RIGHT = load_mario_image('r.png')
    JUMP_RIGHT = load_mario_image('r_jump.png')
    WALK_LEFT = [load_mario_image('l1.png'), load_mario_image('l2.png'), load_mario_image('l3.png')]
    STAND_LEFT = load_mario_image('l.png')
    JUMP_LEFT = load_mario_image('l_jump.png')

    def __init__(self):
        self.position = Position(Player.START_POSITION)
        self.key = pygame.K_RIGHT
        self.velocity = 0
        self.leftVelocity = 0
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 0
        self.topJump = False
        # self.fallingSpeed = 0

    def get_corner(self, dx, dy):
        return self.position.get_x() + dx, self.position.get_y() + dy

    def get_bottom_left_corner(self):
        return self.get_corner(0, ELEMENT_SIZE - 1)

    def get_top_left_corner(self):
        return self.get_corner(0, 0)

    def get_top_right_corner(self):
        return self.get_corner(ELEMENT_SIZE - 1, 0)

    def get_bottom_right_corner(self):
        return self.get_corner(ELEMENT_SIZE - 1, ELEMENT_SIZE - 1)

    def get_key(self):
        return self.key

    def get_positions_difference(self):
        return Player.START_POSITION[0] - self.position.get_x(), Player.START_POSITION[1] - self.position.get_y()

    def is_start_position(self):
        return self.position.is_same_positions(Player.START_POSITION)

    def set_key(self, key):
        self.key = key

    def increase_velocity(self):
        if self.velocity < Player.VELOCITY_MAX:
            self.velocity += Player.ACCELERATION

    def increase_left_velocity(self):
        if self.leftVelocity < Player.VELOCITY_MAX:
            self.leftVelocity += Player.ACCELERATION

    def decrease_velocity(self):
        if self.velocity > 0:
            self.velocity -= 2 * Player.ACCELERATION
            if self.velocity < 0:
                self.velocity = 0

    def decrease_left_velocity(self):
        if self.leftVelocity > 0:
            self.leftVelocity -= 2 * Player.ACCELERATION
            if self.leftVelocity < 0:
                self.leftVelocity = 0

    def change_player_position(self, point):
        self.position.change_position(point[0], point[1])

    def jump(self):
        self.position.change_position(0, -Player.JUMP_SPEED)
        self.jumpCount += Player.JUMP_SPEED

    def fall(self):
        self.position.change_position(0, Player.JUMP_SPEED)

    def draw(self, screen):
        if self.isJump:
            if self.key == pygame.K_RIGHT:
                screen.blit(Player.JUMP_RIGHT, self.position.get_position())
            else:
                screen.blit(Player.JUMP_LEFT, self.position.get_position())
        elif self.velocity == 0 and self.leftVelocity == 0:
            if self.key == pygame.K_RIGHT:
                screen.blit(Player.STAND_RIGHT, self.position.get_position())
            else:
                screen.blit(Player.STAND_LEFT, self.position.get_position())
        elif self.key == pygame.K_RIGHT:
            self.walkCount %= Player.WALK_COUNT_MAX
            screen.blit(Player.WALK_RIGHT[self.walkCount // Player.WALK_COUNT_RANGE], self.position.get_position())
        else:
            self.walkCount %= Player.WALK_COUNT_MAX
            screen.blit(Player.WALK_LEFT[self.walkCount // Player.WALK_COUNT_RANGE], self.position.get_position())

    def get_is_jump(self):
        return self.isJump

    def set_is_jump(self, boolean):
        self.isJump = boolean

    def get_position_x(self):
        return self.position.get_x()

    def get_position_y(self):
        return self.position.get_y()

    def increase_walk_count(self):
        self.walkCount += 1

    def get_velocity(self):
        return self.velocity

    def get_left_velocity(self):
        return self.leftVelocity

    def get_top_jump(self):
        return self.topJump

    def gain_top_jump(self):
        self.topJump = True

    def is_max_jump_count(self):
        return self.jumpCount == Player.JUMP_MAX

    def end_fall(self):
        self.topJump = False
        self.isJump = False
        self.jumpCount = 0

    def begin_jump(self):
        self.isJump = True
