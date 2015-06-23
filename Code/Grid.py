# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:05:28 2015

@author: Natalie
"""
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import random as rnd
import Image2Grid

class Grid():

    # Initialize the CA
    def __init__(self, grid_size=250, savePlots=False, name='test', add=''):

        self.grid_size = grid_size
        self.grid = np.zeros(shape=(grid_size,grid_size))        
        self.savePlots = savePlots
        self.add = add
        self.name = add+name
        self.ext_color = False
        self.lu_values = {'residential': 10, 'comercial': 11, 'industrial': 12,
                          'road'       : 20, 'highway'  : 21, 
                          'sea'        : 30, 'forest'   : 31,
                          'open'       : 0}

    
    # give array of neighbours back
    def getNeighbours(self, pos, neighbourhood='Moore'):
        # central cell at position i,j
        c = self.grid.item(pos)
        i, j = pos[0], pos[1]        
        
        # define basic cardinal directions
        n = self.grid.item(i-1,j)
        w = self.grid.item(i,j-1)
        e = self.grid.item(i,j+1)
        s = self.grid.item(i+1,j)
        
        # add intermediate directions
        nw = self.grid.item(i-1,j-1)
        ne = self.grid.item(i-1,j+1)
        sw = self.grid.item(i+1,j-1)
        se = self.grid.item(i+1,j+1)  
        
        if neighbourhood=='Neuman':     
            neighbours = np.array([n,w,e,s])
    
        elif neighbourhood=='Moore':    
            neighbours = np.array([nw,n,ne,w,e,sw,s,se])
        
        else:
            neighbours = np.array([c])

        return neighbours
    
    # convert an jpg image to grid    
    def image2Grid(self, fname, path='Images\\', mode='yuv', output=True, ext_colors=False):
        
        pxl = Image2Grid.convertImage(fname, path, mode, output, ext_colors)
        n = pxl.shape[0]
        g = np.zeros(shape=(n+2,n+2))
        g[1:n+1,1:n+1] = pxl
        
        self.grid = g
        self.grid_size = n
        self.name = self.add+fname
        self.ext_color = ext_colors
        
        if ext_colors:
            self.lu_values = {'residential': 10, 'comercial' : 11, 'industrial': 12,
                  'road'       : 20, 'highway'   : 21, 
                  'sea'        : 30, 'forest'    : 31, 
                  'open_land'  : 40, 'urban_open': 41,
                  'mining'     : 50, 'recreation': 51,
                  'open'       : 0}
            self.name = "ext_" + self.name
    

    # generate a random grid
    def rnd_gridGenerator(self, grid_size=250):
        
        self.grid_size=grid_size
        f = self.grid_size*self.grid_size/100
        # generate a grid with dead elements
        # make a frame of zeros to avoid out of bounds at neighborhood
        self.grid = np.zeros(shape=(self.grid_size+2,self.grid_size+2))    
        
        # place residential, comercial, industry and sea random positions
        #self.grid = 
        self.place_cells(f*10, 'residential')
        self.place_cells(f*7, 'comercial')
        self.place_cells(f*3, 'industrial')
        self.place_cells(f*5, 'sea')
        self.place_cells(f*5, 'forest')
            
        self.place_street(self.grid_size*10/100, 'highway')


    # create city with differnent properties
    def basic_city(self, sea=False, roads=False, industry=False, forest=False, comerc=False):
        
        m = self.grid_size
        xc,yc = m/2+1,m/2+1; 
        
        
        #smaller part in grid
        n = m/50*10;
        self.grid_size = n
        self.grid = np.zeros(shape=(n,n)); # 5 %
        # number of house
        self.place_cells(m*50/100,'residential',shift=True);
        
        if comerc:
            self.place_cells(m*15/100,'comercial',shift=True);
    
        if industry:
            self.place_cells(m*15/100,'industrial',shift=True);            
            
        if roads:
            self.place_street(m/50*3,'road',shift=True)
                    
        if forest:
            self.place_cells(m*10/100,'forest', shift=True)
            
        if sea:
            self.place_cells(m/50*5,'sea', shift=True)
            
        # place residual space  
        resd_grid = self.grid.copy()
        self.grid = self.grid = np.zeros(shape=(m+2,m+2))
        self.grid[xc-n/2:xc+n/2,yc-n/2:yc+n/2] = resd_grid;
        
    # Plot Grid
    def visualize(self):
      
        fig, ax = plt.subplots()
        
        if self.ext_color:
            cmap = mpl.colors.ListedColormap(['grey','red','orange','yellow','black','white', 'blue',
                                              'green', 'olive','darkcyan','brown','pink'])
            bounds=[0,10,11,12,20,21,30,31,40,41,50,51,52] 
            
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
            cax = ax.imshow(self.grid, interpolation='nearest', cmap=cmap, norm=norm)

            
            cbar = fig.colorbar(cax, ticks=bounds)
            cbar.ax.set_yticklabels([ 'open','residential','commercial','industry','road','highway',
                                     'sea','forest', 'rural open', 'urban open', 'mining','recreation']) 
        else:
                 
            # ake a color map of fixed colors
            cmap = mpl.colors.ListedColormap(['grey','red','orange','yellow','black','white', 'blue', 'green'])
            bounds=[0,10,11,12,20,21,30,31,32] 
    
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
            cax = ax.imshow(self.grid, interpolation='nearest', cmap=cmap, norm=norm)        
            
            cbar = fig.colorbar(cax, ticks=bounds)
            cbar.ax.set_yticklabels(['open','residential','commercial','industry',
                                     'road','highway','sea','forest'])# vertically oriented colorbar

        plt.show()
        
    
    #save grid as Image
    def saveImage(self, path='',name=''):
        
        fig, ax = plt.subplots()
        # make a color map of fixed colors
        if self.ext_color:
            cmap = mpl.colors.ListedColormap(['grey','red','orange','yellow','black','white', 'blue',
                                              'green', 'olive','darkcyan','brown','pink'])
            bounds=[0,10,11,12,20,21,30,31,40,41,50,51,52] 
            
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
            cax = ax.imshow(self.grid, interpolation='nearest', cmap=cmap, norm=norm)

            
            cbar = fig.colorbar(cax, ticks=bounds)
            cbar.ax.set_yticklabels([ 'open','residential','commercial','industry','road','highway',
                                     'sea','forest', 'rural open', 'urban open', 'mining','recreation']) 
        else:
                 
            # ake a color map of fixed colors
            cmap = mpl.colors.ListedColormap(['grey','red','orange','yellow','black','white', 'blue', 'green'])
            bounds=[0,10,11,12,20,21,30,31,32] 
    
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
            cax = ax.imshow(self.grid, interpolation='nearest', cmap=cmap, norm=norm)        
            
            cbar = fig.colorbar(cax, ticks=bounds)
            cbar.ax.set_yticklabels(['open','residential','commercial','industry',
                                     'road','highway','sea','forest'])# vertically oriented colorbar
        
        if name=='':                            
            plt.savefig(path+self.name)
        else:
            plt.savefig(path+name)

            
    # place a number of cells at random postiion in grid    
    def place_cells(self, num, key, shift=False):
        
        if shift:
            pos = [(rnd.randint(0,self.grid_size-1), rnd.randint(0,self.grid_size-1)) for k in range(num)];
        else:
            pos = [(rnd.randint(1,self.grid_size), rnd.randint(1,self.grid_size)) for k in range(num)];
        for pos_i in pos:
            self.grid[pos_i] = self.lu_values[key];
            
            
    # place roads and highways at random positions in random direction
    def place_street(self, num, key, shift=False):
        
        for road in range(num):          
            road_dir = rnd.randint(0,1)
            if shift:
                pos = rnd.randint(0,self.grid_size-1)
                
                if road_dir==0:
                    self.grid[pos,0:self.grid_size] = self.lu_values[key]
                else:
                    self.grid[0:self.grid_size,pos]= self.lu_values[key]
            else:
                pos = rnd.randint(1,self.grid_size)
                
                if road_dir==0:
                    self.grid[pos,1:self.grid_size+1] = self.lu_values[key]
                else:
                    self.grid[1:self.grid_size+1,pos]= self.lu_values[key]
    