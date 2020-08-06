# bootstrapNW
Bootstrapping NW Outcomes

Simple example of bootstrapping different market growth scenarios to understand your possible net wealth outcomes at retirement. 

SCENARIOS:

•	Normal: The market continues on as it has since 1970, and you keep making contributions to your retirement accounts equal to today's contributions.  Each year between age 38 and 55, you take a randomly assigned market growth, and subtract a randomly assigned inflation rate, to get that year's inflation-adjusted growth rate.
•	Downward Growth: Same as before, except you subtract a flat 5% off the real values of past market growth (leaving inflation and unemployment rates unchanged), and then re-run the covariance matrix and means. This simulates a pretty rough economic climate where the market is performing ~33% worse than the past 50 years, and yet unemployment chances and inflation are unchanged. 
•	Unemployment: Same as scenario 1, except that there is a chance of being unemployed each year that is half the randomly assigned unemployment rate for a given year (i.e. if unemployment is at 8%, then you have a 4% chance of being unemployed in that year). Once unemployed, you are randomly assigned a 1- or 2-year period of unemployment, during which retirement contributions drop to 25% their previous rate. In this scenario you encounter 39% of runs where you end up unemployed at least once (with occasional runs where you are unemployed multiple times).
•	Baseline: It is helpful to compare the results of the scenarios against a 4% baseline.  To get this, I take the given annual contribution, assume the market maintains 4% every year, and see where that ends up at age 55 (I use the same formula behind Excel's FV to calculate this future value).
