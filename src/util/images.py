import pygame
import util.resources as resources

images = {}

def load_image(file_name):
    if file_name not in images:
        file_path = resources.get_resource_path(file_name)
        image = pygame.image.load(file_path)
        image.convert()
        images[file_name] = image
    return images.get(file_name)
