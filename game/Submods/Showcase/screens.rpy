# Showcase screens

init python:
    class ShowcaseFullscreen(Action):
        def __init__(self, filename):
            self.filename = filename

        def __call__(self):
            renpy.run(Show("showcase_fullscreen", filename=self.filename))

    class ShowcaseAlbumView(Action):
        def __init__(self, filename):
            self.filename = filename

        def __call__(self):
            renpy.run(Show("showcase_album_view", filename=self.filename))

    class ShowcaseConfirmRemove(Action):
        def __init__(self, filename):
            self.filename = filename

        def __call__(self):
            renpy.run(Show("showcase_album_confirm", filename=self.filename))

    class ShowcaseDoRemove(Action):
        def __init__(self, filename):
            self.filename = filename

        def __call__(self):
            store.showcase.remove_art(self.filename)
            renpy.hide_screen("showcase_album_confirm")
            renpy.hide_screen("showcase_album_view")
            renpy.restart_interaction()


screen showcase_display(filename):
    zorder 40

    $ img = store.showcase.loadable_image(filename)
    $ art = store.showcase.fitted(img, 524, 404)
    $ panel = store.showcase.panel_fill()
    $ well = store.showcase.art_well_fill()
    $ txt_col = store.showcase.text_color()

    fixed:
        xpos 620
        ypos 40
        xsize 620
        ysize 560

        frame:
            background panel
            padding (4, 4)
            xfill True
            yfill True

            frame:
                style "mas_extra_menu_frame"
                padding (14, 14)
                xfill True
                yfill True

                vbox:
                    spacing 10
                    xfill True
                    yfill True

                    label _("For Monika"):
                        text_style "mas_extra_menu_label_text"
                        text_color txt_col
                        xalign 0.5

                    frame:
                        background well
                        padding (2, 2)
                        xalign 0.5
                        xsize 540
                        ysize 420

                        frame:
                            style "mas_extra_menu_frame"
                            padding (8, 8)
                            xfill True
                            yfill True

                            if img:
                                add art:
                                    xalign 0.5
                                    yalign 0.5
                            else:
                                text _("Image not found"):
                                    style "mas_extra_menu_label_text"
                                    color txt_col
                                    xalign 0.5
                                    yalign 0.5

                    textbutton _("Fullscreen"):
                        style "hkb_button"
                        xalign 0.5
                        action ShowcaseFullscreen(filename)


screen showcase_decide(filename):
    modal True
    zorder 80
    style_prefix "choice"

    $ img = store.showcase.loadable_image(filename)
    $ art = store.showcase.fitted(img, 500, 320)
    $ panel = store.showcase.panel_fill()
    $ well = store.showcase.art_well_fill()
    $ txt_col = store.showcase.text_color()

    fixed:
        xpos 620
        ypos 20
        xsize 620
        ysize 580

        frame:
            background panel
            padding (4, 4)
            xfill True
            yfill True

            frame:
                style "mas_extra_menu_frame"
                padding (14, 12)
                xfill True
                yfill True

                vbox:
                    spacing 8
                    xfill True
                    yfill True

                    label _("For Monika"):
                        text_style "mas_extra_menu_label_text"
                        text_color txt_col
                        xalign 0.5

                    frame:
                        background well
                        padding (2, 2)
                        xalign 0.5
                        xsize 520
                        ysize 340

                        frame:
                            style "mas_extra_menu_frame"
                            padding (8, 8)
                            xfill True
                            yfill True

                            if img:
                                add art:
                                    xalign 0.5
                                    yalign 0.5
                            else:
                                text _("Image not found"):
                                    style "mas_extra_menu_label_text"
                                    color txt_col
                                    xalign 0.5
                                    yalign 0.5

                    textbutton _("Fullscreen"):
                        style "hkb_button"
                        xalign 0.5
                        action ShowcaseFullscreen(filename)

                    null:
                        height 4

                    textbutton _("You can keep this one!"):
                        xsize 500
                        action Return("keep")

                    textbutton _("Just wanted to show you."):
                        xsize 500
                        action Return("show")


screen showcase_fullscreen(filename):
    modal True
    zorder 90

    $ img = store.showcase.loadable_image(filename)
    $ art = store.showcase.fitted(img, 1076, 540)
    $ panel = store.showcase.panel_fill()
    $ well = store.showcase.art_well_fill()
    $ txt_col = store.showcase.text_color()

    add Solid("#000000"):
        alpha 0.66

    frame:
        background panel
        xalign 0.5
        yalign 0.5
        padding (4, 4)
        xsize 1120
        ysize 660

        frame:
            style "mas_extra_menu_frame"
            padding (12, 12)
            xfill True
            yfill True

            vbox:
                spacing 10
                xfill True
                yfill True

                frame:
                    background well
                    xalign 0.5
                    xsize 1080
                    ysize 560
                    padding (6, 6)

                    if img:
                        add art:
                            xalign 0.5
                            yalign 0.5
                    else:
                        text _("Image not found"):
                            style "mas_extra_menu_label_text"
                            color txt_col
                            xalign 0.5
                            yalign 0.5

                textbutton _("Exit"):
                    style "hkb_button"
                    xalign 0.5
                    action Hide("showcase_fullscreen")

    key "K_ESCAPE" action Hide("showcase_fullscreen")
    key "mouseup_3" action Hide("showcase_fullscreen")


screen showcase_album_view(filename):
    modal True
    zorder 90

    $ img = store.showcase.loadable_image(filename)
    $ prev_file = store.showcase.adjacent_kept(filename, -1)
    $ next_file = store.showcase.adjacent_kept(filename, 1)
    $ art = store.showcase.fitted(img, 1000, 480)
    $ panel = store.showcase.panel_fill()
    $ well = store.showcase.art_well_fill()
    $ txt_col = store.showcase.text_color()

    add Solid("#000000"):
        alpha 0.66

    frame:
        background panel
        xalign 0.5
        yalign 0.5
        padding (4, 4)
        xsize 1080
        ysize 640

        frame:
            style "mas_extra_menu_frame"
            padding (12, 12)
            xfill True
            yfill True

            vbox:
                spacing 12
                xfill True
                yfill True

                frame:
                    background well
                    xalign 0.5
                    xsize 1030
                    ysize 500
                    padding (6, 6)

                    if img:
                        add art:
                            xalign 0.5
                            yalign 0.5
                    else:
                        text _("Image not found"):
                            style "mas_extra_menu_label_text"
                            color txt_col
                            xalign 0.5
                            yalign 0.5

                hbox:
                    xalign 0.5
                    spacing 16

                    textbutton _("< Prev"):
                        style "hkb_button"
                        sensitive (prev_file is not None)
                        action Show("showcase_album_view", filename=prev_file)

                    textbutton _("Fullscreen"):
                        style "hkb_button"
                        action ShowcaseFullscreen(filename)

                    textbutton _("Back"):
                        style "hkb_button"
                        action Hide("showcase_album_view")

                    textbutton _("Remove"):
                        style "hkb_button"
                        action ShowcaseConfirmRemove(filename)

                    textbutton _("Next >"):
                        style "hkb_button"
                        sensitive (next_file is not None)
                        action Show("showcase_album_view", filename=next_file)

    key "K_ESCAPE" action Hide("showcase_album_view")
    key "mouseup_3" action Hide("showcase_album_view")


screen showcase_album_confirm(filename):
    modal True
    zorder 95

    $ panel = store.showcase.panel_fill()
    $ txt_col = store.showcase.text_color()

    add Solid("#000000"):
        alpha 0.45

    frame:
        background panel
        xalign 0.5
        yalign 0.5
        padding (4, 4)
        xsize 540

        frame:
            style "mas_extra_menu_frame"
            padding (24, 20)
            xfill True

            vbox:
                spacing 14
                xfill True

                label _("Remove this from our album?"):
                    text_style "mas_extra_menu_label_text"
                    text_color txt_col
                    xalign 0.5

                text _("Your original file in the Art folder stays safe."):
                    style "mas_extra_menu_label_text"
                    color txt_col
                    size 16
                    xalign 0.5
                    text_align 0.5

                hbox:
                    xalign 0.5
                    spacing 24

                    textbutton _("Remove"):
                        style "hkb_button"
                        action ShowcaseDoRemove(filename)

                    textbutton _("Nevermind"):
                        style "hkb_button"
                        action Hide("showcase_album_confirm")

    key "K_ESCAPE" action Hide("showcase_album_confirm")


screen showcase_album():
    modal True
    zorder 50

    default page_index = 0

    python:
        pages = store.showcase.album_pages(per_page=6)
        page_count = max(1, len(pages))
        if page_index >= page_count:
            page_index = page_count - 1
        page_items = pages[page_index] if pages else []
        page_label = "Page {0} / {1}".format(page_index + 1, page_count)

    $ panel = store.showcase.panel_fill()
    $ slot = store.showcase.slot_fill()
    $ well = store.showcase.art_well_fill()
    $ txt_col = store.showcase.text_color()

    add Solid("#000000"):
        alpha 0.33

    frame:
        background panel
        xalign 0.5
        yalign 0.45
        padding (4, 4)
        xsize 740
        ysize 540

        frame:
            style "mas_extra_menu_frame"
            padding (18, 16)
            xfill True
            yfill True

            vbox:
                spacing 12
                xfill True
                yfill True

                label _("Our Album"):
                    text_style "mas_extra_menu_label_text"
                    text_color txt_col
                    xalign 0.5

                text _("Tap a picture to view or remove it"):
                    style "mas_extra_menu_label_text"
                    color txt_col
                    size 16
                    xalign 0.5

                grid 3 2:
                    xalign 0.5
                    spacing 12

                    for i in range(6):
                        if i < len(page_items):
                            $ fname = page_items[i]
                            $ thumb_path = store.showcase.loadable_image(fname)
                            $ thumb = store.showcase.fitted(thumb_path, 186, 136)

                            button:
                                style "scrollable_menu_button"
                                xsize 200
                                ysize 150
                                padding (6, 6)
                                action ShowcaseAlbumView(fname)

                                frame:
                                    background well
                                    xfill True
                                    yfill True
                                    padding (4, 4)

                                    if thumb_path:
                                        add thumb:
                                            xalign 0.5
                                            yalign 0.5
                                    else:
                                        text "?":
                                            style "mas_extra_menu_label_text"
                                            xalign 0.5
                                            yalign 0.5
                        else:
                            frame:
                                background slot
                                xsize 200
                                ysize 150
                                padding (2, 2)

                                frame:
                                    style "mas_extra_menu_frame"
                                    xfill True
                                    yfill True

                                    text ".":
                                        style "mas_extra_menu_label_text"
                                        size 28
                                        xalign 0.5
                                        yalign 0.5

                hbox:
                    xalign 0.5
                    spacing 20
                    yoffset 4

                    textbutton _("< Prev"):
                        style "hkb_button"
                        sensitive (page_index > 0)
                        action SetScreenVariable("page_index", page_index - 1)

                    text "[page_label]":
                        style "mas_extra_menu_label_text"
                        color txt_col
                        size 18
                        yalign 0.5

                    textbutton _("Next >"):
                        style "hkb_button"
                        sensitive (page_index < page_count - 1)
                        action SetScreenVariable("page_index", page_index + 1)

                textbutton _("Close"):
                    style "hkb_button"
                    xalign 0.5
                    action Return()

    key "K_ESCAPE" action Return()
