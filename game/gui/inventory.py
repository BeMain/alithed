import glooey

from game import items, resources
from game.gui import gui



class Inventory:
    def __init__(self, gui, *args, **kwargs):
        super().__init__()
        self.gui = gui

        self.gridview = self.GridView()

        self.is_open = False


    def open(self):
        if not self.is_open:
            self.is_open = True
            self.gui.add(self.gridview)

    def close(self):
        if self.is_open:
            self.is_open = False
            self.gui.remove(self.gridview)
    
    def toggle(self):
        if not self.is_open:
            self.open()
        else:
            self.close()
        

    class GridView(glooey.Widget):
        num_rows = 5
        num_cols = 5

        Grid = glooey.Grid

        class Cell(glooey.images.Image):
            def __init__(self, item, *args, **kwargs):
                image = resources.tiles[item["texture_id"]]
                super().__init__(image, *args, **kwargs)

                self.item = item
        

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.items = [[items.items["stone"]] * self.num_rows]* self.num_cols

            # Create widgets
            self.grid = self.Grid()

            for x in range(self.num_rows):
                for y in range(self.num_cols):
                    self.grid.add(x,y, self.Cell(self.items[x][y]))

            self._attach_child(self.grid)