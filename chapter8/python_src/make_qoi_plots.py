import os,shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import gaussian_kde

import pypospack.utils
from pypospack.pyposmat.data import PyposmatConfigurationFile
from pypospack.pyposmat.data import PyposmatDataFile
from pypospack.pyposmat.visualization import PyposmatQoiPlot


def make_qoi_plots(data_directory,
                   plot_directory,
                   config=None,
                   data_type='kde',
                   iterations='all'):

    data_types = ['kde','results']

    assert isinstance(config,str) \
            or isinstance(config,PyposmatConfigurationFile) \
            or config is None
    assert os.path.isdir(data_directory)
    assert isinstance(plot_directory,str)
    assert data_type in data_types

    if not os.path.exists(plot_directory):
        os.mkdir(plot_directory)

    # process config argument
    if isinstance(config,str):
        o_config = PyposmatConfigurationFile()
        o_config.read(filename=config)
    elif isinstance(config,PyposmatConfigurationFile):
        o_config = PyposmatConfigurationFile()
    elif config is None:
        o_config = PyposmatConfigurationFile()
        o_config.read(filename=os.path.join(data_directory,'pyposmat.config.in'))
    else:
        m = 'config arguement must either be a path string of a PyposmatConfigurationFile object'
        raise TypeError(m)

    if iterations == 'all':
        iterations = range(o_config.n_iterations)

    if data_type == 'kde':
        datas = [
            os.path.join(data_directory,'pyposmat.kde.{}.out'.format(i+1)) for i in iterations
        ]
    elif data_type == 'results':
        datas = [
            os.path.join(data_directory,'pyposmat.results.{}.out'.format(i)) for i in iterations
        ]
    else:
        raise TypeError()

    plot_fns = []
    for qn in o_config.qoi_names:
        print('qoi_name:{}'.format(qn))
        plot_fn=os.path.join(plot_directory,'{}.eps'.format(qn.replace('.','_')))
        plot_fns.append(plot_fn)
        xlabel=qn
        ylabel='probablity density'
        o_plot = PyposmatQoiPlot(config=o_config)

        print('\tdetermining x_lims')
        x_min = None
        x_max = None
        for data_fn in datas:
            x_pctl_min = 0.15
            x_pctl_max = 1. - x_pctl_min
            o_data = PyposmatDataFile()
            o_data.read(filename=data_fn)

            from scipy.stats import norm
            mu,std = norm.fit(o_data.df[qn])
            norm_rv = norm(loc=mu,scale=std)
            
            if x_min == None:
                x_min = norm_rv.ppf(x_pctl_min)
            else:
                x_min = min(norm_rv.ppf(x_pctl_min),x_min)

            if x_max == None:
                x_max = norm_rv.ppf(x_pctl_max)
            else:
                x_max = max(norm_rv.ppf(x_pctl_max),x_max)

        for i,data_fn in enumerate(datas):
            print('\t{}'.format(data_fn))
            o_data = PyposmatDataFile()
            o_data.read(filename=data_fn)

            label='i={}'.format(iterations[i]+1)
            o_plot.initialize_data(data=o_data)
            o_plot.add_qoi_plot(
                    qoi_name=qn,
                    x_limits=[x_min,x_max],
                    label=label,
                    color=plt.cm.cool(i/len(datas))
                    )


        o_plot.add_qoitarget(qoi_name=qn)
        o_plot.ax.set_xlim(x_min,x_max)
        o_plot.legend()
        o_plot.ax.set_xlabel(xlabel)
        o_plot.ax.set_ylabel(ylabel)
        o_plot.ax.ticklabel_format(axis='both',style='sci',scilimits=(0,4))
        o_plot.savefig(filename=plot_fn,dpi=1300)

    return plot_fns
if __name__ == "__main__":
    plot_dir = os.path.join('..','qoi_plots')
    pypospack_root_dir = pypospack.utils.get_pypospack_root_directory()
    data_dir = os.path.join(pypospack_root_dir,'data','Si__sw__data','pareto_optimization_p_3.5_q_0.5')

    make_qoi_plots(
            data_directory=data_dir,
            plot_directory=plot_dir,
            iterations=[0,1,4,9,19]
            )


