# Spot-Check Report v2 — full before/after solution text


---

## 1. NOV_2017 (rec640/ann0) — AI-humanized
**Question:** What would be the company's market capitalization based on a share price of $80? Answer in billions of dollars.
**Answer:** before `30.16 billion dollars` / after `30.41 billion dollars` (changed by logic fix)
**GPTZero (solution):** before ai/ai=1.0  →  after human/ai=0.356

### BEFORE solution
0. ## Access Item 8 – Financial Statements and Supplementary Data.
I began by reviewing Item 8 of the 10-K report for NOV, which starts on page 53. This section includes the company's audited financial statements, specifically the Consolidated Balance Sheets and Consolidated Statements of Operations, which are essential for ratio analysis and understanding company performance.
We will be looking at the Income Statement on page 62, titled "CONSOLIDATED STATEMENTS OF INCOME (LOSS)."
1. ## Locate shares outstanding.
In the Consolidated Statement of Income on page 62, I first identified the total number of basic weighted average shares outstanding. The reported amount was 377 million.
2. ## Understand the market capitalization formula.
Market Cap = Outstanding Shares × Stock Price.
Market capitalization represents a company's total value based on its stock price multiplied by the number of shares outstanding.
3. ## Perform the market capitalization formula.
Market Cap = Outstanding Shares × Stock Price.
Market Cap = 377 × $80
Market Cap = $30,160
Convert to full units (billions):
$30,160 / 1,000
So, Market Cap is =
30.16 billion dollars

### AFTER solution
0. ## Step one.
NOV 10-K, Item 8, page 53. Income statement "CONSOLIDATED STATEMENTS OF INCOME (LOSS)" on page 62.
1. ## Step two.
Page 62 (physical page 60), balance sheets. Shares at December 31, 2017: 380,104,970 shares issued and outstanding.
2. ## Step three.
Formula used: market cap = outstanding shares times stock price. The question uses $80 per share.
3. ## Step four.
380,104,970 times 80 = 30,408,397,600. That is 30,408.3976 million. Divided by 1,000 that is 30.41 billion dollars.

---

## 2. BOOT_2024 (rec101/ann0) — AI-humanized
**Question:** If Boot Barn Holdings, Inc. had issued 400,000 new shares during fiscal year 2024 at $80 per share and allocated the full proceeds to increase cash and additional paid-in capital, what would the adjusted current ratio have been?
**Answer:** before `2.43` / after `2.43` (unchanged)
**GPTZero (solution):** before ai/ai=1  →  after human/ai=0.157

### BEFORE solution
0. ## Find current assets and current liabilities.
The Consolidated Balance Sheets table on Document page 57 contains the following information. The March 30 2024 financial data shows:
Total current assets amount to $729,649 while total current liabilities amount to $312,808.
The units are listed as “(In thousands, except per share data)”, so both values are in thousands of USD.
1. ## Calculate proceeds from the share issuance.
The company distributes 400,000 shares at a price of $80 per share.
The company generates $32,000,000 through the sale of 400,000 shares at $80 each.
$32,000 in thousands.
(In thousands, except per share data)
2. ## Add the proceeds to current assets.
The entire $32,000 amount goes into cash which belongs to current assets so we add it to the existing current assets balance.
The total current assets amount to $761,649 after adding $32,000 to the previous $729,649.
3. ## Recalculate the current ratio.
The formula requires calculation as follows:
Current Ratio = Current Assets ÷ Current Liabilities
= 761,649 ÷ 312,808 =
2.43

### AFTER solution
0. ## page 57 numbers
Consolidated Balance Sheets. March 30, 2024. in thousands. current assets = 729,649. current liabilities = 312,808.
1. ## new share proceeds
400,000 shares × 80 per share = 32,000,000 dollars = 32,000 in thousands.
2. ## adding to current assets
729,649 + 32,000 = 761,649.
3. ## ratio
761,649 / 312,808 = 2.43.

---

## 3. AE_2023 (rec24/ann0) — AI-humanized
**Question:** According to the chart titled “Performance Graph” in the document, what was the difference in total return performance between Adams Resources & Energy, Inc. and the S&P 500 index as of December 31, 2023?
**Answer:** before `128.42` / after `128.42` (unchanged)
**GPTZero (solution):** before ai/ai=1  →  after human/ai=0.417

### BEFORE solution
0. ## Locate the chart titled “Performance Graph”.
The Performance Graph chart appears on page 30 of the document with bold title at the top. The Performance Graph chart on page 30 of the document shows how Adams Resources & Energy Inc. and the S&P 500 and S&P Integrated Oil & Gas Index performed from December 31 2018 through December 31 2023.
1. ## Describe the components of the graph.
The Performance Graph presents a line chart showing the total return accumulation of three investments from December 2018 through December 2023. The X-axis (horizontal) shows the year-end points from 2018 to 2023 which represent yearly intervals. The Y-axis (vertical) shows indexed return values which start at $0 and increase by $50 steps up to $250. The investments start at $100 in 2018 and all subsequent years show dividend reinvestment.
The black line with diamond markers represents Adams Resources & Energy Inc. The S&P 500 Index uses black lines with square markers for its representation. The S&P Integrated Oil & Gas Index uses dark gray lines with triangular markers to represent its performance.
The performance of Adams Resources & Energy Inc. shows significant price swings while its value remains below its starting point in 2018. The S&P 500 demonstrates steady growth with controlled price movements. The S&P Integrated Oil & Gas Index shows significant price drops before recovering strongly to become the second most valuable investment at the end of the period.
2. ## Retrieve the data labels for the year ended December 31, 2023.
The chart includes a table which presents exact data labels for every year and each entry in the legend. The total return values for a $100 investment from December 31, 2018 to December 31, 2023 with dividend reinvestment amount to $78.79 for Adams Resources & Energy Inc. and $207.21 for the S&P 500.
3. ## Calculate the difference in total return performance between AE and the S&P 500.
The final 2023 value of Adams Resources & Energy Inc should be subtracted from the S&P 500 value to get the result: 207.21 (index value) - 78.79 (index value) = 
128.42

### AFTER solution
0. ## Graph on page 30.
Title: "Performance Graph." Document page: 30. Covers December 31, 2018 to December 31, 2023. Tracks Adams Resources and Energy Inc., S&P 500, and S&P Integrated Oil and Gas Index. $100 base in 2018, with dividends reinvested.
1. ## Reading the data.
The graph has a table below it with exact values per year-end. For December 31, 2023: Adams Resources and Energy Inc. = $78.79. S&P 500 = $207.21.
2. ## Subtraction.
207.21 minus 78.79 equals 128.42.
3. ## Answer.
The difference in total return performance between Adams Resources and Energy Inc. and the S&P 500 at December 31, 2023 is 128.42.

---

## 4. VAL_2024 (rec236/ann0) — AI-humanized
**Question:** The following assumptions were used to calculate Project Valaris Limited's "Net cash provided by operating activities" for December 31, 2025.
1.  The projected "Net income" for 2025 amounts to $380.0 million.
2.  The 2025 financial data for "Adjustments to reconcile net income to net cash provided by operating activities" section will use the exact 2024 reported cash flow impact amounts from the 2024 Consolidated Statements of Cash Flows.
    The following line items:
    * "Depreciation expense"
    * "Accretion of discount on the Notes Receivable from ARO"
    * "Share-based compensation expense"
    * "Equity in losses (earnings) of ARO"
    * "Deferred income tax expense (benefit)"
    * "Net (gain) loss on sale of property"
    * "Changes in contract liabilities"
    * "Changes in deferred costs"
    * "Other" (adjustments)
    * "Contributions to pension plans and other post-retirement benefits"
3.  The 2025 operating assets and liabilities section shows the following cash flow effects:
    The cash outflow from accounts receivable will amount to $70.0 million according to the "(Increase) decrease in accounts receivable" line.
    The line item "Increase (decrease) in liabilities" shows a cash outflow of $100.0 million while the line item "(Increase) decrease in other assets" generates $25.0 million in cash inflow.
**Answer:** before `$357.2 million` / after `$357.2 million` (unchanged)
**GPTZero (solution):** before ai/ai=0.5  →  after human/ai=0.038

### BEFORE solution
0. ## Extract 2024 Actual Cash Flow Figures for Constant Items.
I have located the "CONSOLIDATED STATEMENTS OF CASH FLOWS" for the year ended December 31, 2024, on Page 43/88 (table from source 525) to extract the actual 2024 cash flow impact amounts for the items assumed to remain constant. All figures are in millions of dollars.
From "Adjustments to reconcile net income to net cash provided by operating activities":
"Depreciation expense": $122.1 (add-back)
"Accretion of discount on the Notes Receivable from ARO": ($40.0) (subtraction, as it's non-cash income)
"Share-based compensation expense": $27.7 (add-back)
"Equity in losses (earnings) of ARO": $11.0 (add-back, as it was a loss of $11.0 million in NI)
"Deferred income tax expense (benefit)": $5.8 (add-back, likely an expense)
"Net (gain) loss on sale of property": $0.2 (add-back, representing a loss of $0.2 million in NI)
"Changes in contract liabilities": ($31.7) (subtraction, increase in liability or recognition of deferred revenue)
"Changes in deferred costs": $39.3 (add-back, amortization or decrease in deferred costs)
"Other" (adjustments): $9.3 (add-back)
"Contributions to pension plans and other post-retirement benefits": ($21.5) (subtraction, cash outflow)
The unit is "(in millions)" as stated on Page 43/88.
1. ## List Projected 2025 Net Income and Constant Adjustment Items.
Based on the problem assumptions and Step 1:
Projected "Net income" for 2025 (Assumption 1) = $380.0 million.
Constant Adjustment Items (from Step 1, these are their 2024 cash flow impacts which are assumed for 2025):
Depreciation expense = +$122.1 million
Accretion of discount on the Notes Receivable from ARO = -$40.0 million
Share-based compensation expense = +$27.7 million
Equity in losses (earnings) of ARO = +$11.0 million
Deferred income tax expense (benefit) = +$5.8 million
Net (gain) loss on sale of property = +$0.2 million
Changes in contract liabilities = -$31.7 million
Changes in deferred costs = +$39.3 million
Other (adjustments) = +$9.3 million
Contributions to pension plans and other post-retirement benefits = -$21.5 million.
2. ## List Projected 2025 Changes in Operating Assets and Liabilities.
Based on Assumption 3, the cash flow impacts for "Changes in operating assets and liabilities" for 2025 are:
"(Increase) decrease in accounts receivable" = -$70.0 million (cash outflow).
"(Increase) decrease in other assets" = +$25.0 million (cash inflow).
"Increase (decrease) in liabilities" = -$100.0 million (cash outflow).
3. ## Calculate Projected 2025 Net Cash Provided by Operating Activities.
I will sum the Projected Net Income (Step 2), all constant adjustment items (Step 2), and the projected changes in operating assets and liabilities (Step 3) to arrive at the "Net cash provided by operating activities" for 2025.
Projected Net cash provided by operating activities =
  $380.0 (Projected Net Income)
+ $122.1 (Depreciation)
- $40.0 (Accretion of discount)
+ $27.7 (Share-based compensation)
+ $11.0 (Equity in losses of ARO)
+ $5.8 (Deferred income tax)
+ $0.2 (Net loss on sale of property)
- $31.7 (Changes in contract liabilities)
+ $39.3 (Changes in deferred costs)
+ $9.3 (Other adjustments)
- $21.5 (Contributions to pension plans)
- $70.0 ((Increase) decrease in accounts receivable)
+ $25.0 ((Increase) decrease in other assets)
- $100.0 (Increase (decrease) in liabilities)
= $357.2 million.
Let me sum the adjustments separately first for clarity:
Sum of constant adjustments from Step 2:
$122.1 - 40.0 + 27.7 + 11.0 + 5.8 + 0.2 - 31.7 + 39.3 + 9.3 - 21.5 = 122.2 million.
Sum of projected changes in operating assets/liabilities from Step 3:
-$70.0 + $25.0 - $100.0 = -$145.0 million.
Projected Net Cash Provided by Operating Activities = Projected Net Income + Sum of Adjustments + Sum of Changes in Op. Assets/Liabilities
= $380.0 million + $122.2 million + (-$145.0 million)
= $357.2 million

### AFTER solution
0. ## The 2024 cash flow page.
Page 43 has the 2024 year-end cash flow statement. Values in millions. Ten items carry forward unchanged into the 2025 forecast.
1. ## Those ten items and their values.
Depreciation 122.1. ARO accretion (40.0). Stock compensation 27.7. ARO equity in losses 11.0. Deferred tax 5.8. Property sale gain/loss 0.2. Contract liabilities change (31.7). Deferred costs change 39.3. Other 9.3. Pension plan contributions (21.5). Their total is 122.2.
2. ## 2025 specific numbers.
Net income: 380.0. Accounts receivable: (70.0). Other assets: 25.0. Liabilities: (100.0). The three working capital items net to negative 145.0 million.
3. ## Grand total.
380.0 + 122.2 + (145.0) = 357.2. Projected net cash provided by operating activities is $357.2 million.

---

## 5. NVDA_2024 (rec207/ann0) — AI-humanized
**Question:** What is the percent change in Nvidia's holdings of marketable securities between 01/28/24 and 01/26/25. Round to two decimal places and return a percentage as an answer, e.g.: 69.00%.
**Answer:** before `85.10%` / after `85.10%` (unchanged)
**GPTZero (solution):** before ai/ai=1  →  after human/ai=0.156

### BEFORE solution
0. ## Locate the "Liquidity and Capital Resources" table.
Review page 43 of the 10-k document where you will find the "Liquidity and Capital Resources" table which presents 2024 and 2025 company holdings in parallel format.
1. ## Analyze the table's components.
The report displays two values which represent Nvidia's marketable securities holdings during 01/26/25 and 01/28/24. The values appear in millions of US dollars.
2. ## Extract the values needed for calculation.
The marketable securities held by Nvidia reached 34,621 million US dollars in value during 01/26/25. The marketable securities held by Nvidia reached 18,704 million US dollars in value during 01/28/24.
3. ## Perform the calculation and return the answer.
The calculation of Nvidia's marketable securities value change percentage from 01/28/24 to 01/26/25 requires the formula: 
The formula calculates percent change by dividing the difference between 01/26/25 and 01/28/24 values by the 01/28/24 value. The calculation results in .850994 which rounds to 85.10% when using the provided values.

### AFTER solution
0. ## Source of data.
Page 43 of the 10-K has the Liquidity and Capital Resources table. Values are in millions of US dollars.
1. ## Numbers.
At 01/26/25 marketable securities are $34,621 million. At 01/28/24 marketable securities are $18,704 million.
2. ## Change.
34,621 minus 18,704 equals 15,917.
3. ## Percentage.
15,917 divided by 18,704 equals 0.850994. Rounded to two decimal places that is 85.10%.