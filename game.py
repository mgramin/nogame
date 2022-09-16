import pygame, pygame.locals
import sys, math

from tiles import load_tile_table

from world_generator import generate_world
from world_generator import textures


class CameraGroup(pygame.sprite.Group):
    def __init__(self, map, tiles, textures):
        super().__init__()

        self.map = map

        self.display_surface = pygame.display.get_surface()

        # camera offset 
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l,t,w,h)

        # ground
        self.ground_surf = pygame.image.load('world_textures.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = (0,0))

        # camera speed
        self.keyboard_speed = 32
        self.mouse_speed = 0.2

        # zoom 
        self.zoom_scale = 1
        self.internal_surf_size = (2500,2500)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']


    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e] and self.zoom_scale - 0.1 > 0:
            self.zoom_scale -= 0.1


    def custom_draw(self):
        self.keyboard_control()
        self.zoom_keyboard_control()

        tile_size = math.ceil(32 * self.zoom_scale)

        offset_x = int(self.offset.x//tile_size)
        offset_y = int(self.offset.y//tile_size)

        w, h = pygame.display.get_surface().get_size()

        for i in range(offset_x, offset_x + w//tile_size):
            for j in range(offset_y, offset_y + h//tile_size):
                if i < len(self.map) and i>0:
                    if j < len(self.map[i]) and j>0:
                        texture = self.map[i][j].texture
                        scaled_tile = pygame.transform.scale(tiles[texture.x][texture.y], (tile_size, tile_size))
                        screen.blit(scaled_tile, (tile_size*(i-offset_x), tile_size*(j-offset_y)))



if __name__=='__main__':

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    tiles = load_tile_table("world_textures.png", 32, 32)



    clock = pygame.time.Clock()
    map = generate_world()

    camera_group = CameraGroup(map, tiles, textures)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill('black')

        camera_group.update()
        camera_group.custom_draw()

        pygame.display.update()
        clock.tick(60)
