# Showcase — Header
# v1.2.0
# By Natashenka

init -990 python in mas_submod_utils:
    Submod(
        author="Natashenka",
        name="Showcase",
        version="1.2.0",
        description="Show Monika images and keep them in an album!",
    )


init 5 python in mas_bookmarks_derand:
    label_prefix_map["showcase_"] = label_prefix_map["monika_"]
