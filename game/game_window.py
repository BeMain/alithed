import pyglet
from pyglet.window import key

import asyncio
import time

from game import constants, resources, positions, debug
from game.terrain import terrain, Tile
from game.objects import player
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
        self.objects_group = pyglet.graphics.OrderedGroup(
            5, parent=self.main_group)

        # Objects
        self.gui = GuiHandler(self, batch=self.gui_batch)
        self.player = player.Player(
            batch=self.main_batch, group=self.objects_group)
        self.fps_display = self.init_fps_display()

        self.game_objects = [self.player]
        self.game_obj_event_handlers = [
            handler for obj in self.game_objects for handler in obj.event_handlers]

        # Register event handlers
        self.push_handlers(*self.game_obj_event_handlers)

        # Init Tile so they can render properly
        Tile.init_rendering(self.main_batch, self.main_group)

    def init_fps_display(self):
        display = pyglet.window.FPSDisplay(self)
        display.label.color = (255, 255, 255, 255)

        return display

    def render(self):
        self.clear()

        # Draw background
        resources.background_image.blit(0, 0)
        # Draw objects
        self.main_batch.draw()
        self.gui_batch.draw()
        self.fps_display.draw()

        self.flip()

    @pause.pausable
    def update(self, dt):
        for obj in self.game_objects:
            obj.update(dt)

        terrain.update(self.player.pos)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:    # Exit
            self.exit()

        elif symbol == key.P:       # Menu
            if self.gui.menus:
                self.gui.close_menus()
            else:
                self.gui.open_main_menu()

        elif symbol == key.I:       # Inventory
            self.gui.inventory.toggle()

    @pause.pausable
    def on_mouse_press(self, x, y, button, modifiers):
        pos = positions.Screenpos(x, y)
        pos.clamp_to_screen()

        worldpos = pos.to_worldpos(self.player.pos)

        tile = terrain.get_tile(worldpos)
        if tile.material == "air":
            tile.set_material("stone")
        else:
            tile.set_material("air")

    async def run(self):
        # Initialization
        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)

        # Update terrain
        terrain.update(self.player.pos)
        self.last_scheduled_update = time.time()

        # Main loop
        while self.running:
            start_time = time.time()
            self.update(start_time - self.last_scheduled_update)
            self.render()

            self.last_scheduled_update = start_time

            await asyncio.sleep(max((1 / constants.FPS) - (time.time() - self.last_scheduled_update), 0))

            event = self.dispatch_events()
            if event:
                debug.log("Event:", event)

    def exit(self):
        # Save chunks
        for k in terrain.chunks:
            terrain.chunks[k].save()

        # Save player
        self.player.save()

        # Stop the game
        self.running = False
