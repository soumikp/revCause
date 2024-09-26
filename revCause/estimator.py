import numpy as np
import scipy.stats as st
from fastkde import fastKDE

def estimator(x, alpha=0.05):
    
    if x.shape[0] % 2 != 0:
        x = x[:-1]  # Ensure an even number of rows
    
    estim, inf = np.split(x, 2)  # Split data into two halves
    
    # First split used for density estimation
    margin_x = fastKDE.pdf_at_points(var1=estim[:, 0], list_of_points=list(inf[:, 0]))
    margin_y = fastKDE.pdf_at_points(var1=estim[:, 1], list_of_points=list(inf[:, 1]))
    select = np.logical_and(margin_x > 0, margin_y > 0)
    
    margin_x = margin_x[select]
    margin_y = margin_y[select]
    
    h_x1 = -np.mean(np.log(margin_x))
    h_y1 = -np.mean(np.log(margin_y))
    covar1 = np.cov(np.log(margin_x), np.log(margin_y))
    delta_var1 = covar1[0, 0] + covar1[1, 1] - 2 * covar1[0, 1]
    
    # Second split used for density estimation
    margin_x = fastKDE.pdf_at_points(var1=inf[:, 0], list_of_points=list(estim[:, 0]))
    margin_y = fastKDE.pdf_at_points(var1=inf[:, 1], list_of_points=list(estim[:, 1]))
    select = np.logical_and(margin_x > 0, margin_y > 0)
    
    margin_x = margin_x[select]
    margin_y = margin_y[select]
    
    h_x2 = -np.mean(np.log(margin_x))
    h_y2 = -np.mean(np.log(margin_y))
    covar2 = np.cov(np.log(margin_x), np.log(margin_y))
    delta_var2 = covar2[0, 0] + covar2[1, 1] - 2 * covar2[0, 1]
    
    # Cross fitting
    h_x = (h_x1 + h_x2) / 2
    h_y = (h_y1 + h_y2) / 2
    delta = h_x - h_y
    
    # Variance estimation using Monte Carlo
    delta_var = (delta_var1 + delta_var2) / 2
    delta_sd = np.sqrt(delta_var)
    
    delta_lcb = delta - st.norm.ppf(1 - alpha / 2) * delta_sd / np.sqrt(np.sum(select))
    delta_ucb = delta + st.norm.ppf(1 - alpha / 2) * delta_sd / np.sqrt(np.sum(select))
    
    return [h_x, h_y, delta_lcb, delta, delta_ucb, delta_sd / np.sqrt(np.sum(select))]