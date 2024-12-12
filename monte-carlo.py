
from numpy.random import normal
import matplotlib.pyplot as plt

#Define the distribution
#We'll use a Gaussian distribution with mean=50 and SD=5 and draw random samples from this distribution
mu = 50
sigma = 5

# generate MC samples of differing size
sizes = [100, 1000, 10000]
for i in range(len(sizes)):

  sample = normal(mu, sigma, sizes[i])
  plt.subplot(3, 3, i+1)
  plt.hist(sample, bins = 20)
  plt.title('%d samples' % sizes[i])
  plt.xticks([])

plt.show()
