import math
import matplotlib.path
import numpy as np

x_pixel_nos = [...]
y_pixel_nos = [...] # Data from https://gist.github.com/sdoken/173fae1f9d8673ffff5b481b3872a69d

temp_list = []
for a, b in zip(x_pixel_nos, y_pixel_nos):
   temp_list.append([a, b])

polygon = np.array(temp_list)
left = np.min(polygon, axis=0)
right = np.max(polygon, axis=0)
x = np.arange(math.ceil(left[0]), math.floor(right[0])+1)
y = np.arange(math.ceil(left[1]), math.floor(right[1])+1)
xv, yv = np.meshgrid(x, y, indexing='xy')
points = np.hstack((xv.reshape((-1,1)), yv.reshape((-1,1))))

path = matplotlib.path.Path(polygon)
mask = path.contains_points(points)
mask.shape = xv.shape
