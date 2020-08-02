import pygame

IMAGES_MARIO_PATH = '../images/mario/'
IMAGES_BOARD_PATH = '../images/board/'


def load_image(path, name):
    return pygame.image.load(path + name)


def load_mario_image(name):
    return load_image(IMAGES_MARIO_PATH, name)


def load_board_image(name):
    return load_image(IMAGES_BOARD_PATH, name)


def get_list_blocks(path_world):
    file = open(path_world, "r")
    blocks = []
    for line in file:
        line = line[0:-1]
        blocks.append(line)
    file.close()
    return blocks


def is_legal_block(char):
    s = ['*', 'c', 'm', 's']
    return char in s
