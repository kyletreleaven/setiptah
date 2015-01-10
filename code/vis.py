
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_axes3d() :
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    return ax
