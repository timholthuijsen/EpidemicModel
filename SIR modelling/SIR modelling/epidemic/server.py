from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


from .model import EpiDyn

COLORS = ['White', 'Red', 'Blue', 'Yellow']

def portrayCell(cell):
    '''
        This function is registered with the visualization server to be called
        each tick to indicate how to draw the cell in its current state.
        :param cell:  the cell in the simulation
        :return: the portrayal dictionary.
        '''
    if cell is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0, "x": cell.x, "y": cell.y}
    portrayal["Color"] = COLORS[cell.state]
    return portrayal

# Make a world that is 100x100, on a 500x500 display.
canvas_element = CanvasGrid(portrayCell, 100, 100, 500, 500)
cell_chart = ChartModule([{"Label": "Infectious", "Color": 'Red'},
                          {"Label": "Removed", "Color": 'Blue'}],
                         canvas_height=500, canvas_width=1000)

model_params = {
    "height": 100,
    "width": 100,
    "dummy": UserSettableParameter("static_text", value = "NB. Use 'Reset'-button to activate new model settings"),
    "schedule_type": UserSettableParameter("choice", "Scheduler type", value="Simultaneous", choices=list(EpiDyn.schedule_types.keys())),
    "startblock": UserSettableParameter("checkbox", "2x2 block start (or random)", value=True),
    "density": UserSettableParameter("slider", "Initial random density", 0.5, 0., 1.0, 0.001),
    "groupsize": UserSettableParameter("slider", "Groupsize", 3, 0, 25, 1),
    "quarantine_delay": UserSettableParameter("slider", "Quarantine Delay", 25, 0, 25, 1),
    "groupswitch": UserSettableParameter("checkbox", "Allow groupswitch (or not)", value=True),
    "switchperx": UserSettableParameter("slider", "Switches groups every x", 10, 1, 25, 1),
    "p_infect": UserSettableParameter("slider", "Probability of Infection", 0.25, 0.00, 1.0, 0.01),
    "p_death": UserSettableParameter("slider", "Probability of Removal", 0.07, 0.00, 1.0, 0.01),
    "spatial": UserSettableParameter("checkbox", "Spatial", value=True),}

 
server = ModularServer(EpiDyn, [canvas_element, cell_chart], "Epidemic Dynamics",  model_params)

