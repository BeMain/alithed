import pyglet
import math
from pyglet.window import key

from game import physics_object, resources, util, constants


class Player(physics_object.PhysicsObject):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(
            img=resources.player_image, *args, **kwargs)

        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.move_speed = 50.0
        self.rotate_speed = 200.0

        self.world_x = 1000.0
        self.world_y = 1000.0

    def update(self, dt):
        super(Player, self).update()

        redraw_required = False

        # Handle rotation
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt
        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        # Handle movement
        speed = dt * self.move_speed
        if self.key_handler[key.RIGHT]:
            self.world_x += speed
            redraw_required = True
        if self.key_handler[key.LEFT]:
            self.world_x -= speed
            redraw_required = True
        if self.key_handler[key.UP]:
            self.world_y += speed
            redraw_required = True
        if self.key_handler[key.DOWN]:
            self.world_y -= speed
            redraw_required = True

        return redraw_required
