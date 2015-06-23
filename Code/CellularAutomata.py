# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 14:32:42 2015

@author: Natalie
"""

from Grid import Grid
import EMD_hist
import numpy as np
from matplotlib import pyplot as plt
import random as rnd
from numpy import mean, sqrt, square

class CellularAutomata():

    # Initialize the CA
    def __init__(self, grid, neighbourhood='Moore', rules='Probabilistic', ref_name='test.jpg'):
        self.grid = grid
        self.neighbourhood = neighbourhood
        self.rules = rules
        self.ref_name = ref_name
        self.ref_grid = self.loadReferenceImage(path='')
        self.emd = list()
        self.changes = list()
        self.diff = -1
        self.rmsd = list()
    
    # Update all cells in CA
    def update(self):
        
        for i in range(1,self.grid.grid_size+1):
            for j in range(1,self.grid.grid_size+1):
                
                # current cell state
                c = self.grid.grid.item(i,j)                
                # get specified neighbourhood
                neighbours = self.grid.getNeighbours( (i,j), neighbourhood='Moore')
                
                # count number of neighbour category
                res_neigh = neighbours[neighbours==self.grid.lu_values['residential']].size
                comc_neigh = neighbours[neighbours==self.grid.lu_values['comercial']].size
                ind_neigh = neighbours[neighbours==self.grid.lu_values['industrial']].size
                high_neigh = neighbours[neighbours==self.grid.lu_values['highway']].size
                road_neigh = neighbours[neighbours==self.grid.lu_values['road']].size
                sea_neigh= neighbours[neighbours==self.grid.lu_values['sea']].size
                forest_neigh= neighbours[neighbours==self.grid.lu_values['forest']].size
                
                if self.grid.ext_color:
                    recreation_neigh = neighbours[neighbours==self.grid.lu_values['recreation']].size
                    open_land_neigh = neighbours[neighbours==self.grid.lu_values['open_land']].size
                    mining_neigh = neighbours[neighbours==self.grid.lu_values['mining']].size
                    urban_open_neigh = neighbours[neighbours==self.grid.lu_values['urban_open']].size
    
                
                # update grid
                if self.rules=='Conway':
                    # update for free space
                    if c==0:
                        if ind_neigh==0 and sea_neigh==0 and forest_neigh==0:
                            # change to residential if there is no unavailable space
                            if res_neigh >= 3:
                                self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                            if comc_neigh >=3:
                                self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];    
                            if (road_neigh >= 1 or high_neigh>=1) and comc_neigh>=1:
                                self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];    
                            # change to residential if there is at least one residential
                            # and one road
                            if res_neigh >= 1 and road_neigh>=1:
                                self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                            
                    # update for forest
                    if c==31: #and ind_neigh==0:
                        if high_neigh>=1 and comc_neigh==4:
                            self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];    
                        if res_neigh==4:
                            self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                            
                    # update unavailable space
                    if (c==10 or c==11) and ind_neigh==0:
                        # dominanting comercial vs residential neighbourhood determines state
                        if res_neigh > comc_neigh:
                            self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                        if res_neigh < comc_neigh:
                            self.grid.grid[(i,j)] = self.grid.lu_values['comercial']; 
                            
                
                elif self.rules=='Probabilistic':
                    # update for free space
                    p = rnd.random()
                    if c==0:
                        if ind_neigh==0 and sea_neigh==0 and forest_neigh==0 or p<0.2:
                            # change to residential if there is no unavailable space
                            p = rnd.random()
                            if res_neigh >= 3 and p<0.75:
                                self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                            if comc_neigh >=3 and p<0.75:
                                self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];    
                            if (road_neigh >= 1 or high_neigh>=1) and comc_neigh>=1 and p<0.75:
                                self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];    
                            # change to residential if there is at least one residential
                            # and one road
                            if res_neigh >= 1 and road_neigh>=1 and p<0.75:
                                self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                            
                    # update for forest
                    if c==31: #and ind_neigh==0:
                        if (high_neigh>=1 and comc_neigh==4) or (comc_neigh>=2 and p<0.05):
                            self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];    
                        if res_neigh==4 or (p<0.05 and res_neigh>=2):
                            self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                            
                    # update unavailable space
                    if (c==10 or c==11) and (ind_neigh==0 or p<0.05):
                        # dominanting comercial vs residential neighbourhood determines state
                        if res_neigh > comc_neigh:
                            self.grid.grid[(i,j)] = self.grid.lu_values['residential'];    
                        if res_neigh < comc_neigh:
                            self.grid.grid[(i,j)] = self.grid.lu_values['comercial'];
                            
                
                if self.grid.ext_color:
                    # update for free space
                    if c==0:
                        if ind_neigh==0 and sea_neigh==0 and forest_neigh==0:
                            #change to urban open if at least  urban open
                            if urban_open_neigh >= 3:
                                self.grid.grid[(i,j)] = self.grid.lu_values['urban_open'];  
                            if open_land_neigh >= 3:
                                self.grid.grid[(i,j)] = self.grid.lu_values['open_land']; 
                                                            
                    # update for forest
                    if c==31: #and ind_neigh==0:
                        if recreation_neigh >=3:
                            self.grid.grid[(i,j)] = self.grid.lu_values['recreation']
                            
                    #update recreation 
                    if c==51:
                        if recreation_neigh >= forest_neigh:
                            self.grid.grid[(i,j)] = self.grid.lu_values['recreation']
                        if recreation_neigh >= open_land_neigh:
                            self.grid.grid[(i,j)] = self.grid.lu_values['recreation']
                            
                    #update open land
                    if c==40:
                        if  road_neigh ==4 and (comc_neigh >=1 or ind_neigh >=1 or res_neigh >= 1):
                              self.grid.grid[(i,j)] = self.grid.lu_values['road']

            
    # load a reference image to grid
    def loadReferenceImage(self, path = ''):
        ref_grid = Grid()
        #if self.grid.ext_color:
            #self.ref_name = 'ext_'+self.ref_name
        ref_grid.image2Grid(path+self.ref_name, ext_colors=self.grid.ext_color)
        ref_grid.visualize()
        return ref_grid
        
    # determine the differnce between to grids
    def gridDifference(self,ref):       
        diffImg = np.where((self.grid.grid==ref)==False)      
        self.changes.append(len(diffImg[0]))
        self.diff = len(diffImg[0])
    
    # compute earth movers distance of reference and grid    
    def emd_dist(self,gen):
        self.emd.append(EMD_hist.emd_grid(self,gen))
        
    # square root mean error
    def rmsd_dist(self):
        diff = np.reshape(self.ref_grid.grid - self.grid.grid,-1)
        self.rmsd.append(sqrt(mean(square(diff))))
        
    def saveEMD(self, path='result\\'):
        
        plt.plot(self.emd)
        plt.ylabel('EMD')
        plt.xlabel('Generations in steps of 5')
        plt.savefig(path+'emd_'+self.grid.name)
    
    def saveChanges(self, path='result\\'):
        plt.plot(self.changes)
        plt.ylabel('number of changes')
        plt.xlabel('Generations')       
        plt.savefig(path+'changes_'+self.grid.name)
                