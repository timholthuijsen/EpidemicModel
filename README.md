3 First points of interest:
1. Make the model choose appropriate neighbours (Done by Tom)
    Updated the model.py file to include a neighbourdic in its initialization and added a unique_id to the initialization of the cells so we can easily track them when we put them in the neighbourdic.
    (In model.py in the step case the neighbourdic gets cleared every step, we want this whole thing eventually to happen only every couple of steps)

    In cell.py I added the newneighbours function that tries to supply a list of new neighbours for a cell based on whether the neighbours already have 4 (this is an arbitrary number we want to be able to change with a slider in the future) neighbours. This function also updates those neighbours in the neighbourdic so the connection made between the cells is a 2 way connection.
    
2. Make a function to modify neighbourhood after an x number of steps
    Step two should be rather straightforward by using the newneighbours function from Tom once step reaches a certain number, but we need     to find a way to format this newneighbours list in a way compatible with mesa. The way mesa identifies a cell's neighbourhood now         looks like this:
    self.neighbourhood = self.model.grid.iter_neighborhood(self.pos, moore=True, radius=2)
    self.neighbourhood = self.model.grid.get_cell_list_contents(self.neighbourhood)
 
3. Create a slider for step 2
    I created 2 variables with corresponding sliders in order to determine the days until quarantine starts in an experiment and how large     social groups will be once quarantine has started. The variable "groupsize" can simply be used as the "amount" variable in the             newneighbours function, and the "quarantine_delay" variable needs to be the number of timesteps until which newneighbours takes effect
