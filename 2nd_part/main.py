import os
import sys
import pygame
import requests


class MapObject:
    def __init__(self, ll=None, zoom=2, l="map"):
        if ll is None:
            ll = ['76.945465', '43.238293']
        self.zoom = zoom
        self.site = "https://static-maps.yandex.ru/1.x/"
        self.spn = ','.join([str(self.zoom), str(self.zoom)])
        self.ll = ",".join(ll)
        self.l = l

    def requests_get(self):
        self.spn = ','.join([str(self.zoom), str(self.zoom)])
        return requests.get(self.site, params={'ll': self.ll, 'l': self.l, 'spn': self.spn})

    def __str__(self):
        self.spn = ','.join([str(self.zoom), str(self.zoom)])
        return "https://static-maps.yandex.ru/1.x/?ll={}&spn={}&l={}".format(self.ll, self.spn, self.l)


mapa = MapObject()
map_file = "map.png"
clock = pygame.time.Clock()
running = True
pygame.init()
screen = pygame.display.set_mode((600, 450))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                mapa.zoom += 0.5
            if event.key == pygame.K_PAGEDOWN:
                if mapa.zoom - 0.5 > 0:
                    mapa.zoom -= 0.5

    response = mapa.requests_get()
    if not response:
        print("Ошибка выполнения запроса:")
        print(str(mapa))
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
os.remove(map_file)