# Pyngine
Python 3 library utilizing Pygame for visualizations, guis, and games.

# Examples
Within the ~/examples directory
## Lables and Buttons
![Labels and Buttons](/images/labels_buttons.png)

## Textboxes
![Textboxes](/images/textboxes.png)

## Loading Bars
![Loading Bars](/images/loading_bars.png)

## Hot Keys
![Hot Keys](/images/hot_keys.png)

## Related Projects
[Pyngine First Person Maze](https://github.com/JacobLondon/first)

[Pyngine Rasterizer](https://github.com/JacobLondon/rasterization)

[Pyngine  Connect Four](https://github.com/JacobLondon/ConnectFour)

[Pyngine Multiplayer Game](https://github.com/JacobLondon/PeoplePlayingGames)
# GUI
Built into Pyngine, the following components allow for easy component implementation.
- panels, labels
- textboxes, imageboxes, listboxes
- buttons, progress bars
- custom layouts for scaling screen sizes
- simple z-index placement of components

## Input
Easily interface with Pygame to capture keyboard and mouse inputs.

## Pre-built Conveniences
- Define grids for relative component placement
- Draw using Pygame's or build in Painter functions at z-indices using Drawers
- Measure real frame time
- Built in colors

## Todo
- Example for each component
- Example for drawers utilizing painters
- multiline textbox option
- gui for building guis
- save controller formats to json
- load controller formats from json

## Known Issues
- Bar component does not always fill up to 100% when finished
