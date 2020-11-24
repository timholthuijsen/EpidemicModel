from mesa import Agent
import numpy as np
import random as rd


class Cell(Agent):
    '''Represents a single individual in the simulation.'''

    SENSITIVE = 0
    INFECTIOUS = 1
    REMOVED = 2
    NEIGHBOUR = 3

    def __init__(self, pos, model, spatial, unique_id, init_state=SENSITIVE):
        '''
        Create a cell, in the given state, at the given x, y position.
        '''
        super().__init__(pos, model)
        self.x, self.y = pos
        self.spatial = spatial
        self.unique_id = unique_id
        self.state = init_state
        self._nextState = None

    @property
    def isInfectious(self):
        return self.state == self.INFECTIOUS
    
    @property
    def isNeighbour(self):
        return self.state == self.NEIGHBOUR

    @property
    def isSensitive(self):
        return self.state == self.SENSITIVE

    @property
    def neighbours(self):
        return self.model.grid.neighbor_iter((self.x, self.y), True)

    def newneighbours(self, amount):
        for neighbour in self.neighbourhood:
            if neighbour.unique_id in self.model.neighbourdic:
                if len(self.model.neighbourdic[neighbour.unique_id]) >= self.groupsize:
                    self.neighbourhood.remove(neighbour)
        if self.neighbourhood:
            if len(self.neighbourhood) > amount:
                self.newneighbourlist = rd.choices(self.neighbourhood, k=amount)
            else:
                self.newneighbourlist = self.neighbourhood
            for newneighbour in self.newneighbourlist:
                if newneighbour in self.model.neighbourdic:
                    self.model.neighbourdic[newneighbour.unique_id].append(self)
                else:
                    self.model.neighbourdic[newneighbour.unique_id] = [self]
            return self.newneighbourlist
        else:
            return []

    def step(self):
        
        '''
        Compute if the cell will be INFECTIOUS or REMOVED at the next tick.
        With simultaneous updating, he state is not changed here,
        but is just computed and stored in self._nextState,
        because the current state may still be necessary for our neighbors
        to calculate their next state.
        '''

        # Get the neighbors and apply the rules on whether to be INFECTIOUS or SENSITIVE
        # at the next tick.
        #In order to use our newneigbours list, we need to get it compatitable with the way 
        #in which mesa defines a neigbourhood here
        if self.spatial:
            self.neighbourhood = self.model.grid.iter_neighborhood(self.pos, moore=True, radius=2)
            self.neighbourhood = self.model.grid.get_cell_list_contents(self.neighbourhood)

        # In the non-spatial setting, th he next function is using random cells instead
        # neigboring cells;  in this way "mean field" is simulated

        else:
            self.neighbourhood = rd.sample(self.model.measure_CA, self.groupsize)
            
        if self.model.counter >= self.model.quarantine_delay:
            if self.model.groupswitch == True or self.model.counter == self.model.quarantine_delay:
                if (self.model.counter - self.model.quarantine_delay) % self.model.switchperx == 0: 
                    if self.unique_id in self.model.neighbourdic:
                        if len(self.model.neighbourdic[self.unique_id]) < self.groupsize:
                            neighboursrequired = self.groupsize - len(self.model.neighbourdic[self.unique_id])
                            for newneighbour in self.newneighbours(neighboursrequired):
                                self.model.neighbourdic[self.unique_id].append(newneighbour)
                    else:
                        self.model.neighbourdic[self.unique_id] = self.newneighbours(self.groupsize)
        
                    self.smallerneighbourhood = self.model.neighbourdic[self.unique_id]
        else:
            self.smallerneighbourhood = self.neighbourhood
        self.rd_neighbour = rd.choice(self.smallerneighbourhood)
        # Assuming default nextState is unchanged
        # Check if state will be changed
        if self.isNeighbour:
           self.state = self.SENSITIVE
           
        self._nextState = self.state
            
        if self.isSensitive:
            for neighbour in self.smallerneighbourhood:
                    if neighbour.isInfectious:
                        self._nextState = self.NEIGHBOUR
            if self.rd_neighbour.state == self.rd_neighbour.INFECTIOUS:
                if np.random.random() < self.p_infect:
                    self._nextState = self.INFECTIOUS
        
        if self.isInfectious:
            if np.random.random() < self.p_death:
                self._nextState = self.REMOVED

        if self.model.schedule_type == "Random":
            self.advance()

    def advance(self):
        '''
        Simultaneously set the state to the new computed state -- computed in step().
        '''
        self.state = self._nextState
        

