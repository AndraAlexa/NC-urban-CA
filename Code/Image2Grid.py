from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

#    free        --> 0 
#    residential -->10
#    comercials --> 11
#    industry   --> 12
#    roads      --> 20
#    highway    --> 21
#    sea        --> 30
#    forest     --> 31
#    open land  --> 40
#    urban open --> 41
#    mining     --> 50
#    recreation --> 51

# global color definitions and the corresponding value in the grid
# colors:       red -commercial lila-industrial  blue - water  orange - resi  green -forest high densi resid black dotss
colors = np.array([ [255, 0, 0], [115, 0, 132], [0, 255, 255], [255, 173, 0], [0, 132, 0],  [148,148,0],   [0,0,0], [255, 255, 57],
                   # yellow - reside yellow - res   grey - transport grey- open    green-open   lila water-based recreation
                  [204, 204, 0], [255, 255, 173], [156,156,156], [92, 177, 153], [181, 255, 0], [255,0,255], [239, 90, 181],[149, 187, 230]])
colorIDs = np.array([11,12,30,10,31,10,10,10,
                     10,10,21,0,0,30,30,30])

# extended version of land usage
colors_ext = np.array([ [255, 0, 0], [115, 0, 132], [0, 255, 255], [255, 173, 0], [0, 132, 0],  [148,148,0],   [0,0,0], [255, 255, 57],
                   # yellow - reside yellow - res   grey - transport grey- open    green-open   lila water-based recreation
                  [204, 204, 0], [255, 255, 173], [156,156,156], [92, 177, 153], [181, 255, 0], [255,0,255], [239, 90, 181],[255, 99, 206], 
                                 # light brown - mining
                 [149, 187,230], [165, 99, 49],[8,123,132]])
                 
colorIDs_ext = np.array([11,12,30,10,31,10,10,10,
                     10,10,21,0,41,51,51,51,30,
                     50,40])

def rgb_to_yuv(I):
    #takes rgb pixel matrix 3 x #pixel and transforms to YUV
    #http://bit.ly/1blFUsF
    M = np.array([ [.299, .587, .114], [-.168736, -.331364, .5], [.5, -.418688, -.081312] ])
    m = np.array([ [0], [128], [128] ])
    return M.dot(I)+m


def rgb_to_cie(I):
    #http://en.wikipedia.org/wiki/CIE_1931_color_space#Construction_of_the_CIE_XYZ_color_space_from_the_Wright.E2.80.93Guild_data
    M = np.array([ [.49, .31, .20], [.17697, .81240, .01063], [.00, .01, .99] ])
    return M.dot(I)


def convertImage(fname, path='Images\\', mode='yuv', output=True, ext_colors = False):
    
    global colors, colorIDs, colors_ext, colorIDs_ext
    
    # switch to extended landuse mapping
    if ext_colors:
        colors = colors_ext
        colorIDs = colorIDs_ext
        
    #transform image and target colors to yuv
    img = Image.open(path+fname)
    x,y = img.size
    I = np.array(img.getdata()).T
    
    if mode is 'yuv':
        I = rgb_to_yuv(I)
        colors_m = rgb_to_yuv(colors.T).T
    elif mode is 'cie':
        I = rgb_to_cie(I)
        colors_m = rgb_to_cie(colors.T).T
    else:
        print('mode unknown, using rgb as fallback')
        colors_m = colors
    #colors is 8 x 3
    #I is 3 x #pixel

    #we use the following identity to compute the distances matrix
    #||x-y||^2 = (x-y)'(x-y) = x'x - 2x'y + y'y
    xx = np.diag( colors_m.dot(colors_m.T) ).reshape(len(colors),1)
    xy = colors_m.dot(I)
    #due to memory issues we cannot get this as a diagonal of a hufge #pixels x #pixels matrix
    #we could iterate as follows, which needs a long time as well
    #yy = np.array([[ a.dot(a) for a in I.T ]])
    #BUT luckily we only want to select the x for which the distance is minimal,
    #hence we can ignore the y'y as it is constant wrt x
    #so we arrive at the following 8 x #pixel matrix
    pseudodists = xx-2*xy

    #this gives the ID of the closest colour for each pixel and the rgb matrix of the closest colours
    ids = pseudodists.argmin(axis=0)
    closestIDs = colorIDs[ ids ]
    closestcolors_rgb = colors[ ids ]
    conv_pxl = closestIDs.reshape(img.size)
    
    
    if output:
        
        conv_img = np.zeros([x,y,3], dtype=np.uint8)
        closestcolors_rgb = closestcolors_rgb.T
        conv_img[:,:,0] = closestcolors_rgb[0,:].reshape(x,y)
        conv_img[:,:,1] = closestcolors_rgb[1,:].reshape(x,y)
        conv_img[:,:,2] = closestcolors_rgb[2,:].reshape(x,y)
        conv_img = Image.fromarray(conv_img, 'RGB')
        
        # console output 
        plt.imshow(img)
        plt.show()
        plt.imshow(conv_img)
        plt.show()
        cols = conv_img.getcolors()
        print 'colors:', cols
        
        # save converted file
        conv_fname = mode + '_' + fname;
        conv_img.save(conv_fname)

    return conv_pxl

# RUN 
#grid = convertImage('mass1971.jpg', mode='yuv', output=True)

