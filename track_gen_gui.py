import PySimpleGUI
from os import system
from time import sleep


def main():
    global window
    PySimpleGUI.theme("SystemDefaultForReal")

    layout = [[PySimpleGUI.Text("Track Length: "), PySimpleGUI.Slider(range=(1,30000), default_value=5000, key="track_length_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Track Width: "), PySimpleGUI.Slider(range=(1,100),default_value=8, key="track_width_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Track Start Height: "), PySimpleGUI.Slider(range=(1,500),default_value=100, key="track_height_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Short Straight Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=1, key="short_straight_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Long Straight Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=1, key="long_straight_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Short Turn Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=4, key="short_turn_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Long Turn Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=1, key="long_turn_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Track Length Percent Multiplier: "), PySimpleGUI.Slider(range=(100,1000), default_value=100, key = "track_length_multiplier_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Height Multiplier: "), PySimpleGUI.Slider(range=(0,1000), default_value=100, key="height_multiplier_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Chance of Height Change: "), PySimpleGUI.Slider(range=(0,100), default_value=33, key="height_chance_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Track Texture: "), PySimpleGUI.DropDown(values=["base","sand","mud","grass","ice"], default_value="base", key="track_texture_dropdown", enable_events=True), PySimpleGUI.Text("Track Material: "), PySimpleGUI.DropDown(values=['SAND', 'MUD', 'GRASS', 'ASPHALT', 'CONCRETE', 'ICE', 'DIRT', 'ASPHALT_PREPPED', 'ASPHALT_WET'], default_value="ASPHALT", key="track_materials_dropdown", enable_events=True)],
              [PySimpleGUI.Text("Preset (piece height and distribution parameters will have no effect): "), PySimpleGUI.DropDown(values=["", "highway", "rally", "normal", "bumpy", "hillclimb", "racetrack", "drift"], default_value="", key="preset_dropdown", enable_events=True)],
              [PySimpleGUI.Text("Center Mesh Type: "), PySimpleGUI.DropDown(values=['regular', 'flat'], default_value='regular', key="center_mesh_dropdown", enable_events=True), PySimpleGUI.Text("Side Mesh Type: "), PySimpleGUI.DropDown(values=['regular', 'bevel', 'wideBevel', 'highBevel', 'smallDiagonal', 'bigDiagonal', 'rail', 'none', 'smoothedRect', 'racetrack'], default_value="smallDiagonal", key="side_mesh_dropdown", enable_events=True)],
              [PySimpleGUI.Text("Track Name: "), PySimpleGUI.Input("Atompunk78's_autogen_track", justification='left',key="track_name_input", enable_events=True)],
              [PySimpleGUI.Text("Overwrite Existing Track:"), PySimpleGUI.Checkbox(text=" ", default=True, key="overwrite_track_checkbox", enable_events=True), PySimpleGUI.Text("Enable Overlap Detection:"), PySimpleGUI.Checkbox(text="", default=True, key="overlap_detection_checkbox", enable_events=True)],
              [PySimpleGUI.Button('Generate Track', key="generate_track_button", enable_events=True)],
              [PySimpleGUI.Text("Track Generated with exit code: "),PySimpleGUI.Output(size=(50,2), key="output")]
              ]

    window = PySimpleGUI.Window("Beamng Track Generator", layout=layout, size=(500,725))

    while True:
        event, values = window.read()
        
        if event == "generate_track_button":
            generate_track(values)

        if event == PySimpleGUI.WIN_CLOSED:
            window.close()
            exit()

def generate_track(params):
    if params["track_length_slider"]> 9999 or params["preset_dropdown"] == "drift":
        PySimpleGUI.popup_quick_message("long track/drift preset detected, be prepared to wait, program hang is normal", background_color="black", text_color="white", non_blocking=True)
    dot = ""
    dod= ""
    preset= ""
    step=1
    increment=5
    if params["overwrite_track_checkbox"] == False:
        dot = "-dot"
    if params["overlap_detection_checkbox"] == False:
        dod = "-dod"
    if params["preset_dropdown"] != "":
        preset = "-p="+params["preset_dropdown"]

    if params["track_length_slider"] > 20000:
        step =4
        increment=20
    elif params["track_length_slider"] >10000 or params["preset_dropdown"] == "drift":
        step =2
        increment=10

    command = f"python main_cli.py -tl={int(params['track_length_slider'])} -tw={int(params['track_width_slider'])} -sh={int(params['track_height_slider'])} -ssd={int(params['short_straight_distro'])} -lsd={int(params['long_straight_distro'])} -std={int(params['short_turn_distro'])} -ltd={int(params['long_turn_distro'])} -tn={params['track_name_input']} {dot} -hm={int(params['height_multiplier_slider'])} -hcc={int(params['height_chance_slider'])} -tt={params['track_texture_dropdown']} -tm={params['track_materials_dropdown']} {preset} {dod} -step={step} -inc={increment} -v -cmt={params['center_mesh_dropdown']} -smt={params['side_mesh_dropdown']} -tlm={int(params['track_length_multiplier_slider'])}"

    print(system(command))

main()