import pygame


class TextView(pygame.sprite.Sprite):
    def __init__(self, text, x, y, right_finish_position, finish_callback, group):
        super().__init__(group)
        self._text = text
        self._available = True
        self._x = x
        self._y = y
        self._right_finish_position = right_finish_position
        self._finish_callback = finish_callback
        self._font_text = pygame.font.Font(None, 50)
        self.image = self._font_text.render(text, 1, WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self._last_coordinates = None
        self._k_x = 1
        self._k_y = 1
        self._speed = 8

    def update(self, *args):
        if self._available and len(args) == 2:
            if (self.rect[0] + self.rect[2]) > args[0][0] > self.rect[0] \
                    and (self.rect[1] + self.rect[3]) > args[0][1] > self.rect[1]:
                self._last_coordinates = (args[1][0], args[1][1])
                self._available = False
                delta_x = abs(self._x - self._last_coordinates[0])
                delta_y = abs(self._y - self._last_coordinates[1])
                if delta_x > delta_y:
                    self._k_x = 1
                    self._k_y = abs(self._y - self._last_coordinates[1]) / abs(self._x - self._last_coordinates[0])
                elif delta_x < delta_y:
                    self._k_x = abs(self._x - self._last_coordinates[0]) / abs(self._y - self._last_coordinates[1])
                    self._k_y = 1
                self._k_x *= 1 if self._x < self._last_coordinates[0] else -1
                self._k_y *= 1 if self._y < self._last_coordinates[1] else -1
                self._k_x *= self._speed
                self._k_y *= self._speed
                self._finish_callback()
        elif not self._available and self._last_coordinates is not None \
                and (abs(self.rect.x - self._last_coordinates[0]) > self._speed or
                     abs(self.rect.y - self._last_coordinates[1]) > self._speed):
            if self._right_finish_position == self._last_coordinates:
                self.image = self._font_text.render(self._text, 1, GREEN)
            else:
                self.image = self._font_text.render(self._text, 1, RED)
            self._x += self._k_x
            self._y += self._k_y
            self.rect.x = self._x
            self.rect.y = self._y


GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RANDOM_COLOR = (234, 165, 43)

target_position = [(425, 77), (685, 77), (360, 277), (650, 277)]

FPS = 60

pygame.init()
display = pygame.display.set_mode((1281, 720))
display.fill((255, 255, 255))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)
text = font.render("Слово слово_________слово_________слово слово", 1, WHITE)
place = text.get_rect(center=(600, 100))

font1 = pygame.font.Font(None, 50)
text1 = font1.render("Слово_________слово_________слово слово", 1, WHITE)
place1 = text1.get_rect(center=(600, 300))

surf_down = pygame.Surface((1200, 100))
surf_down.fill(RANDOM_COLOR)
rect_surf_down = pygame.Rect((40, 560, 0, 0))


pygame.display.update()

count = 0


def inc_count():
    global count
    count += 1


text_group = pygame.sprite.Group()
for value in [["qwe", 100, target_position[0]], ["werfui", 300, target_position[1]], ["earhb", 500, target_position[2]],
              ["it7j", 700, target_position[3]]]:
    TextView(value[0], value[1], 600, value[2], inc_count, text_group)


def renderView():
    display.blit(image_surf, image_rect)
    display.blit(text, place)
    display.blit(text1, place1)
    display.blit(surf_down, rect_surf_down)
    text_group.draw(display)


text_group.draw(display)
pygame.display.update()

image_surf = pygame.image.load("game_photo1.jpg")
image_rect = image_surf.get_rect()

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1 and count < len(target_position):
            text_group.update((i.pos[0], i.pos[1]), target_position[count])
    text_group.update()
    renderView()
    pygame.display.update()
    clock.tick(FPS)
