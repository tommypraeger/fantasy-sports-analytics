from scipy.stats import norm
import numpy as np

def stdDev(arr):
    return np.std(arr, ddof=1)

def winLikelihood(first, second, stdDev):
    return norm.cdf(first - second, 0, stdDev)