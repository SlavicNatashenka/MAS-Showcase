# Showcase core

default persistent._showcase_kept = []
default persistent._showcase_shown = []
default persistent._showcase_seen_intro = False

init -1 python in showcase:
    import os
    import re
    import shutil
    import store

    REL_ROOT = "Submods/Showcase"
    REL_ART = REL_ROOT + "/Art"
    REL_KEPT = REL_ROOT + "/kept"

    SUPPORTED_EXTS = (".png",)

    def is_supported_art(filename):
        if not filename or filename.startswith("."):
            return False
        return filename.lower().endswith(SUPPORTED_EXTS)

    OVERLAY = "#000000"

    def _textbox_path():
        """Prefer Monika's dialogue box art so Comfy themes match automatically."""
        dark = bool(getattr(store.mas_globals, "dark_mode", False))
        candidates = []
        if dark:
            candidates.extend([
                "gui/textbox_monika_d.png",
                "gui/textbox_d.png",
                "gui/textbox_monika.png",
                "gui/textbox.png",
            ])
        else:
            candidates.extend([
                "gui/textbox_monika.png",
                "gui/textbox.png",
                "gui/textbox_monika_d.png",
                "gui/textbox_d.png",
            ])

        for path in candidates:
            if renpy.loadable(path):
                return path
        return None

    def panel_fill():
        """
        Opaque polka-dot panel using a tiled crop of the dialogue box.
        (Framing/stretching the whole textbox looks glitchy in a tall window.)
        """
        dark = bool(getattr(store.mas_globals, "dark_mode", False))
        base_color = "#14241F" if dark else "#FFFFFF"
        path = _textbox_path()

        if not path:
            return store.Solid("#210B16" if dark else "#FFF5F8")

        try:
            w, h = renpy.image_size(path)
            x = int(w * 0.18)
            y = int(h * 0.28)
            cw = max(48, int(w * 0.64))
            ch = max(48, int(h * 0.44))
            if x + cw > w:
                cw = w - x
            if y + ch > h:
                ch = h - y

            cell = store.im.Composite(
                (cw, ch),
                (0, 0), store.Solid(base_color, xsize=cw, ysize=ch),
                (0, 0), store.im.Crop(path, (x, y, cw, ch)),
            )
            return store.im.Tile(cell)
        except Exception:
            return store.Solid("#210B16" if dark else "#FFF5F8")

    def slot_fill():
        """Empty slots reuse the same tiled look."""
        return panel_fill()

    def art_well_fill():
        if store.mas_globals.dark_mode:
            return store.Solid("#16080F")
        return store.Solid("#FFFFFF")

    def text_color():
        """Match the active MAS / Comfy UI button text color so labels stay readable."""
        dark = bool(getattr(store.mas_globals, "dark_mode", False))
        try:
            col = getattr(store.style.hkb_button_text, "color", None)
            if col:
                return col
        except Exception:
            pass
        return "#FFFFFF" if dark else "#2D1B24"

    def _abs(rel_path):
        return os.path.normpath(os.path.join(renpy.config.gamedir, rel_path.replace("/", os.sep)))

    def fitted(path, max_w, max_h):
        """Scale an image to fit inside max_w x max_h (Ren'Py 6.99 safe)."""
        if not path:
            return store.Null()

        try:
            w, h = renpy.image_size(path)
        except Exception:
            try:
                return store.im.Scale(path, max_w, max_h)
            except Exception:
                return store.Null()

        if w <= 0 or h <= 0:
            return store.Null()

        scale = min(float(max_w) / float(w), float(max_h) / float(h))
        nw = max(1, int(w * scale))
        nh = max(1, int(h * scale))

        try:
            return store.im.Scale(path, nw, nh)
        except Exception:
            return store.Null()

    def ensure_folders():
        for rel in (REL_ART, REL_KEPT):
            path = _abs(rel)
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except Exception:
                    pass

    def _added_timestamp(filename):
        """Return timestamp for when the file was added/updated in Art/."""
        path = _abs(art_rel_path(filename))
        try:
            return max(os.path.getctime(path), os.path.getmtime(path))
        except Exception:
            return 0.0

    def _sort_key(name):
        return (_added_timestamp(name), name.lower())

    def list_art_files():
        """Return PNG filenames in the Art inbox, ordered by date added."""
        ensure_folders()
        art_dir = _abs(REL_ART)
        if not os.path.isdir(art_dir):
            return []

        found = []
        try:
            for name in os.listdir(art_dir):
                full_path = os.path.join(art_dir, name)
                if os.path.isfile(full_path) and is_supported_art(name):
                    found.append(name)
        except Exception:
            return []

        found.sort(key=_sort_key)
        return found

    def kept_list():
        if store.persistent._showcase_kept is None:
            store.persistent._showcase_kept = []
        return list(store.persistent._showcase_kept)

    def shown_list():
        if store.persistent._showcase_shown is None:
            store.persistent._showcase_shown = []
        return list(store.persistent._showcase_shown)

    def is_kept(filename):
        return filename in kept_list()

    def is_shown(filename):
        return filename in shown_list()

    def mark_shown(filename):
        if store.persistent._showcase_shown is None:
            store.persistent._showcase_shown = []
        if filename not in store.persistent._showcase_shown:
            store.persistent._showcase_shown.append(filename)

    def list_new_art():
        """Art in the inbox that has not been shown to Monika yet."""
        return [name for name in list_art_files() if not is_shown(name)]

    def next_new_art():
        new = list_new_art()
        if not new:
            return None
        return new[0]

    def art_rel_path(filename):
        return REL_ART + "/" + filename

    def kept_rel_path(filename):
        return REL_KEPT + "/" + filename

    def display_path(filename):
        """Prefer kept copy; fall back to inbox."""
        kept = kept_rel_path(filename)
        if renpy.loadable(kept) or os.path.isfile(_abs(kept)):
            return kept
        return art_rel_path(filename)

    def loadable_image(filename):
        """Return a path Ren'Py can display for this art file."""
        candidates = []

        for rel in (kept_rel_path(filename), art_rel_path(filename)):
            candidates.append(rel)
            candidates.append(_abs(rel).replace("\\", "/"))

        for path in candidates:
            if renpy.loadable(path):
                return path
            if os.path.isfile(path):
                return path

        return None

    def keep_art(filename):
        """Copy inbox art into kept/ and record it in persistent."""
        ensure_folders()
        if is_kept(filename):
            return True

        src = _abs(art_rel_path(filename))
        dst = _abs(kept_rel_path(filename))

        if not os.path.isfile(src):
            if os.path.isfile(dst):
                if filename not in store.persistent._showcase_kept:
                    store.persistent._showcase_kept.append(filename)
                return True
            return False

        try:
            shutil.copy2(src, dst)
        except Exception:
            return False

        if filename not in store.persistent._showcase_kept:
            store.persistent._showcase_kept.append(filename)
        return True

    def remove_art(filename):
        """Remove a piece from the album (kept list + kept file copy)."""
        ensure_folders()

        if store.persistent._showcase_kept is None:
            store.persistent._showcase_kept = []
        if filename in store.persistent._showcase_kept:
            store.persistent._showcase_kept.remove(filename)

        if store.persistent._showcase_shown is None:
            store.persistent._showcase_shown = []
        if filename in store.persistent._showcase_shown:
            store.persistent._showcase_shown.remove(filename)

        kept_path = _abs(kept_rel_path(filename))
        if os.path.isfile(kept_path):
            try:
                os.remove(kept_path)
            except Exception:
                pass

        return True

    def adjacent_kept(filename, offset):
        items = kept_list()
        if not items or filename not in items:
            return None
        idx = items.index(filename) + offset
        if 0 <= idx < len(items):
            return items[idx]
        return None

    def album_pages(per_page=6):
        """Split kept art into pages of thumbnails."""
        items = kept_list()
        if not items:
            return [[]]

        pages = []
        for i in range(0, len(items), per_page):
            pages.append(items[i:i + per_page])
        return pages

    def art_folder_hint():
        return _abs(REL_ART)


init python:
    store.showcase.ensure_folders()
