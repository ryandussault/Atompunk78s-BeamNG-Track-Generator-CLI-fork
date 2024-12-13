import PySimpleGUI
from os import system, path


def main():
    PySimpleGUI.theme("SystemDefaultForReal")

    layout = [[PySimpleGUI.Text("Track Length: "), PySimpleGUI.Slider(range=(1,5000), default_value=1000, key="track_length_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Track Width: "), PySimpleGUI.Slider(range=(1,100),default_value=8, key="track_width_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Track Start Height: "), PySimpleGUI.Slider(range=(1,500),default_value=100, key="track_height_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Short Straight Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=1, key="short_straight_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Long Straight Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=1, key="long_straight_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Short Turn Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=4, key="short_turn_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Long Turn Tile Type Distribution: "), PySimpleGUI.Slider(range=(0,100), default_value=1, key="long_turn_distro", enable_events=True, orientation='horizontal')],
              [PySimpleGUI.Text("Height Multiplier: "), PySimpleGUI.Slider(range=(0,1000), default_value=100, key="height_multiplier_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Chance of Height Change: "), PySimpleGUI.Slider(range=(0,100), default_value=33, key="height_chance_slider", enable_events=True, orientation="horizontal")],
              [PySimpleGUI.Text("Track Texture: "), PySimpleGUI.DropDown(values=["base","sand","mud","grass","ice"], default_value="base", key="track_texture_dropdown", enable_events=True), PySimpleGUI.Text("Track Material: "), PySimpleGUI.DropDown(values=['SAND', 'MUD', 'GRASS', 'ASPHALT', 'CONCRETE', 'ICE', 'DIRT', 'ASPHALT_PREPPED', 'ASPHALT_WET'], default_value="ASPHALT", key="track_materials_dropdown", enable_events=True)],
              [PySimpleGUI.Text("Preset (Other params have no effect when a preset is selected): "), PySimpleGUI.DropDown(values=["", "highway", "rally", "normal", "bumpy", "hillclimb", "racetrack", "drift"], default_value="", key="preset_dropdown", enable_events=True)],
              [PySimpleGUI.Text("Track Name: "), PySimpleGUI.Input("Atompunk78's_autogen_track", justification='left',key="track_name_input", enable_events=True)],
              [PySimpleGUI.Text("Overwrite Existing Track:"), PySimpleGUI.Checkbox(text=" ", default=True, key="overwrite_track_checkbox", enable_events=True), PySimpleGUI.Text("Enable Overlap Detection:"), PySimpleGUI.Checkbox(text="", default=True, key="overlap_detection_checkbox", enable_events=True)],
              [PySimpleGUI.Button('Generate Track', key="generate_track_button", enable_events=True)],
              [PySimpleGUI.Text("Track Generated with exit code: "),PySimpleGUI.Output(size=(50,2), key="output")]
              ]

    window = PySimpleGUI.Window("Beamng Track Generator", layout=layout, size=(500,650))

    while True:
        event, values = window.read()
        
        if event == "generate_track_button":
            generate_track(values)

        if event == PySimpleGUI.WIN_CLOSED:
            window.close()
            exit()

def generate_track(params):
    dot = ""
    dod= ""
    preset= ""
    if params["overwrite_track_checkbox"] == False:
        dot = "-dot"
    if params["overlap_detection_checkbox"] == False:
        dod = "-dod"
    if params["preset_dropdown"] != "":
        preset = "-p="+params["preset_dropdown"]

    command = f"python main_cli.py -tl={int(params['track_length_slider'])} -tw={int(params['track_width_slider'])} -sh={int(params['track_height_slider'])} -ssd={int(params['short_straight_distro'])} -lsd={int(params['long_straight_distro'])} -std={int(params['short_turn_distro'])} -ltd={int(params['long_turn_distro'])} -tn={params['track_name_input']} {dot} -hm={int(params['height_multiplier_slider'])} -hcc={int(params['height_chance_slider'])} -tt={params['track_texture_dropdown']} -tm={params['track_materials_dropdown']} {preset} {dod}"

    print(system(command))


main()