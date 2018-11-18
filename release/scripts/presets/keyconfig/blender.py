import os
import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
)

userpref = bpy.context.user_preferences

idname = os.path.splitext(os.path.basename(__file__))[0]

def update(_self, _context):
    _load()


class Prefs(bpy.types.KeyConfigPreferences):
    bl_idname = idname

    spacebar_action: EnumProperty(
        name="Spacebar",
        items=(
            ('TOOL', "Tool-Bar",
             "Open the popup tool-bar\n"
             "When 'Space' is held and used as a modifier:\n"
             "\u2022 Pressing the tools binding key switches to it immediately.\n"
             "\u2022 Dragging the cursor over a tool and releasing activates it (like a pie menu).\n"
            ),
            ('PLAY', "Playback",
             "Toggle animation playback"
            ),
        ),
        description=(
            "Action when 'Space' is pressed ('Shift-Space' is used for the other action)"
        ),
        default='TOOL',
        update=update,
    )
    use_select_all_toggle: BoolProperty(
        name="Select All Toggles",
        description=(
            "Causes select-all (A-key) to de-select in the case a selection exists"
        ),
        default=False,
        update=update,
    )

    def draw(self, layout):
        col = layout.column(align=True)
        col.label(text="Spacebar Action:")
        col.row().prop(self, "spacebar_action", expand=True)
        layout.prop(self, "use_select_all_toggle")


from bpy_extras.keyconfig_utils import (
    keyconfig_init_from_data,
    keyconfig_module_from_preset,
)

mod = keyconfig_module_from_preset(os.path.join("keymap_data", "blender_default"), __file__)

def _load():
    kc = bpy.context.window_manager.keyconfigs.new(idname)
    kc_prefs = kc.preferences

    keyconfig_data = mod.generate_keymaps(
        mod.KeymapParams(
            select_mouse=userpref.inputs.select_mouse,
            spacebar_action=kc_prefs.spacebar_action,
            use_select_all_toggle=kc_prefs.use_select_all_toggle,
        ),
    )
    keyconfig_init_from_data(kc, keyconfig_data)
    kc.has_select_mouse = True  # Support switching select mouse


if __name__ == "__main__":
    bpy.utils.register_class(Prefs)
    _load()
