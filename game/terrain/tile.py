import pyglet

from game import resources, constants, style, positions

class Tile(pyglet.sprite.Sprite):
    BATCH = None
    GROUPS = {}

    def __init__(self, *args, **kwargs):
        super(Tile, self).__init__(img=resources.tiles[0], usage="static", *args, **kwargs)

        self.register_event_type("on_update")

        self.value = 0
        self.material = "air"

        self.tilepos = positions.Tilepos()
    
    @property
    def screenpos(self):
        return positions.Screenpos(self.x, self.y)
    
    @property
    def size(self):
        return positions.Size2(self.width, self.height)

    @staticmethod
    def init_rendering(batch, group):
        Tile.BATCH = batch
        Tile.GROUPS = {
            -1 : pyglet.graphics.OrderedGroup(0, parent=group),
            0 : pyglet.graphics.OrderedGroup(1, parent=group),
            1 : pyglet.graphics.OrderedGroup(2, parent=group),
        }

    def set_pos(self, screenpos, z):
        newpos = screenpos + self.tilepos * constants.TILE_SIZE

        # Check bounds
        if not newpos.is_on_screen(margin=(constants.TILE_SIZE // 2)):
            # Don't render if sprite is not on screen
            self.batch = None

        else:
            if self.material == "air":
                # Air shouldn't be rendered
                self.batch = None
            else:
                self.batch = self.BATCH

            self.x = newpos.x
            self.y = newpos.y
        
            # Change appearance depending on what layer we are on
            self.group = self.GROUPS[z]
            self.color = style.layers[z]["color"]
            self.opacity = style.layers[z]["opacity"]

    def set_material(self, material):
        self.material = material
        if material == "air":
            self.batch = None
        else:
            self.batch = self.BATCH
        
        # Trigger update
        self.dispatch_event("on_update", self.tilepos)


    def to_data(self):
        return {
            "tilepos": self.tilepos.to_list(),
            "value": self.value,
            "material": self.material,
        }

    @classmethod
    def from_data(cls, data):
        tile = cls()

        tile.tilepos = positions.Tilepos.from_list(data["tilepos"])

        color = data["value"] * 255
        tile.color = (color, color, color)
        tile.value = data["value"]
        
        tile.material = data["material"]

        return tile
