from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import SimultaneousActivation, RandomActivation
from mesa.space import Grid

from .cell import Cell


class EpiDyn(Model):
    '''
    Represents the 2-dimensional model for epidemic dynamics
    '''
    
    schedule_types = {"Random": RandomActivation,
                      "Simultaneous": SimultaneousActivation}
    
    def __init__(self, height=100, width=100, dummy="", schedule_type="Simultaneous",startblock=1, density=0.1, p_infect=0.25, p_death=0.0, spatial=1, groupsize=4, quarantine_delay=7, neighbourdic={}, groupswitch=True, switchperx=2):
        '''
        Create the CA field with (height, width) cells.
        '''
        #setting an explicit seed allows you to reproduce interesting runs
        #self.random.seed(30)
        
        # Set up the grid and schedule.
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self)
        self.neighbourdic = neighbourdic
        self.quarantine_delay = quarantine_delay
        self.groupswitch = groupswitch
        self.switchperx = switchperx
        self.counter = 0
        
        # Use a simple grid, where edges wrap around.
        self.grid = Grid(height, width, torus=True)
        self.datacollector = DataCollector(
            {"Infectious": lambda m: self.count_infectious(m,width*height),
             "Removed": lambda m: self.count_removed(m,width*height),
             "Exposed": lambda m: self.count_removed(m,width*height)})

        # Place a cell at each location, with default SENSTIVE,
        # and some (a 2x2 block) initialized to INFECTIOUS
        
        for (contents, x, y) in self.grid.coord_iter():
            cell = Cell((x, y), self, spatial, unique_id=int(0.5 * (x + y) * (x + y + 1) + y))
            cell.state = cell.SENSITIVE
            cell.p_infect = p_infect
            cell.p_death = p_death
            cell.groupsize = groupsize
            if startblock:
                if ((x == height/2 or x == height/2+1) and  (y == height/2 or y == height/2+1)):
                    cell.state = cell.INFECTIOUS
            elif self.random.random() < density:
                    cell.state = cell.INFECTIOUS
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        self.measure_CA = []
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        '''
        Have the scheduler advance each cell by one step
        '''
        #Need this seperately so the Reset button works fo no group switches
        if self.counter == 0:
            self.neighbourdic.clear()
        
        if (self.counter - self.quarantine_delay) % self.switchperx == 0:
            if self.groupswitch == 1:
                self.neighbourdic.clear()
        
        self.measure_CA = [a for a in self.schedule.agents]
        self.schedule.step()
               # collect data
        self.datacollector.collect(self)
        
        self.counter = self.counter + 1

    @staticmethod
    def count_infectious(model,grid_size):
        """
        Helper method to count cells in a given state in a given model.
        """
        list_state = [a for a in model.schedule.agents if a.state == a.INFECTIOUS]
        return len(list_state)/grid_size

    @staticmethod
    def count_removed(model,grid_size):
        """
        Helper method to count cells in a given state in a given model.
        """
        list_state = [a for a in model.schedule.agents if a.state == a.REMOVED]
        return len(list_state)/grid_size

    @staticmethod
    def count_exposed(model,grid_size):
        """
        Helper method to count cells in a given state in a given model.
        """
        list_state = [a for a in model.schedule.agents if a.state == a.NEIGHBOUR]
        return len(list_state)/grid_size
