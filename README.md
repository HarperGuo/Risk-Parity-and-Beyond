# Risk Parity and Beyond

##### ---- a novel definition of contributions to risk 




This is for the final project of FRE-GY 6331 Financial Risk Management and Optimization 

May 15th 2017

Instructor: Professor Daniel Totouom 

  

[TOC]

​    

## 1. Introduction

Risk budgeting, the fair attribution of the total risk of a portfolio, and risk parity, equal contribution to the risk of the total portfolio are two highly related, though different, concepts. They are more and more applied to portfolio management both in academia and industry.

The traditional method to computing risk contribution is by means of marginal risk. Our project is to implement an alternative method, proposed by Romain Deguest, etc (2013), in the paper *Risk Parity and Beyond - From Asset Allocation to Risk Allocation Decisions*. Instead of marginal risk, we measure risk contribution by uncorrelated bets.

A natural start point of computing uncorrelated bets is PCA (principle components analysis), from which orthogonal eigenvectors are obtained. But the method of principle components bets suffers some innate flaws, which drives us to explore alternative methods.

Fortunately, besides PCA, there are several alternative method of zero-correlation transformation of original factors. Here we introduce a method called Minimum Torsion Bets, which is a de-correlating transformation but is closest to the original factors.  

​    

​    

## 2. Effective Number of Bets

A portfolio is a combination of $n$ correlated assets, and the portfolio return is a weighted average of the return of each asset $R = \Sigma^{n}_{i=1} w_i R_i$, where $w_i$ is the weight of $i$-th asset. 

More in general, a portfolio is a combination of $k$ correlated factors, for instance, Fama-French Five Factors model. Thus, the portfolio return is a combination of the return of each factor:
$$
R = \sum_{i=1}^k b_i F_i
$$
where $b_i$ is the exposure of $i$-th factor 

But if we run a linear regression to obtain the factor-based portfolio return, it would cause a problem: co-linearity for the reason that those factors are correlated. 

In order to solve this problem, we aspire to have a portfolio which is a combination of uncorrelated factors:
$$
R=\sum_{i=1}^k \tilde{b}_i \tilde{F}_i
$$
where $\Bbb{Cr} (\tilde{F}_i, \tilde{F}_j)=0$ if $ i \neq j$. ($\Bbb{Cr}$ denotes the correlation.)

Then, we can compute the Diversification Distribution, namely true relative contributions to total risk from each bet. For $i=1,2,...,k$,
$$
p_i =\frac {\Bbb{V}( \tilde{b}_i \tilde{F}_i)}{\Bbb{V}(R)}
$$
where $\Bbb{V}$ denotes the variance. Note that for any distribution, $p_i$ sums up to $1$ and non-negative.

If $p_1=p_2=...=p_k$, the risk parity is achieved, or the portfolio is well diversified. To quantify diversification, we use the exponential of the entropy that measures the uniformity of a distribution. We define the **Effective Number of Bets** as follows:
$$
\Bbb{N}=e^{-\sum_{i=1}^k p_i * ln(p_i)}
$$
In the case of full concentration, let's say, one factor represents all the risks, the entropy would be $0$, and the Effective Number of Bets would be $1$. Oppositely, in the case of full diversification, each factor represents equal risk contribution, then the Effective Number of Bets would $k$. In general, $1 \leq \Bbb{N} \leq k$.

​    

​    

## 3. Principle Components Bets

In order to construct a portfolio as a combination of uncorrelated factors, a natural start point is principle components analysis on the original factors $\bf{F}$. 

Basically, to perform PCA:
$$
\bf{\Sigma_{F}} = eDe^T
$$
where the covariance of the original factors $\Bbb{Cv}(\bf{F})=\Sigma_{\bf{F}}$. Performing PCA decomposition, we obtain $\bf{D}$ and $\bf{e}$, where $\bf{D}$ is the diagonal matrix of eigenvalues of $\bf{\Sigma_{F}}$, and $\bf{e}$ is the matrix whose columns are eigenvectors of $\bf{\Sigma_{F}}$. 

$\bf{e}$ is orthogonal, that is, $\bf{e}^T\bf{e}=\bf{e}\bf{e}^T=I$. 

Therefore, we have
$$
\bf{\tilde{F}_{PC}}=e^T F
$$

$$
\bf{\tilde{b}_{PC}} =e^T b
$$

$$
\bf{R}=b^T F ={\tilde{b}_{PC}^T} \tilde{F}_{PC} = b^Tee^TF
$$

Then given the exposures $\bf{b}$, we can compute the **Principal Components Diversification Distribution** and the **Effective Number of Principal Components Bets**:
$$
\bf{p}_{PC}(b)=\frac {(e^T b) \cdot (e^T \Sigma_{F} b)} {b^T \Sigma_{F} b}
$$

$$
\Bbb{N}_{PC}({\bf{b}})=e^{-{\bf{p}_{PC}(b)^T \, ln(p_{PC}(b))}}
$$

where $\cdot$ is element-wise product. 

However,  PCA suffers some innate flaws: 

First, principal components are usually uninterpretable. 

Second, principle components are not unique. For instance, $e_i$ is $i$-th eigenvector, so is $-e_i$.

Third, principal components would not be coherent with its simple scale transformations.

​    

​    

## 4. Minimum Torsion Bets

Since principle components' innate flaws, we may think of some alternative methods. There exist several alternative factor rotations, or torsions $\bf{\tilde{F}}=\tilde{t} F$. For instance, we could use the lower-triangular Cholesky decomposition, ${\bf{\Sigma_F}=LL^T}$,  where ${\bf{\tilde{t}}=L^{-1}}$. Because ${\Bbb{Cv}}({\bf{L^{-1} F})=L^{-1} L L^{T} L^{T-1}=I}$, thus $\bf{\tilde{F}}=L^{-1} F$ are uncorrelated. But such transformations suffer the same problems as PCA.

   

#### 4.1 Minimum Torsion Transformation

Now we attempt to find out an alternative de-correlation method: we choose a linear transformation that least distort the original factors $\bf{F}$. To be more specific, we intend to minimize the tracking error with respect to the original factors, under the constraint that the correlation of transformed factors is identity matrix.
$$
{\bf{\tilde{t}_{MT}}} = argmin_{{\Bbb{Cr({\bf{tF}})=I}}} NTE({\bf{tF \mid F}})
$$
where NTE is normalized tracking error:
$$
NTE({\bf{Z \mid F}})=\sqrt{\frac{1}{k} \sum_{i=1}^k{\Bbb{V}(\frac{Z_i-F_i}{{\Bbb{Std}(Z)}})}}
$$
If we are able to solve this optimization problem, we will obtain
$$
\bf{\tilde{F}_{MT}}=\tilde{t}_{MT}^T F
$$

$$
\bf{\tilde{b}_{MT}} =\tilde{t}_{MT}^{T-1} b
$$

$$
\bf{R}={\tilde{b}_{MT}^T} \tilde{F}_{MT} 
$$

Then given the exposures $\bf{b}$, we can compute the **Minimum Torsion Diversification Distribution** and the **Effective Number of Minimum Torsion Bets**:
$$
\bf{p}_{MT}(b)=\frac {(\tilde{t}_{MT}^{T-1}b)\cdot (\tilde{t}_{MT} \Sigma_{F} b)} {b^T \Sigma_{F} b}
$$

$$
\Bbb{N}_{MT}({\bf{b}})=e^{-{\bf{p}_{MT}(b)^T \, ln(p_{MT}(b))}}
$$

Now the Minimum Torsion factors are unique, coherent with its simple scale transformations, and interpretable because they have same meanings with original factors.

​    

#### 4.2 Optimization Problem Solution

The solution of the minimum torsion optimization (11) is a special instance of a  quadratic program with constraints. We obtain the solution by first computing analytically a starting guess, and then perturbing the starting guess via an efficient recursive algorithm, as follows. 

Let's present the covariance matrix $\bf{\Sigma_F}$ by extract standard deviation of factors ${\bf{\sigma_F}}$ and correlation matrix $ {\bf{C_F}}$, that is
$$
{\bf{\Sigma_F}}=diag({\bf{\sigma_F}}) {\bf{C_F}} diag{(\bf{\sigma_F}})
$$
where $diag()$ is to embeds the vector into the principal diagonal of a square matrix which is zero anywhere else. 

Then let's decompose correlation matrix via its Riccati root $\bf{c}$, that is,
$$
\bf{C_F}=cc'
$$
where we emphasize that the factors cannot be collinear, otherwise the inverse Riccati root $\bf{c^{-1}}$ is not defined.

Next, we compute a perturbation matrix $\bf{\pi}$ recursively with the algorithm below:

1. initialize:

$$
\bf{I} \to d
$$

2. Riccati root 

$$
(\bf{d c^2d})^{\frac{1}{2}} \to u
$$

3. Rotation 

$$
\bf{u^{-1}dc} \to q
$$

4. Stretching 

$$
diag(\bf{qc}) \to d
$$

5. Perturbation 

$$
\bf{dq} \to \pi
$$

6. If convergence, output $\bf{\pi}$; otherwise go back to step 1.

The solution reads:
$$
{\bf{\tilde{t}_{MT}}}=diag({\bf{\sigma_F}}) {\bf{\pi c^{-1}}} diag({\bf{\sigma_F}})^{-1}
$$
​    

​    

  ## 5. Case study

Let's create a portfolio of N=425 stocks in S&P 500 index. In this case each stock is a factor $\bf{F}$ and each stock's weight in portfolio is the respective exposure $\bf{b}$. We estimate every month the covariance matrix of the of the S&P stock returns $\bf{F}$ using a 900-day rolling window of daily observations. 

We have three scenarios: 

i.) Equal weights;

ii.) Mean-variance optimized weights;

iii.) Black-Litterman optimized weights.

​    

##### scenario i.) 

When we are in scenario i.), or the Minimum-Torsion Diversification Distribution $\bf{p}_{MT}(b_{eq})$  and portfolio weights $\bf{b_{eq}}$: 

![p_mt_0](C:\Users\Hao Guo\Pictures\p_mt_0.PNG)

where x-axis is the window-rolling times, y-axis is the number of stocks, z-axis is Minimum-Torsion Diversification Distribution and portfolio weights.

It indicates that equal-weight allocation provide a portfolio that is not as diversified as expected. Unlike the portfolio weights, the Minimum-Torsion Diversification Distribution is not flat: some stocks are riskier than others, a fact good to known for portfolio managers. 

As for principle components diversification distribution and portfolio weights:

![p_pc_0](C:\Users\Hao Guo\Pictures\p_pc_0.PNG)

Recall that the marginal risk contribution is 
$$
\bf{m}=\frac{b \cdot (\Sigma_Fb)}{b^T \Sigma_F b}
$$
![mr_0](C:\Users\Hao Guo\Pictures\mr_0.PNG)

We can see that the overall risk profile generated by marginal risk contribution is similar to the Diversification Distribution.

​    

##### scenario ii.)

When we are in scenario i.), or the Minimum-Torsion Diversification Distribution $\bf{p}_{MT}(b_{mv})$  and portfolio weights $\bf{b_{mv}}$. Here we all consider no-short-selling constraint, and we set risk aversion coefficient is 1. The result is the following: 

![p_mt_1_mv](C:\Users\Hao Guo\Pictures\p_mt_1_mv.PNG)

where x-axis is the window-rolling times, y-axis is the number of stocks, z-axis is Minimum-Torsion Diversification Distribution and portfolio weights.

It indicates that Minimum-Torsion Diversification Distribution display the relative contribution of each risk source. It reflects Minimum-Torsion Diversification Distribution's interpretability.

As for principle components diversification distribution and portfolio weights:

![p_pc_1_mv](C:\Users\Hao Guo\Pictures\p_pc_1_mv.PNG)

Here we can say that principle components diversification distribution fails to deliver correct risk profile and we notice negative contributions for some factors. 

   

##### scenario iii.)

When we are in scenario i.), or the Minimum-Torsion Diversification Distribution $\bf{p}_{MT}(b_{bl})$ and portfolio weights $\bf{b_{bl}}$. In black-litterman framework, we assume the mean-variance optimized weights are equilibrium weights and we form two views: equilibrium weights portfolio has historical mean returns as expected return and equal weights portfolio has appropriate random number as expected return. Here we all consider no-short-selling constraint: 

![p_mt_2](C:\Users\Hao Guo\Pictures\p_mt_2.PNG)

where x-axis is the window-rolling times, y-axis is the number of stocks, z-axis is Minimum-Torsion Diversification Distribution and portfolio weights.

Again, it shows that Minimum-Torsion Diversification Distribution is generally able to catch the relative contribution of each risk source. It reflects Minimum-Torsion Diversification Distribution's interpretability.

As for principle components diversification distribution and portfolio weights:

![p_pc_2](C:\Users\Hao Guo\Pictures\p_pc_2.PNG)

Again, we can say that principle components diversification distribution fails to catch relative contribution of risk and we notice negative contributions for some factors. It reflects its disadvantage of interpretability. 

​    

​    

## 6. Conclusion

We have implemented the Minimum Torsion Bets, the transformation of correlated factors into uncorrelated factors. Unlike the Principal Component Bets, the Minimum-Torsion Bets are more interpretable. 

We expect to implement Minimum Torsion Bets to have impact on the job of risk budgeting and risk parity. In our case study, Minimum-Torsion Bets manage to closely track the factors used in the allocation. In this way, we turn the asset allocation into risk allocation.

​    

​    

## Reference 

Deguest, R., Martellini, L., and Meucci, A. (2013). Risk parity and beyond - from asset allocation to risk allocation decisions, EDHEC Risk Working Paper.

​    

​     

## Appendix

The attached python codes are the following:

* DataManip.py: the scripts to load and wrangle data. 

* Weights.py: the functions to return weights in the three scenarios, that is, the equal weights, mean-variance optimized weights and Black-litterman weights.

* torsion.py: the functions to return  ${\bf{\tilde{t}_{MT}}}$

* EffectiveBets.py: the functions to return diversification distribution $\bf{p}$ and effective number of bets $\Bbb{N}$

* Main1.py: the scripts to run scenario i), equal weights portfolio

* Main2.py: the scripts to run scenario ii),  mean-variance optimized weights portfolio

* Main3.py: the scripts to run scenario iii),  Black-litterman weights portfolio

  ​
