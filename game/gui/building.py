import glooey


class Workbench3(glooey.Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        grid = glooey.Grid(3, 3)

        text = "Hej!"
        label = glooey.Label(text, line_wrap=640)
        grid.add(0, 0, label)

        grid.add(1, 2, glooey.Placeholder())

        self.add(grid)
