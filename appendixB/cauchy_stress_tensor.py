from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

#https://stackoverflow.com/questions/22867620/putting-arrowheads-on-vectors-in-matplotlibs-3d-plot
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
class Arrow3D(FancyArrowPatch):
    def __init__(self, posA, posB, *args,**kwargs):
        FancyArrowPatch.__init__(self,posA,posB,*args,**kwargs)

    def draw(self,renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d,yd3d,zs3d,renderer.M)
        FancyArrowPatch.draw(self,renderer)

# https://stackoverflow.com/questions/44881885/python-draw-parallelepiped
def plot_cube(cube_definition):
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]

    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    faces = Poly3DCollection(edges, linewidths=1, edgecolors='k')
    faces.set_facecolor((0,0,1,0.1))
    ax.add_collection3d(faces)
    # Plot the points themselves to force the scaling of the axes
    ax.scatter(points[:,0], points[:,1], points[:,2], s=0)

    arrows = OrderedDict()
    arrows['sigma_11'] = OrderedDict()
    arrows['sigma_11']['x0'] = (1.0,0.5,0.5)
    arrows['sigma_11']['xdir'] = (1,0,0)
    arrows['sigma_11']['length'] = 0.4
    arrows['sigma_11']['text_location'] = ()

    def annonated_quiver(ax,x,y,z,u,v,w,l,s):
        x_0 = np.array([x,y,z])
        x_f = x_0 + l * np.array([u,v,w])

        if (u,v,w) == (1,0,0) or (u,v,w) == (0,1,0):
            x_t = (x_0 + x_f)/2 + np.array([0,0,.05])
        elif (u,v,w) == (0,0,1):
            x_t = (x_0 + x_f)/2 + np.array([0,0.05,0])
        else:
            raise NotImplementedError

        ax.quiver(x,y,z,y,v,w,l)
        ax.text(x_t[0],x_t[1].x_t[2],s)
    ax.quiver(1.0, 0.5, 0.5, 1,0,0, length=0.4, normalize=False)
    ax.text(1.2,0.5,0.55,r'$\sigma_{11}$')
    ax.quiver(1.0, 0.5, 0.5, 0,1,0, length=0.4, normalize=False)
    ax.text(1.0,0.65,0.55,r'$\sigma_{12}$')
    ax.quiver(1.0, 0.5, 0.5, 0,0,1, length=0.4, normalize=False)
    ax.text(1.0,0.55,0.68,r'$\sigma_{13}$')

    ax.quiver(0.5, 1.0, 0.5, 0,1,0, length=0.4, normalize=False)
    ax.quiver(0.5, 1.0, 0.5, 1,0,0, length=0.4, normalize=False)
    ax.quiver(0.5, 1.0, 0.5, 0,0,1, length=0.4, normalize=False)

    ax.quiver(0.5, 0.5, 1.0, 0,0,1, length=0.4, normalize=False)
    ax.quiver(0.5, 0.5, 1.0, 1,0,0, length=0.4, normalize=False)
    ax.quiver(0.5, 0.5, 1.0, 0,1,0, length=0.4, normalize=False)


    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.view_init(azim=54, elev=27)
    fig.savefig('stress_tensor.eps',dpi=1200)
    plt.show()


cube_definition = [
    (0,0,0), (0,1,0), (1,0,0), (0,0,1)
]
plot_cube(cube_definition)
