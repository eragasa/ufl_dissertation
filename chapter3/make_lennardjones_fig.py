import pytest
import numpy as np
from collections import OrderedDict
from pypospack.potential import LennardJonesPotential

testcase = OrderedDict()
testcase['symbols'] = ['Ar']
testcase['parameters'] = OrderedDict()
testcase['parameters']['ArAr_sigma'] = 1.0
testcase['parameters']['ArAr_epsilon'] = 1.0
testcase['parameter_names'] = ['r_cut_global', 'ArAr_epsilon', 'ArAr_sigma', 'ArAr_r_cut_pair', 'ArAr_r_cut_coulomb']

print('calculating LJ potential')
r = np.linspace(1,1000,1000)/1000*3
r_m = 2**(1/6)*testcase['parameters']['ArAr_sigma']
o = LennardJonesPotential(symbols=testcase['symbols'])
print('symbols:',o.symbols)
o.evaluate(r=r,parameters=testcase['parameters'])

print('creating plot...')
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text',usetex=True)
plot_width = 5
aspect_ratio = 1.
symbol_pair = 'ArAr'
x_lim_min = 0.5
x_lim_max = 2
y_lim_min = -2
y_lim_max = 2
x_label_latex = r'interatomic distance $[r/\sigma]$'
y_label_latex = r'potential strength $[\hat{V}/\epsilon]$'
fig,ax = plt.subplots(1,1,figsize=(5,5))
ax.axhline(0,color='black')
ax.plot(r,o.potential_evaluations['ArAr'])
ax.hlines(-1,
           xmin=x_lim_min,
           xmax=r_m,
           color='black',
           linestyle='--'
           )
ax.vlines(testcase['parameters']['ArAr_sigma'],
          ymin=y_lim_min,
          ymax=0,
          color='black',
          linestyle='--'
          )
ax.annotate('',
            xy=(0.75,0),xycoords='data',
            xytext=(0.75,-1),textcoords='data',
            arrowprops=dict(arrowstyle='<->',connectionstyle='arc3')
            )
ax.set_xlim(x_lim_min,x_lim_max)
ax.set_ylim(y_lim_min,y_lim_max)
ax.set_xlabel(x_label_latex)
ax.set_ylabel(y_label_latex)
#plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace =0, wspace=0)
plt.margins(0,0)
#plt.gca().xaxis.set_major_locator(plt.NullLocator())
#plt.gca().yaxis.set_major_locator(plt.NullLocator())
fig.tight_layout()
plt.show()

fig.savefig('lj.png',dpi=1200)
#,bbox_inches='tight',pad_inches=0)
