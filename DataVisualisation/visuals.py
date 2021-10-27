from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas
import pandas as pd
import csv
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


points = pandas.read_csv('SobjObj_realcoords.csv')
pp = PdfPages('histograms.pdf')

#create 2 figures
fig = plt.figure()
fig2 = plt.figure()
fig3 = plt.figure()

#create 2 subplots
ax = fig.add_subplot(111, projection='3d')
ax2 = fig2.add_subplot(111, projection='3d')
ax3 = fig3.add_subplot(111, projection='3d')


x = points['Xs'].values
y = points['Ys'].values
z = points['Zs'].values

x2 = points['Xo'].values
y2 = points['Yo'].values
z2 = points['Zo'].values

#Point labels
n = points['s_id'].values
n2 = points['o_id'].values
#realationship id ex. boook - shelf
n3 = n + ' -' + n2


#Define the 1rst plot
ax.scatter(x, y, z, label='Subjects', s=10, c='g', marker='o')
ax.scatter(x2, y2, z2, label='Objects', s=10, c='r', marker='o')
ax.legend()

#Labeling of each point
#for i, txt in enumerate(n):
#    ax.text(x[i], y[i], z[i], txt, color='black')

#for i, txt in enumerate(n2):
#    ax.text(x2[i], y2[i], z2[i], txt, color='black')

#Axis labels
ax.set_xlabel('x axis')
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')

#2nd plot
colors = np.random.rand(len(points),3)

ax2.scatter(x, y, z, s=10, c=colors, marker='o')
ax2.scatter(x2, y2, z2, s=20, c=colors, marker='o')

#for i, txt in enumerate(n3):
#    ax2.text(x[i], y[i], z[i], txt, color='black')

ax2.set_xlabel('x axis')
ax2.set_ylabel('y axis')
ax2.set_zlabel('z axis')

#3rd plot
ax3.plot(x, y, z, label='subjects', marker='o')
ax3.plot(x2, y2, z2, label='objects', marker='o')
ax3.legend()

ax3.set_xlabel('x axis')
ax3.set_ylabel('y axis')
ax3.set_zlabel('z axis')

#plot the 3 figures
fig.savefig('fig.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True, bbox_inches='tight', pad_inches=0.1,
        frameon=1, metadata=None)

fig2.savefig('fig1.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True, bbox_inches='tight', pad_inches=0.1,
        frameon=1, metadata=None)

fig3.savefig('fig2.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=True, bbox_inches='tight', pad_inches=0.1,
        frameon=1, metadata=None)

plt.show()


