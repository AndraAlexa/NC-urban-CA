# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:36:03 2015

@author: andruta
"""

"""This code performs the color quantization using K-means
   It was a first approach we used, but it was not implemented in the final project
   because a better solution was found
"""

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import shuffle
from time import time
from scipy.misc import toimage
import os
import utility as ut
import webcolors
from  webcolors import rgb_to_name
from numpy import zeros
#I usually set my own working directory where I keep my files
os.chdir("/home/andruta/anaconda/NC")
os.getcwd()

#define the number of colors to reduce to

def color_quantization(filename='mass1971.jpg', n_colors = 8):

    # Load the  photo
    img=Image.open(filename)
    
    #convert the values to floats instead of the defalt 8 bits integer
    #Dividing by 255 is very important so that plt.inshow works well on float data
    #data needs to be in range [0 1]
    
    img=np.array(img, dtype=np.float64)/255
    
    #Load the image and transform into a 2Dnumpy array
    w,h,d = original_shape = tuple (img.shape)
    assert d==3
    image_array=np.reshape(img, (w*h,d))
    """
    ((   
   (0, 0, 0),     # black background
    (255, 0, 0),   # index 1 is red
    (255, 255, 0), # index 2 is yellow
    (255, 0, 255), # index 3 is orange
    (102, 160, 38),   # index 4 is green
   ( 0, 148, 189),   # index 5 is blue
   ( 207, 3, 124), # index 6 is pink
   ( 69, 0, 68), # index 7 is lila
   ( 117,117,117)
   )) # index 8 is grey
    """
    """
            Now it builds the predictive model
    """
    
    print("Fitting model on a small sub-sample of the data")
    t0 = time()
    #gets 1000 random states
    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    
  
    #not it fits the model
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
    #just to check the time
    print("Done in %0.3fs." % (time() - t0))
    
    """
            Now it generalizes to all the pixels of the picture
    """
    
    # Get labels for all points
    print("Predicting color indices on the full image (k-means)")
    t0 = time()
    labels = kmeans.predict(image_array)
    print("Done in %0.3fs." % (time() - t0))
    
    
    """
            Now it predicts the color
    """
    
    codebook_random = shuffle(image_array, random_state=0)[:n_colors + 1]
    print("Predicting color indices on the full image (random)")
    t0 = time()
    labels_random = pairwise_distances_argmin(codebook_random,
                                              image_array,
                                              axis=0)
    print("Done in %0.3fs." % (time() - t0))
    
    
    def recreate_image(codebook, labels, w, h):
        """Recreate the (compressed) image from the code book & labels"""
        d = codebook.shape[1]
        image = np.zeros((w, h, d))
        label_idx = 0
        for i in range(w):
            for j in range(h):
                image[i][j] = codebook[labels[label_idx]]
                label_idx += 1
        return image
        
        
    # Displays the initial image
    plt.figure(1)
    plt.clf()
    ax = plt.axes([0, 0, 1, 1])
    plt.axis('off')
    plt.title('Original image (thousands colors)')  
    plt.imshow(img)
    
    #This plots the image with 8 colors
    plt.figure(2)
    plt.clf()
    ax = plt.axes([0, 0, 1, 1])
    plt.axis('off')
    plt.title('Quantized image (8 colors, K-Means)')
    plt.imshow(recreate_image(kmeans.cluster_centers_, labels, w, h))
    plt.show()
    
    
    #this is the modified image in np.ndarray format
    image = recreate_image(kmeans.cluster_centers_, labels, w, h)
    #now this image is in np.ndarray format, we have to extract the colors.
    plt.imshow(image)
    
    im=toimage(recreate_image(kmeans.cluster_centers_, labels, w, h))
    
    #now transform the image in 8 bits integer (image) and extract colors
    return toimage(recreate_image(kmeans.cluster_centers_, labels, w, h)).getcolors(), im
    
def make_color_list (colors):
    color_list = list()
    for i in range (0,len(colors)):
        color_list.append(str(closest_colour(colors[i][1])))
    """
    for i in range (0,len(color_list)):
        if color_list[i] in {'green'}:
            color_list[i]='green'
        if color_list[i] in {'blue', 'darkcyan'}:
            color_list[i]='blue'
        if color_list[i] in {'red'}:
            color_list[i]='red'
        if color_list[i] in {'yellow', 'olive'}:
            color_list[i]='yellow'
        if color_list[i] in {'orange'}:
            color_list[i]='orange'
        if color_list[i] in {'white'}:
            color_list[i]='white'
        if color_list[i] in {'black','palevioletred'}:
            color_list[i]='black'
        if color_list[i] in {'grey', 'palegoldenrod'}:
            color_list[i]='grey'
    """
    return color_list
                     
  
def grid_generator(im):
    #define the variables
    white_space=0
    resd = 0   # number of residentials -->10 (red)
    comerc = 0  # number of comercials --> 11  (yelow)
    industry = 0 # industrial area      --> 12 (black)
    roads = 0   # number of roads       --> 20 (grey)
    highway = 0  # number of highway    --> 21 (grey)
    sea = 0    # number of sea        --> 30 (blue)
    forest = 0  # number of forest      --> 31 (green)

    pix=im.load()
    w=im.size[0]
    h=im.size[1]
    
    grid=np.zeros(shape=(w,h))
    
    
    
    for y in range (0, h):
        for x in range (0,w):
            offset=y*w+x
            xy= (x, y)
            rgb=im.getpixel(xy)
            
            if  rgb == colors[0][1]: #this is yellow, let's make it roads
               roads=roads+1
               grid[y,x]=20
                
            elif rgb == colors[1][1]: #this is red
                resd=resd+1
                grid[y,x]=10
                
            elif rgb == colors[2][1]: #this is green
                forest=forest+1
                grid [y,x]=31
                
            elif rgb == colors [3][1]: #this is blue
                sea=sea+1
                grid[y,x]=30
                
            elif rgb == colors [4][1]: #this is some sort of green 
                highway=highway+1
                grid [y,x]=21
                
            elif rgb == colors [5][1]:#this is orange -
                comerc=comerc+1
                grid[y,x]=11
                
            elif rgb == colors [6][1]:#this is (almost) white
                white_space=white_space+1
                grid[y,x]=0
                
            elif rgb == colors [7][1]:#this is pink
                industry=industry+1
                grid[y,x]=12
                
            else:
                grid[y,x]=0
                
    return grid
    

def RGBColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor
    
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]
    
    
def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

requested_colour = (119, 172, 152)
actual_name, closest_name = get_colour_name(requested_colour)
    
print "Actual colour name:", actual_name, ", closest colour name:", closest_name

    
    
    
if __name__ == '__main__':
    
    
    filename='mass1971.jpg'
    #colors is a list, first column is the no of appearances and 2nd column is the colors (tuple)
    white_space= 'white'
    resd = 'red'   # number of residentials -->10 (red)
    comerc = 'yellow' # number of comercials --> 11  (yelow)
    industry = 'black' # industrial area      --> 12 (black)
    roads = 'grey'   # number of roads       --> 20 (grey)
    highway = 'grey'  # number of highway    --> 21 (grey)
    sea = 'blue'   # number of sea        --> 30 (blue)
    forest='green'
    
    colors, im = color_quantization(filename='mass1971.jpg', n_colors = 8)
    color_list = make_color_list(colors)
    
    grid=grid_generator(im)
    
    ut.visualizeGrid(grid)

    #make a list with all the colors
    color_list=make_color_list(colors)
        