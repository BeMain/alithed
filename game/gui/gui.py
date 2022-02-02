import glooey

from game.gui import resources


class WhiteBorder(glooey.Background):
    custom_top = resources.white_border["top"]
    custom_bottom = resources.white_border["bottom"]
    custom_right = resources.white_border["right"]
    custom_left = resources.white_border["left"]

    custom_top_right = resources.white_border["tr"]
    custom_top_left = resources.white_border["tl"]
    custom_bottom_right = resources.white_border["br"]
    custom_bottom_left = resources.white_border["bl"]


class WhiteFrame(glooey.Frame):
    Decoration = WhiteBorder

    class Box(glooey.Bin):
        custom_right_padding = 15
        custom_top_padding = 15
        custom_left_padding = 15
        custom_bottom_padding = 15


class Label(glooey.Label):
    custom_font_name = "Lato Regular"
    custom_font_size = 20
    custom_color = "#b9ad86"
    custom_text_alignment = "center"

    custom_horz_padding = 15
    custom_top_padding = 13
    custom_bottom_padding = 10
    custom_alignment = "center"


class EditableLabel(glooey.EditableLabel):
    custom_font_name = "Lato Regular"
    custom_font_size = 20
    custom_color = "#b9ad86"
    custom_text_alignment = "left"

    custom_horz_padding = 15
    custom_top_padding = 13
    custom_bottom_padding = 10
    custom_size_hint = 200, 30
    custom_alignment = "center"


class Button(glooey.Button):
    Foreground = Label
    Background = WhiteBorder
