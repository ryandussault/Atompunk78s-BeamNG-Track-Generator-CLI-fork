Hi! Welcome to Atompunk78's BeamNG Track Generator, modified for ease of use by ryandussault, I hope you enjoy it!

To use the program:
 -open track editor on gridmap
 -win+r a cmd terminal and cd into the folder containing the scipts
 -run using python ('python track_gen_gui.py')
 -load the track into track editor
 -enjoy (or dont)

 ps: an exit code of zero in the gui output box means the script ran successfully, anything else is an error
 
This will generate one track with the default parameters. You don't need to reboot BeamNG to load a new generated track if the file name is the same as the old one.
You can change the type of track it generates by changing 'trackType' in the config file to the name of any file in the 'Presets' folder, or make your own preset by creating one or editing the 'custom' preset.

If you want to generate multiple tracks at once, pass in '-dot' (don't overwrite track, only when using the cli version) then run the program multiple times.
The gui version will generate a new track everytime the button is pressed
Occasionally the generated tracks will cross over themselves (or otherwise be invalid), if this happens just generate a new one.
The tracks are designed to be played on Small Grid Map rather than the default Glow City.
If you're struggling with anything message me and I'll almost certainly be able to help.

Kindly note there's a licence attached to the program. It basically says:
 - You can freely distribute and modify it as long as you give credit
 - You can't profit off of it

I'm flexible on these, so if the above is a problem just send me a message!

I hope you like the program, have fun :)

Prerequisites:
 -Python 3.10 (or higher might work might not)
 -PySimpleGui (for the gui wrapper)
