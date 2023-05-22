import pygame, os

class ImgLoader:
    """Check os.path"""
        
    @staticmethod
    def load_image(image_name):
        _, ext = os.path.splitext(image_name)
        if ext == '.jpg':
            return pygame.image.load(image_name).convert()
        elif ext == '.png':
            return pygame.image.load(image_name).convert_alpha()
        else:
            return None

    @staticmethod
    def load_ordered_imgs(dir_name):
        file_names = os.listdir(dir_name)
        if dir_name[-1] != "/":
            dir_name += "/"

        result = []
        for i in range(len(file_names)):
            img = pygame.image.load(dir_name + str(i) + '.png').convert_alpha()
            #img = pygame.transform.scale(img, (5 * img.get_rect().width, 5 * img.get_rect().height))
            result.append(img)

        return result

if __name__ == '__main__':
    pass