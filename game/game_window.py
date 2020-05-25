import pyglet
from pyglet.window import key

import time
import math

from game import constants, resources
from game.objects import player
from game.terrain import terrain, tile


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(constants.SCREEN_WIDTH,
                                         constants.SCREEN_HEIGHT, vsync=False, *args, **kwargs)
        self.running = True
        self.last_scheduled_update = time.time()

        self.main_batch = pyglet.graphics.Batch()

        self.objects_group = pyglet.graphics.OrderedGroup(1)

        self.player_sprite = player.Player(batch=self.main_batch, group=self.objects_group)
        self.terrain = terrain.Terrain()
        self.fps_display = pyglet.window.FPSDisplay(self)

        self.game_objects = [self.player_sprite]

        # Register event handlers
        for obj in self.game_objects:
            for handler in obj.event_handlers:
                self.push_handlers(handler)

        # Pass main_batch to tile.Tile so they can render properly
        tile.Tile.MAIN_BATCH = self.main_batch

    def render(self):
        self.clear()

        # Draw background
        resources.background_image.blit(0,0)

        self.main_batch.draw()
        self.fps_display.draw()

        self.flip()

    def update(self, dt):
        redraw_needed = False

        # Update all objects
        for obj in self.game_objects:
            if obj.update(dt):
                redraw_needed = True

        # Only redraw terrain if needed
        if redraw_needed:
            self.terrain.update(
                self.player_sprite.world_x, self.player_sprite.world_y, self.player_sprite.world_z)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.running = False

    def run(self):
        self.last_scheduled_update = time.time()

        # First draw
        resources.background_image.blit(0,0)
        self.terrain.update(
            self.player_sprite.world_x, self.player_sprite.world_y, self.player_sprite.world_z)

        # Main loop
        while self.running:
            if time.time() - self.last_scheduled_update > 1 / constants.FPS:
                self.update(time.time() - self.last_scheduled_update)
                self.last_scheduled_update = time.time()
            self.render()

            event = self.dispatch_events()
