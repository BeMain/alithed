import pyglet
from pyglet.window import key

from game import constants, debug, positions, resources
from game.gui import pause
from game.terrain import data_handler, terrain


class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(
            img=resources.player_image, *args, **kwargs)

        self.register_event_type("on_move")

        self.key_handler = key.KeyStateHandler()
        self.event_handlers = [self.key_handler, self.on_mouse_motion]

        self.move_speed = 500.0
        self.rotate_speed = 200.0

        self.pos = positions.Worldpos(0, 0, 0)

        # Can't use just positions since this is what Pyglet wants
        self.x = constants.SCREEN_SIZE.width // 2
        self.y = constants.SCREEN_SIZE.height // 2
        self.screenpos = positions.Screenpos(self.x, self.y)

    @property
    def size(self):
        return positions.Size2(self.width, self.height)

    async def load_data(self):
        data = await data_handler.read_player_data()
        if data:
            self.pos = positions.Worldpos(*data["worldpos"])

    def to_data(self):
        return {
            "worldpos": [*self.pos]
        }

    async def save(self):
        await data_handler.write_player_data(self.to_data())

    async def update(self, dt):
        await self.handle_xy_movement(dt)
        self.handle_z_movement()

    async def handle_xy_movement(self, dt):
        # Handle movement
        dpos = positions.Vector2(0, 0)
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
            self.pos += positions.Pos3.from_pos2(
                *await self.calculate_move_xory(positions.Vector2(dpos.x, 0), speed))
        if dpos.y:
            # Move in y-direction
            self.pos += positions.Pos3.from_pos2(
                *await self.calculate_move_xory(positions.Vector2(0, dpos.y), speed))

        # Trigger move event
        self.dispatch_event("on_move")

    async def calculate_move_xory(self, dpos, speed):
        newpos = self.pos + dpos * (self.size // 2 + speed)

        tile = await terrain.get_tile(newpos)

        normal_move = dpos * speed
        snap_move = (abs(tile.screenpos - self.screenpos) -
                     tile.size // 2 - self.size // 2) * dpos

        # Check if new pos is obstructed
        if tile.material != "air":
            # Test if we can move UP to the next tile
            tile_a = await terrain.get_tile(newpos + positions.Pos3(0, 0, 1))
            if tile_a.material == "air":
                return normal_move, 1

            return snap_move, 0

        # Check if there is a tile below new pos
        if (await terrain.get_tile(newpos - positions.Pos3(0, 0, 1))).material == "air":
            # Test if we can move DOWN to the next tile
            if (await terrain.get_tile(newpos - positions.Pos3(0, 0, 2))).material != "air":
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
        terrain.queue_update()

    @pause.pausable
    def on_mouse_motion(self, x, y, dx, dy):
        pos = positions.Screenpos(x, y)
        self.rotation = self.screenpos.angle_to(pos)

    def collides_with(self, sprite):
        return self.screenpos.distancesq_to(sprite.x, sprite.y) < ((self.width + sprite.width) // 2) ** 2
