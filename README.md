# Surprisingly Popular Answer

## About
This repo is an implementation of the Surprisingly Popular Answer ([Prelec, D., Seung, H. & McCoy, J. A solution to the single-question crowd wisdom problem](https://doi.org/10.1038/nature21054)), in Python.
The algorithm is implemented in `spa.py`, while an example usage of NFL 2017 data is available in the notebook `spa_nfl_2017.ipynb`.


## The Data:

Since we couldn't obtain the original paper ([Prelec, D., Seung, H. & McCoy, J. A solution to the single-question crowd wisdom problem](https://doi.org/10.1038/nature21054)) data, we searched for alternatives datasets that do contain meta-cognitive judgments.

We found two follow-up papers that attempted the evaluate SPA over different domains: 
- [Lee, M.D., Vi, J., & Danileiko, I. (2017), Testing the ability of the surprisingly popular algorithm to predict the 2017 NBA playoffs. Working paper](https://osf.io/hq6a4/).
- [Rutchick, A.M., Ross, B.J., Calvillo, D.P. et al. Does the “surprisingly popular” method yield accurate crowdsourced predictions?. Cogn. Research 5, 57 (2020)](https://doi.org/10.1186/s41235-020-00256-z)

We used the data from both papers. However, since the NBA dataset (Lee et al.) exhibited a consensus among respondents, which was correct (All aggregation methods predicted correctly all games but one), and after further reading about NBA playoffs patterns (which do not contain high variance), we decided to focus on the NFL dataset from Rutchick el al. (Study 1).  
The participants (227) were recruited from a psychology course. Each participant was asked to predict the results of the NFL season games (2017).  
It's important to point out that the original paper, respondents were asked about questions with a "known" answers, such as state capitals. In this dataset, respondents were asked about future outcomes. A reasonable argue is that these kind of questions usually require higher level of expertise in the subject.