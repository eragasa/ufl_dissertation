import os,shutil
from collections import OrderedDict
import pypospack.utils
from pypospack.pyposmat.data import PyposmatConfigurationFile
from pypospack.pyposmat.data import PyposmatDataFile
from pypospack.pyposmat.visualization import Pyposmat2DDensityPlot

data_directory = os.path.join(
        pypospack.utils.get_pypospack_root_directory(),
        'data','Si__sw__data',
        'pareto_optimization_unconstrained'
        )

plot_directory = 'qoi_2d_density_plots'
if os.path.isdir(plot_directory):
    shutil.rmtree(plot_directory)
os.mkdir(plot_directory)

o_config = PyposmatConfigurationFile()
o_config.read(filename=os.path.join(data_directory,'pyposmat.config.in'))

max_iteration = o_config.n_iterations
o_data = PyposmatDataFile()
o_data.read(filename=os.path.join(data_directory,'pyposmat.kde.{}.out'.format(max_iteration)))

plots_to_make = OrderedDict()
plots_to_make['Si_dia_E_coh__Si_dia_a0']= OrderedDict([
        ('names',['Si_dia.E_coh','Si_dia.a0']),
        ('fig_suffix','png'),
        ('fig_dpi',1300)
    ])
for plot_fn, plot_info in plots_to_make.items():
    fig_suffix = plot_info['fig_suffix']
    fig_dpi = plot_info['fig_dpi']
    name_1 = plot_info['names'][0]
    name_2 = plot_info['names'][1]
    plot_fn = os.path.join(
            plot_directory,
            '{}.{}'.format(plot_fn,fig_suffix))
    o = Pyposmat2DDensityPlot(config=o_config,data=o_data)
    o.plot(x_name=name_1,y_name=name_2)
    o.ax.axvline(o.configuration.qoi_targets[name_1],
        color='black',linewidth=1)
    o.ax.axhline(o.configuration.qoi_targets[name_2],
        color='black',linewidth=1)
    o.ax.set_xlabel(r'{} [{}]'.format(
        o.configuration.latex_labels[name_1]['label'],
        o.configuration.latex_labels[name_1]['units']))
    o.ax.set_ylabel(r'{} [{}]'.format(
        o.configuration.latex_labels[name_2]['label'],
        o.configuration.latex_labels[name_2]['units']))
    o.fig.savefig(plot_fn,dpi=fig_dpi)
