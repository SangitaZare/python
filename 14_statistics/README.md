# 14 · Statistics for Data Science

**👉 Start with the notebook: [statistics_tutorial.ipynb](statistics_tutorial.ipynb).** It uses the shop data from topics 12–13 to show every idea below with real numbers and charts.

To run it yourself:

```bash
.venv\Scripts\activate             # Windows; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cd 14_statistics
jupyter notebook statistics_tutorial.ipynb
```

**Why statistics?** Charts show patterns, but patterns also appear by pure chance. Statistics tells you **how much to trust** what you see, and that's the difference between an analyst who reports patterns and one whose conclusions hold up.

---

## Part A: Describing data

### Centre

| Measure | What it is | Use it when |
|---------|-----------|-------------|
| **Mean** | Sum ÷ count | The data is roughly symmetric, without extreme values |
| **Median** | The middle value | The data is **skewed** or has outliers (prices, incomes, order values) |
| **Mode** | The most frequent value | Categories, or "the most common choice" |

In our shop data the mean order is **₹2,308** but the median is **₹1,497**. A few big orders pull the mean up, so the median is the honest "typical order".

### Spread

| Measure | What it is | Pairs with |
|---------|-----------|------------|
| Range | max − min | (Too sensitive to one extreme value) |
| **Standard deviation** | Typical distance from the mean | Mean |
| **IQR** | Q3 − Q1: the range of the middle 50% | Median |
| Percentiles | The value below which X% of data falls | Reporting: "90% of orders are under ₹5,000" |

**Skewness** measures asymmetry: 0 is symmetric, and positive means a long right tail. (Ours is 2.4, strongly right-skewed.)

### Outliers

- **IQR rule:** below Q1 − 1.5×IQR or above Q3 + 1.5×IQR. Works for any shape, and it's what box plots use.
- **z-score rule:** |z| > 3, where `z = (x − mean) / std`. It assumes the data is bell-shaped.

An outlier is a reason to **investigate**, not automatically to delete. A ₹15,000 order is real and important.

## Part B: Distributions and sampling

### The normal distribution

The bell curve, described by its mean μ and standard deviation σ. **68–95–99.7 rule:** about 68% of values lie within 1σ of the mean, 95% within 2σ, and 99.7% within 3σ.

### Population vs sample

| | Population | Sample |
|---|---|---|
| What | **Everyone/everything** you care about | The part you actually measured |
| Numbers | Parameters: μ, σ | Statistics: x̄, s |
| Example | All customers who will ever shop | The 297 orders we have |

### The Central Limit Theorem (CLT)

If you take many samples and compute each sample's mean, **those means form a normal distribution, even when the data itself is skewed**, as long as the samples are large enough. Their spread is the **standard error**: `SE = s / √n`.

This is why so many statistical methods work: they rely on means being approximately normal. The notebook shows it happening with our skewed order values.

## Part C: Estimating with confidence

A **95% confidence interval** gives a range for an unknown value, like the true average order:

```python
from scipy import stats
low, high = stats.t.interval(0.95, df=n - 1, loc=mean, scale=stats.sem(data))
```

**Bootstrap** (resample your data with replacement thousands of times, then take the middle 95% of the results) works for medians and almost any other statistic, without formulas.

⚠️ **"95% confident" means:** if we repeated the study many times, 95% of the intervals would contain the true value. It does **not** mean "a 95% chance the true value is in this particular interval".

## Part D: Hypothesis testing

### The recipe

1. **H₀ (null hypothesis):** "nothing is going on": no difference, no effect.
2. **H₁ (alternative):** "there is a difference".
3. Choose **α** (usually 0.05) **before** looking at the data.
4. Compute the **p-value**: the probability of a result **at least this extreme if H₀ were true**.
5. If **p < α**, reject H₀ ("statistically significant"). Otherwise, there isn't enough evidence.

### Two kinds of mistakes

| | H₀ actually true | H₀ actually false |
|---|---|---|
| **Reject H₀** | ❌ **Type I error** (false positive), probability α | ✅ Correct |
| **Don't reject H₀** | ✅ Correct | ❌ **Type II error** (false negative), probability β |

**Power** = 1 − β = the chance of detecting a real effect. More data means more power.

### Which test?

| Question | Data | Test | SciPy |
|----------|------|------|-------|
| Do two groups have different **means**? | Numbers, roughly normal or large samples | Welch's t-test | `stats.ttest_ind(a, b, equal_var=False)` |
| Do two groups differ (skewed data, outliers)? | Numbers | Mann-Whitney U | `stats.mannwhitneyu(a, b)` |
| Same people measured twice (before/after)? | Paired numbers | Paired t-test | `stats.ttest_rel(before, after)` |
| Three or more groups? | Numbers | ANOVA / Kruskal-Wallis | `stats.f_oneway`, `stats.kruskal` |
| Do counts match what we expect? | One categorical variable | Chi-square goodness of fit | `stats.chisquare(counts)` |
| Are two categorical variables related? | A contingency table | Chi-square independence | `stats.chi2_contingency(table)` |
| Are two numbers related? | Two numeric columns | Pearson / Spearman | `stats.pearsonr`, `stats.spearmanr` |
| Did a change improve a rate (A/B test)? | Successes / trials | Two-proportion z or chi-square | `stats.chi2_contingency` |

### What we found in the shop data

| Question | Result | Conclusion |
|----------|--------|------------|
| Are Clothing orders bigger than others? | p < 0.000001, Cohen's d = 0.88 | **Yes**, and the effect is large |
| Clothing vs Electronics? | t-test p = 0.098, **Mann-Whitney p = 0.0006** | A typical Clothing order is larger. The t-test missed it because of Electronics' extreme orders |
| Does the weekday matter? (Thu 54 vs Sun 31) | p = 0.24 | **Can't tell**: gaps like this happen by chance |
| Do cities prefer different payment methods? | p = 0.28 | No evidence |
| More orders → more revenue? | r = 0.64, p < 0.001 | Yes, a strong positive relationship |
| Did the new checkout page work? (A/B) | 5.0% → 6.5%, p = 0.03 | Yes, a 30% relative lift |

## Traps that fool even experienced analysts

1. **Correlation ≠ causation.** Ice-cream sales and drownings rise together because of summer, not because one causes the other. Only experiments (A/B tests) show cause.
2. **"Not significant" ≠ "no difference".** It means the data can't tell. Thursday vs Sunday may well differ; 300 orders just aren't enough to know.
3. **Statistical vs practical significance.** With a million rows, a ₹1 difference can be "significant" but useless. Always report the **effect size** too.
4. **p-hacking.** Test 20 random things and about one will be "significant" at α = 0.05 by luck. Decide your tests in advance, or correct for multiple tests (e.g. Bonferroni: use α ÷ number of tests).
5. **Peeking** at an A/B test and stopping the moment p < 0.05. That inflates false positives. Fix the sample size first.
6. **Ignoring assumptions.** The t-test assumes roughly normal means, and chi-square needs expected counts ≥ 5. Our skewed data made the t-test and its intervals less reliable, which the notebook shows.
7. **Simpson's paradox.** A trend can reverse when you combine groups. Always check important results within subgroups too.

---

## Interview questions

**1. Mean or median: which would you report for salaries, and why?**
The median. Salaries are right-skewed, and a few very high earners pull the mean up, so the median better describes a typical employee.

**2. What is a p-value?**
The probability of seeing data at least as extreme as yours **if the null hypothesis were true**. It is *not* the probability that the null hypothesis is true.

**3. What are Type I and Type II errors?**
A Type I error is a false positive: rejecting a true null hypothesis (its probability is α). A Type II error is a false negative: missing a real effect (probability β). Lowering α reduces Type I errors but increases Type II errors, unless you collect more data.

**4. Explain the Central Limit Theorem and why it matters.**
The distribution of sample means approaches a normal distribution as the sample size grows, whatever the shape of the original data. It's why we can build confidence intervals and run t-tests on non-normal data with large enough samples.

**5. What is a confidence interval?**
A range built by a method that captures the true parameter in a stated percentage (e.g. 95%) of repeated samples. Wider intervals mean more uncertainty; larger samples give narrower intervals.

**6. When would you use Mann-Whitney U instead of a t-test?**
When the data is skewed, has outliers, or is ordinal (like ratings), especially with small samples. Mann-Whitney compares ranks instead of means.

**7. What is the difference between standard deviation and standard error?**
Standard deviation measures the spread of the **data**. Standard error measures the uncertainty of an **estimate** (like the mean): `SE = SD / √n`, so it shrinks as the sample grows.

**8. How would you design an A/B test?**
Define one primary metric and the minimum effect worth detecting. Calculate the sample size for the power you want (often 80%) at α = 0.05. Randomly split users, run until the planned size is reached without peeking, then test (two-proportion test or chi-square) and report both the p-value and the effect size with a confidence interval.

**9. What is the difference between statistical and practical significance?**
Statistical significance says an effect is unlikely to be chance. Practical significance asks whether it's big enough to matter. With huge samples, tiny useless effects become statistically significant.

**10. What is p-hacking, and how do you avoid it?**
Trying many analyses until something is significant, then reporting only that one. Avoid it by planning your hypotheses in advance, correcting for multiple comparisons, and reporting every test you ran.

**11. Pearson vs Spearman correlation?**
Pearson measures **linear** relationships and is sensitive to outliers. Spearman uses ranks, so it measures any **monotonic** (consistently rising or falling) relationship and is robust to outliers.

**12. What does a chi-square test of independence tell you?**
Whether two categorical variables are associated. It compares the observed counts in a contingency table with the counts expected if the variables were independent.

---

## Practice

Use `../12_pandas/data/sales_clean.csv`:

1. Compute the mean, median, standard deviation and IQR of `quantity`. Which centre measure would you report, and why?
2. Build a 95% bootstrap confidence interval for the **median** order value of Electronics.
3. Is the average order value different between **UPI** and **Card** payments? Choose a test, justify it, and interpret the result.
4. Are some categories more popular in some cities? Run a chi-square test on `city × category`.
5. Split the data into January–March and April–June. Is the average order value different between the halves?
6. Simulate p-hacking: generate 20 pairs of random groups **from the same distribution**, t-test each pair, and count how many are "significant".
7. **Challenge:** write your own permutation test function `permutation_test(a, b, n=10_000)` that returns a p-value, and check it against `stats.permutation_test`.
