# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 17:44:14 2015

@author: Natalie
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 03 11:15:49 2015

@author: Natalie
"""

# TODO: Check number of changes: just cumulativ??
# TODO: Adapt rules
# Initialize CA
from Grid import Grid 
from CellularAutomata import CellularAutomata

# NUMBER OF GENERATIONS
generations = 50 # number of generations

# IMAGE FILES
fname = 'milford1971_21.jpg'
ref_name = 'milford1999_21.jpg'
#ref_name = 'milford1999_21.jpg'
simulation = False;

# generate grid
grid = Grid()

if simulation:
    # generate random grid with size m
    grid.rndGenerator(grid_size=250, savePlots=False, name='rnd_simulation')
else:
    # load Image to grid
    grid.image2Grid(fname, path='Images\\', mode='yuv', output=False, ext_colors=True)

# save initial state
init = grid.grid.copy()
# Create CA with reference image
ca = CellularAutomata(grid, neighbourhood='Moore', rules='Conway', ref_name=ref_name)

print 'intial state: '
ca.grid.visualize()

for gen in range(1,generations+1):
    
    # update grid and save number of changes
    curr = ca.grid.grid.copy();   
    ca.update()    
    ca.gridDifference(curr)   
    ca.rmsd_dist()

    
    if gen%5==0:
        # compute distance between current image and target
        ca.emd_dist(gen)

        print "generation:", gen, " changes:", ca.changes[-1], " emd_dist:", ca.emd[-1], " rmsd: :", ca.rmsd[-1]
        ca.grid.visualize()

ca.gridDifference(ca.ref_grid.grid)
ca.saveEMD()
ca.saveChanges()