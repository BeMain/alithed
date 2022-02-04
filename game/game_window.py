import asyncio
import time
import pyglet
from pyglet.window import key

from game import constants, debug, positions, resources
from game.gui import pause
from game.gui.handler import GuiHandler
from game.objects import player
from game.terrain import Tile, terrain


class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(GameWindow, self).__init__(constants.SCREEN_SIZE.width,
                                         constants.SCREEN_SIZE.height, vsync=False, *args, **kwargs)
        self.running = True

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
    async def update(self, dt):
        await terrain.update(self.player.pos)

        for obj in self.game_objects:
            await obj.update(dt)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:    # Exit
            loop = asyncio.get_event_loop()
            loop.create_task(self.exit())

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

        # Load saved player data
        await self.player.load_data()

        # Update terrain
        await terrain.update(self.player.pos)
        last_update = time.time()

        # Main loop
        while self.running:
            start_time = time.time()

            # Update & render
            await self.update(start_time - last_update)
            self.render()

            # Sleep for the rest of the frame
            await asyncio.sleep(max((1 / constants.FPS) - (time.time() - start_time), 0))

            # Catch events (don't know why we do this)
            event = self.dispatch_events()
            if event:
                debug.log("Event:", event)

            last_update = start_time

    async def exit(self):
        # Save chunks
        for k in terrain.chunks:
            await terrain.chunks[k].delete()

        # Save player
        await self.player.save()

        # Stop the game
        self.running = False
