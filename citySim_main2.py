# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:18:40 2015

@author: Natalie
"""

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
generations = 10 # number of generations

# IMAGE FILES
fname = 'milford1971_21.jpg'
ref_name = 'milford1999_21.jpg'
#ref_name = 'milford1999_21.jpg'
simulation = False;

# generate grid
prob_grid1 = Grid(add='prob_')
prob_grid2 = Grid(add='prob_')
grid1 = Grid()
grid2 = Grid()
#grid = Grid()

if simulation:
    # generate random grid with size m
    grid1.rndGenerator(grid_size=250, savePlots=False, name='rnd_simulation')
else:
    # load Image to grid
    grid1.image2Grid(fname, path='Images\\', mode='yuv', output=False, ext_colors=False)
    grid2.image2Grid(fname, path='Images\\', mode='yuv', output=False, ext_colors=True)
    prob_grid1.image2Grid(fname, path='Images\\', mode='yuv', output=False, ext_colors=False)
    prob_grid2.image2Grid(fname, path='Images\\', mode='yuv', output=False, ext_colors=True)

# save initial state
#init = grid.grid.copy()
# Create CA with reference image
ca = CellularAutomata(prob_grid2, neighbourhood='Moore', rules='Conway', ref_name=ref_name)
#ca2 = CellularAutomata(grid2, neighbourhood='Moore', rules='Probabilistic', ref_name=ref_name)
#ca3 = CellularAutomata(prob_grid1, neighbourhood='Moore', rules='Conway', ref_name=ref_name)
#ca4 = CellularAutomata(prob_grid2, neighbourhood='Moore', rules='Probabilistic', ref_name=ref_name)

print 'intial state: '
ca.grid.visualize()
#ca1.grid.saveImage(path='EMDimages\\')
#ca2.grid.saveImage(path='EMDimages\\')
#ca3.grid.saveImage(path='EMDimages\\')
#ca4.grid.saveImage(path='EMDimages\\')

for gen in range(1,generations+1):
    
    # update grid and save number of changes
    curr = ca.grid.grid.copy();
    #curr1 = ca1.grid.grid.copy();
    #curr2 = ca2.grid.grid.copy();
    #curr3 = ca3.grid.grid.copy();
    #curr4 = ca4.grid.grid.copy();
    
    ca.update()
    
    #ca1.update()
    #ca2.update()
    ca3.update()    
    ca4.update()
    
    
    ca.gridDifference(curr)
    
    ca1.gridDifference(curr1)
    ca2.gridDifference(curr2)
    ca3.gridDifference(curr3)
    ca4.gridDifference(curr4)
    
    ca.rmsd_dist()
    
    ca1.rmsd_dist()
    ca2.rmsd_dist()
    ca3.rmsd_dist()
    ca4.rmsd_dist()
    
    if gen%5==0:
        # compute distance between current image and target
        #ca.emd_dist(gen)

        ca1.emd_dist(gen)
        ca2.emd_dist(gen)
        ca3.emd_dist(gen)
        ca4.emd_dist(gen)
        
        #print "generation:", gen, " changes:", ca.changes[-1], " emd_dist:", ca.emd[-1], " rmsd: :", ca.rmsd[-1]
        #ca.grid.visualize()

#ca.gridDifference(ca.ref_grid.grid)

ca1.gridDifference(ca1.ref_grid.grid)
ca2.gridDifference(ca2.ref_grid.grid)
ca3.gridDifference(ca3.ref_grid.grid)
ca4.gridDifference(ca4.ref_grid.grid)

ca.saveEMD()
ca.saveChanges()