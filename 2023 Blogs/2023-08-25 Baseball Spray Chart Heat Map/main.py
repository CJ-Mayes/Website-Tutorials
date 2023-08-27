import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
from matplotlib.colors import rgb2hex
import sys
np.set_printoptions(threshold=sys.maxsize)

# Read data from file
data = pd.read_csv('data.csv')

# Create variables for X, Y coordinates
x = data['hc_x']
y = data['hc_y']

x = (x-125.42)/10
y = (198.27-y)/10

# Create a bivariate kernel density plot
cs = sns.kdeplot(x=x, y=y, legend=True, n_levels=10, thresh=.3, cmap='plasma')

#Set the limits to what is used in background mapping of tutorial
plt.xlim(-12.5, 12.5)
plt.ylim(-5, 19)
plt.axis('on')

plt.show()

# Create a list of all vertices, their colour and contours
lines = []

vertice_id=0
path_id=0
for collection in cs.collections:
    color = collection.get_edgecolor()
    for path in collection.get_paths():
        for vertice in path.to_polygons():
            path_id = path_id + 1
            for i in vertice:
                vertice_id = vertice_id + 1
                aa = rgb2hex(color[0]), path_id, vertice_id, i[0],i[1]
                lines.append(aa)
                print (rgb2hex(color[0]), path_id, vertice_id, i[0],i[1])

# Save values to file
np.savetxt("data_contour.csv", lines, header='color,contour_id,vertice_id,x,y', fmt='%s',  delimiter=",")

