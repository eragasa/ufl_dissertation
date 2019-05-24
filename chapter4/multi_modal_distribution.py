import os,shutil
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

plot_dpi = 1200
plot_fn = "kde_cdf_pdf.eps"

n_samples = 1000
n_bins = 30

mu_1 = -5.0
sigma_1 = 2

mu_2 = 0.0
sigma_2 = 1.0

mu_3 = 5.0
sigma_3 = 2

norm_rv_1 = norm(loc=mu_1,scale=sigma_1)
norm_rv_2 = norm(loc=mu_2,scale=sigma_2)
norm_rv_3 = norm(loc=mu_3,scale=sigma_3)

# determin x_limits
x_min = min(norm_rv_1.ppf(0.0001),
            norm_rv_2.ppf(0.0001),
            norm_rv_3.ppf(0.0001))
x_max = max(norm_rv_1.ppf(0.9999),
            norm_rv_2.ppf(0.9999),
            norm_rv_3.ppf(0.9999))

x_min = -10
x_max = 10

x = np.linspace(x_min,x_max,500)

import scipy.integrate as integrate

pdf_1 = norm_rv_1.pdf(x)
pdf_2 = norm_rv_2.pdf(x)
pdf_3 = norm_rv_3.pdf(x)

c_pdf_1 = 1
c_pdf_2 = 2
c_pdf_3 = 1

pdf = c_pdf_1*pdf_1 \
      + c_pdf_2*pdf_2 \
      + c_pdf_3*pdf_3
pdf_normalization_factor = integrate.quad(
        lambda x: c_pdf_1*norm_rv_1.pdf(x) \
                  + c_pdf_2*norm_rv_2.pdf(x) \
                  + c_pdf_3*norm_rv_3.pdf(x),
        x_min,
        x_max)
pdf = pdf/pdf_normalization_factor[0]

#calculating the CDF by using the trapazoidal rule
print('calculating the CDF')
print('len(x)={}'.format(len(x)))
cdf = [np.trapz(pdf[:i],x[:i]) for i in range(len(x))]
cdf = np.array(cdf)

base_n_samples = int(n_samples/(c_pdf_1+c_pdf_2+c_pdf_3))
sample_rv = np.concatenate(
        (
            norm_rv_1.rvs(size=c_pdf_1*base_n_samples),
            norm_rv_2.rvs(size=c_pdf_2*base_n_samples),
            norm_rv_3.rvs(size=c_pdf_3*base_n_samples)
        )
)

fig, ax = plt.subplots(1,2)
ax[0].hist(sample_rv,
        bins=n_bins,
        density=True,
        histtype='stepfilled',
        alpha=0.2)
ax[0].plot(x,pdf)
ax[0].set_xlabel('x')
ax[0].set_ylabel('probability density')
ax[0].set_xlim(left=x_min,right=x_max)
ax[1].text(
        0.05,0.95,
        '(a) pdf',
        transform=ax.transAxes,
        fontsize=14,
        vertical_alignment="top",
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


ax[1].hist(sample_rv,
        bins=n_bins,
        density=True,
        histtype='step',
        cumulative=True,
        color='black',
        label='sampling')


ax[1].plot(x,cdf)
ax[1].set_xlabel('X')
ax[1].set_ylabel('cumulative density')
ax[1].set_xlim(left=x_min,right=x_max)
ax[1].text(
        0.05,0.95,
        '(b) cdf',
        transform=ax.transAxes,
        fontsize=14,
        vertical_alignment="top",
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.savefig(
        plot_fn,
        dpi=plot_dpi)
plt.close(fig)

