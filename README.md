
A **deterministic model** is specified by a set of equations that describe how the system will evolve over time. The evolution is at least partially random in a **stochastic model**, and the model will not give identical results if the process is run several times. Different runs of a stochastic model are often called realisations of the process.

The distinction between deterministic and stochastic models is also blurred slightly by chaotic models. **A chaotic model is a deterministic model which is extremely sensitive to the values of some parameters in the model. Making a very small change to the values of these parameters can make the outcome of the model completely different**. Some people have argued that a system normally regarded as a stochastic process be better regarded as chaotic deterministic system, as exemplified by the quote:-

*A mountain stream, a beating heart, a smallpox epidemic, and a column of rising smoke are all examples of dynamic phenomena that sometimes seem to behave randomly. In reality, such processes exhibit a special order. This special order is ’deterministic chaos’ or chaos in short.*

Examples of **stochastic processes** -

1. **Random walk** -> It's a **discrete-time** stochastic process. A collection of random variables (iid - independent & identically distributed) such that y_i moves ±1 at each step with equal probability (of each variable's occurence) make up an 1D simple random walk. Refer: https://github.com/ranja-sarkar/Markov/blob/main/references/BM.ipynb 

2. **Markov chain** -> It's a stochastic process of a sequence of events such that y_(i+1) depends only on y_i and not on the whole set of values y_0, y_1, y_2, ....., y_i which means the effect of the past on the future is summarized only by the present or current state rather than the whole sequence of states or history.

   A Markov chain at a high level is a graph of states over which the sampling algorithm takes a random walk.

3. **Weiner process** or Brownian motion -> It's a **continuous-time** stochastic process.
   Refer: https://github.com/ranja-sarkar/Markov/blob/main/references/BM.ipynb
   
   
**Chapter 8** of my book named "A handbook of mathematical models with python" discusses **Markov chain**. 

 **“The future depends only upon the present, not upon the past."**

**M**arkov **C**hain **M**onte **C**arlo is a random sampling method used to sample from a target population/distribution defined in high dimensions by constructing a Markov Chain, where the next sample drawn from the probability distribution is dependent upon the just the previous sample drawn. The idea is that the chain will settle on (or find equilibrium) on the desired quantity we're inferring. 

For most probabilistic models of practical interest, exact inference is intractable, so we have to resort to some form of approximation (expected value or density). The desired calculation is typically a sum of a discrete distribution of many random variables or integral of a continuous distribution of many variables. 

<img width="174" alt="22" src="https://github.com/user-attachments/assets/ac96a335-b68f-411e-bb73-85ba84ed70aa">

Buy from Amazon: https://a.co/d/1zUEkNQ

**Gibbs sampling is a special case of the Metropolis-Hastings algorithm**, the former algorithm relies on conditional distributions and the latter uses a joint (density) distribution to generate samples.

**Metropolis-Hastings:**

This algorithm involves using a surrogate (kernel) or proposal probability distribution that is sampled, then an acceptance criterion that decides whether the new sample is accepted into the chain or discarded. The proposal suggests an arbitrary next step in the chain trajectory and the acceptance ensures appropriate limiting direc­tion is maintained by rejecting unwanted moves in the chain. The acceptance criterion is probabilistic based on how likely the proposal distribution differs from the true next-state probability distribution.

For example, if the next-step conditional probability distribution is used as the proposal distribution, Metropolis-Hastings is equivalent to the Gibbs Sampling algorithm. If a symmetric proposal distribution is used like a Gaussian, the algorithm is equivalent to another MCMC called the Metropolis algorithm.

https://colab.research.google.com/drive/1JZWLvPArxUYz215idmgWylvmuf42b4lF


<img width="276" alt="MH1" src="https://github.com/user-attachments/assets/744fcf54-3cd2-408f-9cb9-224b822f179a">

<img width="276" alt="MH2" src="https://github.com/user-attachments/assets/43b5d6c8-e89c-42b8-8314-115693133e5e">


**Gibbs:**

Given a multivariate (two or more) distribution and calculated conditional probability, it is simpler to sample from a conditional distribution than from a joint distribution. The idea behind Gibbs sampling is that we sample each variable in turn, conditioned on the values of all the other variables in the distribution. Gibbs Sampling is appropriate for discrete (rather than continuous) distribution.


<img width="347" alt="g1" src="https://github.com/user-attachments/assets/1a28c36f-a58b-4ba1-a3cd-af611bfca32e">
<img width="322" alt="g2" src="https://github.com/user-attachments/assets/9e593afd-ec97-4cd0-9bf1-66d4b885696b">


MCMC algorithms are sensitive to starting points, and often require a warm-up phase (burn-in) to move in towards a fruitful part of the search space, after which prior samples can be discarded and useful samples collected.

**More about Markov chains:** https://github.com/Smeths/Markov_Chains/blob/master/Markov%20Notes.ipynb/


**Note on Monte-Carlo Sampling**

Monte-Carlo sampling provides the foundation for many ML algorithms such as resampling, hyperparameter tuning, and ensemble learning. Unlike Monte Carlo sampling methods (drawing independent samples from probability distribution and repeat the process many times to approximate desired quantity), MCMC methods draw a sample which is dependent on the existing sample.

A desired quantity can be approximated by random sampling of a probability distribution - MC sampling is one method for this. A quantity may be intractable for many reasons, such as the stochastic nature of the domain, noise in the observations, the lack of observations, and more. 

*Drawing a sample may be as simple as calculating the probability for a randomly selected event, or may be as complex as running a computational simulation, the latter often referred to as a Monte Carlo simulation.*

*The bootstrap is a simple Monte Carlo technique to approximate the sampling distribution and is particularly useful in cases where the estimator is a complex function of the true parameters.*

Monte Carlo sampling is not effective and may be intractable for high-dimensional probabilistic models, MCMC provides an alternate approach. 


**MCMC with scipy:** https://people.duke.edu/~ccc14/sta-663/MCMC.html

**Simulated annealing** is another example of MC sampling. Find a little more about it from **Chapter 10** of my book. 

<img width="174" alt="22" src="https://github.com/user-attachments/assets/ac96a335-b68f-411e-bb73-85ba84ed70aa">

Let us suppose we don’t know the form of the probability distribution for a random variable and we want to sample the function (defines the probability distribution of the random variable) to get an idea of the probability density. We can draw a sample of a given size and plot a histogram to estimate the density. As the size of the sample is increased, the probability density better approximates the true density of the target function, given the law of large numbers. 

<img width="359" alt="33" src="https://github.com/user-attachments/assets/f71d8b43-7d5c-445c-8757-83e61fed62ac" />


This highlights the need to draw many samples, even for a simple random variable. We clearly see how the largest size here resembles a Gaussian (bell-shaped) distribution. 

**Lectures on Computational Statistics from Duke University:** https://people.duke.edu/~ccc14/sta-663-2018/

