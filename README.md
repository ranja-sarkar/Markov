
A **deterministic model** is specified by a set of equations that describe how the system will evolve over time. The evolution is at least partially random in a **stochastic model**, and the model will not give identical results if the process is run several times. Different runs of a stochastic model are often called realisations of the process.

The distinction between deterministic and stochastic models is also blurred slightly by chaotic models. A chaotic model is a deterministic model which is extremely sensitive to the values of some parameters in the model. Making a very small change to the values of these parameters can make the outcome of the model completely different. Some people have argued that a system normally regarded as a stochastic process be better regarded as chaotic deterministic system, as exemplified by the quote:-

*A mountain stream, a beating heart, a smallpox epidemic, and a column of rising smoke are all examples of dynamic phenomena that sometimes seem to behave randomly. In reality, such processes exhibit a special order. This special order is ’deterministic chaos’ or chaos in short.*

Examples of **stochastic processes** -

1. Random walk

2. Markov chain

3. Weiner process or Brownian motion

   
**Chapter 8** of my book discusses **Markov chain**. It is a mathematical system describing a sequence of events in which the probability of each event depends only on the previous event.

 **“The future depends only upon the present, not upon the past."**

**M**arkov **C**hain **M**onte **C**arlo is a random sampling method used to sample from a target population/distribution defined by high dimensions, and there're a few MCMC algorithms. Following two of them have been explained in the book.   

<img width="174" alt="22" src="https://github.com/user-attachments/assets/ac96a335-b68f-411e-bb73-85ba84ed70aa">

Buy from Amazon: https://a.co/d/1zUEkNQ

**Gibbs sampling is a special case of the Metropolis-Hastings algorithm**, the former algorithm relies on conditional distributions and the latter uses a joint (density) distribution to generate samples.

**Metropolis-Hastings:**

https://colab.research.google.com/drive/1JZWLvPArxUYz215idmgWylvmuf42b4lF



<img width="276" alt="MH1" src="https://github.com/user-attachments/assets/744fcf54-3cd2-408f-9cb9-224b822f179a">

<img width="276" alt="MH2" src="https://github.com/user-attachments/assets/43b5d6c8-e89c-42b8-8314-115693133e5e">


**Gibbs:**

Given a multivariate (two or more) distribution, it is simpler to sample from a conditional distribution than from a joint distribution.

<img width="347" alt="g1" src="https://github.com/user-attachments/assets/1a28c36f-a58b-4ba1-a3cd-af611bfca32e">
<img width="322" alt="g2" src="https://github.com/user-attachments/assets/9e593afd-ec97-4cd0-9bf1-66d4b885696b">


**More about Markov chains:** https://github.com/Smeths/Markov_Chains/blob/master/Markov%20Notes.ipynb/


**Note on Monte-Carlo Sampling**

Monte-Carlo sampling provides the foundation for many ML algorithms such as resampling, hyperparameter tuning, and ensemble learning. 

A desired quantity can be approximated by random sampling of a probability distribution - MC sampling is one method for this. A quantity may be intractable for many reasons, such as the stochastic nature of the domain, noise in the observations, the lack of observations, and more. 

*Drawing a sample may be as simple as calculating the probability for a randomly selected event, or may be as complex as running a computational simulation, the latter often referred to as a Monte Carlo simulation.*

*The bootstrap is a simple Monte Carlo technique to approximate the sampling distribution and is particularly useful in cases where the estimator is a complex function of the true parameters.*

**Simulated annealing** is another example of MC sampling. Find a little more about it from **Chapter 10** of my book. 

<img width="174" alt="22" src="https://github.com/user-attachments/assets/ac96a335-b68f-411e-bb73-85ba84ed70aa">

Let us suppose we don’t know the form of the probability distribution for a random variable and we want to sample the function (defines the probability distribution of the random variable) to get an idea of the probability density. We can draw a sample of a given size and plot a histogram to estimate the density. As the size of the sample is increased, the probability density better approximates the true density of the target function, given the law of large numbers. 

<img width="359" alt="33" src="https://github.com/user-attachments/assets/f71d8b43-7d5c-445c-8757-83e61fed62ac" />


This highlights the need to draw many samples, even for a simple random variable. We clearly see how the largest size here resembles a Gaussian (bell-shaped) distribution.
