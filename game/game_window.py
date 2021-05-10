import pyglet
from pyglet.window import key

import glooey

import time
import math

from game import constants, resources, util
from game.objects import player
from game.terrain import terrain, tile, data_handler
from game.gui import pause
from game.gui.handler import GuiHandler


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(constants.SCREEN_WIDTH,
                                         constants.SCREEN_HEIGHT, vsync=False, *args, **kwargs)
        self.running = True
        self.last_scheduled_update = time.time()

        # Batches
        self.main_batch = pyglet.graphics.Batch()
        self.gui_batch = pyglet.graphics.Batch()

        # Groups
        self.main_group = pyglet.graphics.Group()
        self.objects_group = pyglet.graphics.OrderedGroup(5, parent=self.main_group)

        # Objects
        self.gui = GuiHandler(self, batch=self.gui_batch)
        self.terrain = terrain.Terrain()
        self.player = player.Player(batch=self.main_batch, group=self.objects_group)
        self.fps_display = self.init_fps_display()

        self.game_objects = [self.player]
        self.game_obj_event_handlers = [handler for obj in self.game_objects for handler in obj.event_handlers]
            
        # Register event handlers
        self.push_handlers(*self.game_obj_event_handlers)
        
        self.terrain.push_handlers(on_update=self.on_tile_update)

        # Init tile.Tile so they can render properly
        tile.Tile.init_rendering(self.main_batch, self.main_group)

    def init_fps_display(self):
        display = pyglet.window.FPSDisplay(self)
        display.label.color = (255,255,255,255)

        return display

    def render(self):
        self.clear()

        # Draw background
        resources.background_image.blit(0,0)

        # Draw objects
        self.main_batch.draw()
        self.fps_display.draw()

        self.gui_batch.draw()

        self.flip()

    @pause.pausable
    def update(self, dt):
        # Update all objects
        for obj in self.game_objects:
            obj.update(dt)


    def on_tile_update(self, chunk_x, chunk_y, chunk_z, tile_x, tile_y):
        self.terrain.update(self.player.world_x, self.player.world_y, self.player.world_z)


    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # Exit the game
            self.exit()
        
        elif symbol == key.P:
            # Pause the game
            if self.gui.menus:
                self.gui.close_menus()
            else:
                self.gui.open_main_menu()
        
        elif symbol == key.I:
            self.gui.inventory.toggle()

    @pause.pausable
    def on_mouse_press(self, x, y, button, modifiers):
        x = util.clamp(x, 0, constants.SCREEN_WIDTH)
        y = util.clamp(y, 0, constants.SCREEN_HEIGHT)

        world_x = self.player.world_x - constants.SCREEN_WIDTH / 2 + x
        world_y = self.player.world_y - constants.SCREEN_HEIGHT / 2 + y
        
        tile = self.terrain.get_tile(world_x, world_y, self.player.world_z)
        if tile.material == "air":
            tile.set_material("stone")
        else:
            tile.set_material("air")

    def run(self):
        # Initialization
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)

        # Update terrain
        self.terrain.update(self.player.world_x, self.player.world_y, self.player.world_z)

        self.last_scheduled_update = time.time()

        # Main loop
        while self.running:
            if time.time() - self.last_scheduled_update > 1 / constants.FPS:
                self.update(time.time() - self.last_scheduled_update)
                self.last_scheduled_update = time.time()
                self.render()

            event = self.dispatch_events()
            if event: print("Event:", event)

        
    def exit(self):
        # Save chunks
        for k in self.terrain.chunks:
            self.terrain.chunks[k].save()
            
        # Save player
        self.player.save()

        # Stop the game
        self.running = False