import bpy
import af
import json

from bpy.props import StringProperty, IntProperty, CollectionProperty, EnumProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel

# -------------------------------------------------
# Global Variables
# -------------------------------------------------
render_clients = []
client_map = {}
selected_client = ''

# -------------------------------------------------
# Model Classes
# -------------------------------------------------
class AF_RenderClient():
    def __init__(self, hostname, engine, ip, port):
        self.hostname = hostname
        self.engine = engine
        self.ip = ip
        self.port = port
    
    @staticmethod
    def request_cgru_renderclients():
        client_list = []
        cmd = af.Cmd()
        clients = cmd.renderGetList()
        for client in clients:
            name = client['name']
            version = client['engine']
            address = client['address']
            ip = address['ip']
            port = address['port']

            print(name)
            print(version)
            print(ip)
            print(port)
            
            client_list.append(AF_RenderClient(name, version, ip, port))
        return client_list

class ListItem(PropertyGroup):
    """Group of properties representing an item in the list."""

    name = StringProperty(
           name="Name",
           description="A name for this item",
           default="Untitled")

    random_prop = StringProperty(
           name="Any other property you want",
           description="",
           default="")

# -------------------------------------------------
# Operators
# -------------------------------------------------
class LIST_OT_NewItem(Operator):
    """Add a new item to the list."""

    bl_idname = "my_list.new_item"
    bl_label = "Add a new item"

    def execute(self, context):
        item = context.scene.my_list.add()
        item.name = selected_client

        return{'FINISHED'}

class LIST_OT_DeleteItem(Operator):
    """Delete the selected item from the list."""

    bl_idname = "my_list.delete_item"
    bl_label = "Deletes an item"

    @classmethod
    def poll(cls, context):
        return context.scene.my_list

    def execute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index)
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1)

        return{'FINISHED'}

# -------------------------------------------------
# UI Classes
# -------------------------------------------------
class ExcludePanel(bpy.types.Panel):
    bl_label = "Exclude Hosts"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(context.scene, "dropdown_list")
        
        row = layout.row()
        row.template_list("MY_UL_List", "The_List", scene, "my_list", scene, "list_index")

        row = layout.row()
        row.operator('my_list.new_item', text='Add Renderclient', icon='ZOOMIN')
        row.operator('my_list.delete_item', text='Remove Renderclient', icon='ZOOMOUT')

        if scene.list_index >= 0 and scene.my_list:
            item = scene.my_list[scene.list_index]
            row = layout.row()
            row.prop(item, "name")
            row.prop(item, "random_property")

class MY_UL_List(UIList):
    """UIList of excluded renderclients"""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # We could write some code to decide which icon to use here...
        custom_icon = 'CONSOLE'

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name, icon = custom_icon)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon = custom_icon)

# -------------------------------------------------
# Callbacks
# -------------------------------------------------
def on_select_renderclient(self, context):
    selected_client = client_map[context.scene.dropdown_list]
    print('Selected Client: ' + selected_client)

# -------------------------------------------------
# Plugin Management
# -------------------------------------------------
def register():
    render_clients = AF_RenderClient.request_cgru_renderclients()
    
    bpy.utils.register_class(ListItem)
    bpy.utils.register_class(MY_UL_List)
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.utils.register_class(LIST_OT_DeleteItem)
    bpy.utils.register_class(ExcludePanel)

    bpy.types.Scene.my_list = CollectionProperty(type = ListItem)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list", default = 0)
    
    counter = 1
    dropdown_items = []
    for render_client in render_clients:
        dropdown_item = []
        dropdown_item.append(str(counter))
        dropdown_item.append(render_client.hostname + " (" + render_client.ip + ")")
        dropdown_item.append("CGRU Version " + render_client.engine)
        dropdown_items.append(tuple(dropdown_item))
        client_map[str(counter)] = render_client.ip
        if counter == 1:
            selected_client = render_client.ip
        counter += 1
    
    bpy.types.Scene.dropdown_list = EnumProperty(name="Render Clients:", items=tuple(dropdown_items), update=on_select_renderclient)
    
def unregister():
    del bpy.types.Scene.my_list
    del bpy.types.Scene.list_index

    bpy.utils.unregister_class(ListItem)
    bpy.utils.unregister_class(MY_UL_List)
    bpy.utils.unregister_class(LIST_OT_NewItem)
    bpy.utils.unregister_class(LIST_OT_DeleteItem)
    bpy.utils.unregister_class(ExcludePanel)

if __name__ == "__main__":
    register()