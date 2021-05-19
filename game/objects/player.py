import pyglet
from pyglet.window import key

import math
import concurrent.futures

from game import resources, constants, positions, debug
from game.terrain import terrain, data_handler
from game.gui import pause


class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)

        self.terrain = terrain.Terrain()

        self.register_event_type("on_move")

        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self.key_handler, self.on_mouse_motion]


        self.move_speed = 1000.0
        self.rotate_speed = 200.0

        self.pos = positions.Worldpos()

        # Can't use just positions since this is what Pyglet wants
        self.x = constants.SCREEN_WIDTH // 2
        self.y = constants.SCREEN_HEIGHT // 2
        self.screenpos = positions.Screenpos(self.x, self.y)

        # Load player data
        self.load_data()
    
    @property
    def size(self):
        return positions.Size2(self.width, self.height)

    def load_data(self):
        data = data_handler.read_player_data()
        if data:
            self.pos = positions.Worldpos(*data["worldpos"])
    
    def to_data(self):
        return {
            "worldpos": self.pos.to_coords()
        }
    
    def save(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(data_handler.write_player_data, self.to_data())


    def update(self, dt):
        self.handle_xy_movement(dt)
        self.handle_z_movement()

        
    def handle_xy_movement(self, dt):
        # Handle movement
        dpos = positions.Vector2(0,0)
        if self.key_handler[key.RIGHT] or self.key_handler[key.D]:
            dpos.x += 1
        if self.key_handler[key.LEFT] or self.key_handler[key.A]:
            dpos.x -= 1
        if self.key_handler[key.UP] or self.key_handler[key.W]:
            dpos.y += 1
        if self.key_handler[key.DOWN] or self.key_handler[key.S]:
            dpos.y -= 1

        if not dpos:
            return
            
        # Normalize to avoid fast diagonal movement
        dpos.normalize()
        
        speed = self.move_speed * dt

        if dpos.x:
            # Move in x-direction
            self.pos += positions.Pos3.from_pos2(*self.calculate_move_xory(positions.Vector2(x=dpos.x), speed))
        if dpos.y:
            # Move in y-direction
            self.pos += positions.Pos3.from_pos2(*self.calculate_move_xory(positions.Vector2(y=dpos.y), speed))

        # Trigger move event
        self.dispatch_event("on_move")


    def calculate_move_xory(self, dpos, speed):
        newpos = self.pos + dpos * (self.size // 2 + speed)

        tile = self.terrain.get_tile(newpos)

        normal_move = dpos * speed
        snap_move = (abs(tile.screenpos - self.screenpos) - tile.size // 2 - self.size // 2) * dpos

        # Check if new pos is obstructed
        if tile.material != "air":
            # Test if we can move UP to the next tile
            tile_a = self.terrain.get_tile(newpos + positions.Pos3(0, 0, 1))
            if tile_a.material == "air":
                return normal_move, 1

            return snap_move, 0
        
        # Check if there is a tile below new pos
        if self.terrain.get_tile(newpos - positions.Pos3(0, 0, 1)).material == "air":
            # Test if we can move DOWN to the next tile
            if self.terrain.get_tile(newpos - positions.Pos3(0, 0, 2)).material != "air":
                return normal_move, -1
            
            return snap_move, 0
        
        # Normal movement
        return normal_move, 0


    def handle_z_movement(self):
        if self.key_handler[key.Z]:
            self.pos.z += 1
            self.dispatch_event("on_move")
        if self.key_handler[key.X]:
            self.pos.z -= 1
            self.dispatch_event("on_move")
    
    def on_move(self):
        self.terrain.update(self.pos)

    @pause.pausable
    def on_mouse_motion(self, x, y, dx, dy):
        pos = positions.Screenpos(x, y)
        self.rotation = self.screenpos.angle_to(pos)


    def collides_with(self, sprite):
        return self.screenpos.distancesq_to(sprite.x, sprite.y) < ((self.width + sprite.width) // 2) ** 2
