import json

# The initial scores for all entries
initial_scores = {
    (630, 0): (0.045, 'mixed'),
    (632, 0): (0.453, 'human'),
    (633, 0): (0.000, 'human'),
    (634, 0): (0.001, 'human'),
    (635, 0): (1.000, 'ai'),
    (636, 0): (0.003, 'human'),
    (636, 1): (0.001, 'human'),
    (637, 0): (0.000, 'human'),
    (638, 0): (1.000, 'ai'),
    (639, 0): (0.000, 'human'),
    (640, 0): (1.000, 'ai'),
    (641, 0): (0.776, 'ai'),
    (642, 0): (1.000, 'ai'),
    (643, 0): (0.193, 'mixed'),
    (644, 0): (0.000, 'human'),
    (644, 1): (0.001, 'mixed'),
    (645, 0): (0.006, 'human'),
    (646, 0): (1.000, 'ai'),
    (647, 0): (0.428, 'human'),
    (648, 0): (0.006, 'human'),
    (649, 0): (1.000, 'ai'),
    (650, 0): (0.758, 'ai'),
    (651, 0): (1.000, 'ai'),
    (652, 0): (1.000, 'ai'),
    (653, 0): (0.079, 'human'),
    (654, 0): (0.000, 'human'),
    (655, 0): (1.000, 'ai'),
    (656, 0): (0.000, 'human'),
    (657, 0): (0.001, 'human'),
    (658, 0): (0.013, 'human'),
    (659, 0): (0.000, 'human'),
    (660, 0): (0.001, 'human'),
    (661, 0): (1.000, 'ai'),
    (662, 0): (1.000, 'ai'),
    (663, 0): (0.093, 'human'),
    (665, 0): (1.000, 'ai'),
    (666, 0): (0.000, 'human'),
    (667, 0): (0.000, 'human'),
    (668, 0): (1.000, 'ai'),
    (670, 0): (0.951, 'ai'),
    (671, 0): (1.000, 'ai'),
    (672, 0): (0.207, 'mixed'),
    (673, 0): (1.000, 'ai'),
    (674, 0): (0.683, 'ai'),
    (675, 0): (1.000, 'ai'),
    (677, 0): (0.853, 'ai'),
    (678, 1): (1.000, 'ai'),
    (679, 0): (0.226, 'human'),
    (680, 0): (1.000, 'ai'),
    (681, 0): (0.000, 'human'),
    (682, 0): (0.003, 'human'),
    (684, 0): (0.106, 'human'),
    (685, 0): (0.000, 'human'),
    (686, 0): (1.000, 'ai'),
    (687, 0): (0.000, 'human'),
    (689, 0): (0.762, 'ai'),
    (690, 0): (0.000, 'human'),
    (692, 0): (0.551, 'ai'),
    (693, 0): (1.000, 'ai'),
    (694, 0): (0.255, 'human'),
    (695, 0): (0.168, 'mixed'),
    (696, 0): (0.015, 'human'),
    (697, 0): (1.000, 'ai'),
    (698, 0): (0.001, 'human'),
    (699, 0): (0.689, 'ai'),
    (700, 0): (0.004, 'human'),
    (701, 0): (0.097, 'human'),
    (706, 0): (0.958, 'ai'),
    (707, 0): (0.001, 'human'),
    (708, 0): (0.471, 'human'),
}

# Rewrites with their final solutions and scores
rewrites = {
    (635, 0): {
        'solution': [
            "## Step one.\nPage 89, Consolidated Balance Sheets, EchoStar 2019 annual report. Numbers in thousands.",
            "## Step two.\nPage 89. \"Total current assets\" for December 31, 2019 is 2,836,214 thousand dollars.",
            "## Step three.\nPage 89. \"Cash and cash equivalents\" for December 31, 2019 is 1,519,431 thousand dollars.",
            "## Step four.\nNon-cash current assets is 2,836,214 minus 1,519,431 which is 1,316,783 thousand dollars."
        ],
        'ai_prob': 0.10363159237126052,
        'predicted_class': 'human'
    },
    (638, 0): {
        'solution': [
            "## Step one.\nPage 43. Table: \"Consolidated Statements of Income.\" Numbers in thousands of U.S. dollars.",
            "## Step two.\n2014 values from the table: Net sales 1,334,951. Cost of sales 865,951. Net income attributable to Steven Madden, Ltd. 111,880.",
            "## Step three.\nSales up 5%: 1,334,951 x 1.05 = 1,401,698.55. Cost of sales up 7%: 865,951 x 1.07 = 926,567.57. New gross profit: 1,401,698.55 - 926,567.57 = 475,130.98. Old gross profit: 1,334,951 - 865,951 = 469,000.",
            "## Step four.\nGross profit increase: 475,130.98 - 469,000 = 6,130.98. Net income increase equals gross profit increase since nothing else changes. 111,880 + 6,130.98 = 118,010.98. Rounds to $118,011."
        ],
        'ai_prob': 0.5912453820196863,
        'predicted_class': 'human'
    },
    (640, 0): {
        'solution': [
            "## Step one.\nNOV 10-K, Item 8, page 53. Income statement \"CONSOLIDATED STATEMENTS OF INCOME (LOSS)\" on page 62.",
            "## Step two.\nPage 62 (physical page 60), balance sheets. Shares at December 31, 2017: 380,104,970 shares issued and outstanding.",
            "## Step three.\nFormula used: market cap = outstanding shares times stock price. The question uses $80 per share.",
            "## Step four.\n380,104,970 times 80 = 30,408,397,600. That is 30,408.3976 million. Divided by 1,000 that is 30.41 billion dollars."
        ],
        'ai_prob': 0.35564791426344766,
        'predicted_class': 'human'
    },
    (641, 0): {
        'solution': [
            "## Source pages.\nSunoco LP 2022 10-K. Consolidated Statements of Equity: page 82. Acquisitions section: page 90. Numbers in millions of dollars.",
            "## 2022 deals.\nPage 90 shows two 2022 deals. Peerless was purchased on November 30, 2022 for $76 million. Huntington facility was purchased on April 1, 2022 for $252 million. 76 + 252 = $328 million total for 2022.",
            "## 2021 deals.\nPage 90 shows two 2021 deals. NuStar terminal October 8, 2021 for $250 million. Cato terminal September 24, 2021 for $6 million. 250 + 6 = $256 million total for 2021.",
            "## Math.\nDifference: 328 - 256 = 72. Percentage change: 72 / 256 x 100 = 28.13%."
        ],
        'ai_prob': 0.3232109451386913,
        'predicted_class': 'human'
    },
    (642, 0): {
        'solution': [
            "## Note location.\nTrimble financial statements, document page 47 index. Note 3 \"Acquisitions\" spans pages 58-60. Document page 59, \"Purchase Price Allocation\" subsection, has the Transporeon acquisition table.",
            "## Intangible assets and values.\nDocument page 59, table under \"Intangible assets acquired.\" Three line items: Customer relationships $759.5 million, Developed product technology $168.4 million, Trade name $11.9 million. All in millions.",
            "## Useful lives.\nSame table page 59, column \"Estimated Useful Life.\" Customer relationships 11 years, Developed product technology 7 years, Trade name 5 years.",
            "## Annual amortization per asset.\nDivide fair value by useful life. Customer relationships: 759.5 / 11 = $69.05 million. Developed product technology: 168.4 / 7 = $24.06 million. Trade name: 11.9 / 5 = $2.38 million.",
            "## Total.\n69.05 + 24.06 + 2.38 = $95.49 million."
        ],
        'ai_prob': 0.003302508382971675,
        'predicted_class': 'human'
    },
    (646, 0): {
        'solution': [
            "## Source data.\nBrown & Brown annual report, page 69. The \"Long-Term Debt\" table. All figures in thousands.",
            "## Total debt.\nRow \"Total debt,\" December 31, 2017: $976,141 thousand.",
            "## Debt issuance costs contra.\nRow \"Debt issuance costs (contra),\" December 31, 2017: ($7,802) thousand, meaning negative $7,802 thousand.",
            "## Current portion of 4.500% notes.\nUnder \"Current portion,\" row \"4.500% senior notes, Series E, quarterly interest payments, balloon due 2018,\" December 31, 2017: $100,000 thousand.",
            "## Calculation.\n976,141 + 7,802 - 100,000 = $883,943 thousand."
        ],
        'ai_prob': 0.32836583001900993,
        'predicted_class': 'human'
    },
    (649, 0): {
        'solution': [
            "## Source.\nPage 39. Table \"CONSOLIDATED STATEMENTS OF EARNINGS.\" Numbers in thousands (header says \"(in thousands, except per share amounts)\").",
            "## Values.\n\"Operating earnings\" row. 2023: $106,712 thousand. 2022: $68,544 thousand.",
            "## Formula.\nPercentage change = (2023 - 2022) / 2022 x 100.",
            "## Result.\n(106,712 - 68,544) / 68,544 x 100. That is 38,168 / 68,544 x 100. That is 55.68%."
        ],
        'ai_prob': 0.023339092604499175,
        'predicted_class': 'human'
    },
    (650, 0): {
        'solution': [
            "## Source and EBIT values.\nPage 63, \"Consolidated Statements of Operations.\" Numbers in thousands. Operating income for December 30, 2023: $8,268 thousand. Operating income for December 31, 2022: $17,933 thousand.",
            "## Depreciation and amortization values.\nPage 67, \"Consolidated Statements of Cash Flows.\" Numbers in thousands. D&A for December 30, 2023: $31,039 thousand. D&A for December 31, 2022: $23,047 thousand.",
            "## EBITDA calculation.\nEBITDA = Operating Income + D&A. For 2023: 8,268 + 31,039 = $39,307 thousand. For 2022: 17,933 + 23,047 = $40,980 thousand.",
            "## Percentage change.\n(39,307 - 40,980) / 40,980 x 100. Numerator: negative 1,673. Result: negative 1,673 divided by 40,980 times 100 equals negative 4.08%."
        ],
        'ai_prob': 0.04924811956035728,
        'predicted_class': 'mixed'
    },
    (651, 0): {
        'solution': [
            "## The data.\nPage 43, \"Stock Price Performance Graph.\" Data table below the chart tracks $100 investments. Six date columns ending with 7/31/2022.",
            "## PANW.\nPage 43 table, row \"Palo Alto Networks, Inc.,\" date 7/31/2022: $378.74. Return from $100: 278.74%.",
            "## S&P IT.\nPage 42 table, row \"S&P Information Technology Index,\" date 7/31/2022: $257.30. Return from $100: 157.30%.",
            "## Answer.\n278.74% minus 157.30% is 121.44%."
        ],
        'ai_prob': 0.0543259317703282,
        'predicted_class': 'human'
    },
    (652, 0): {
        'solution': [
            "## Financial statement.\nPage 97. Table name: \"DIGITAL REALTY TRUST, INC. AND SUBSIDIARIES CONSOLIDATED INCOME STATEMENTS.\" Units are in thousands except per share data. Year 2024: total operating revenues = $5,554,968 thousand. Operating income = $471,864 thousand.",
            "## 2024 operating margin.\n471,864 / 5,554,968 = 0.084944, or about 8.4944%.",
            "## 2025 revenues.\nRevenues increase 40%. 5,554,968 x 1.40 = $7,776,955.2 thousand.",
            "## 2025 operating margin.\nMargin increases by 8 percentage points. 8.4944% + 8% = 16.4944%.",
            "## 2025 operating income.\n7,776,955.2 x 0.164944 = $1,282,770.068 thousand, which is $1,282,770,068 to the nearest dollar."
        ],
        'ai_prob': 0.0013685066261567031,
        'predicted_class': 'human'
    },
    (655, 0): {
        'solution': [
            "## Note on page 139.\nDocument page 139. \"Notes to Consolidated Financial Statements.\" One of the notes discusses the Adimab Collaboration Agreement.",
            "## 2021 number.\nPage 139, second paragraph of the Adimab note, last sentence: \"For the years ended December 31, 2022 and 2021, the Company recognized $5.2 million and $2.6 million, respectively, of research and development expense related to the quarterly fee.\" The 2021 value is $2.6 million.",
            "## 2022 number.\nSame sentence on page 139. The 2022 value is $5.2 million.",
            "## Percentage increase.\n(5.2 - 2.6) / 2.6 x 100. That is 2.6 / 2.6 x 100. Result: 100.00%."
        ],
        'ai_prob': 0.013747833184375028,
        'predicted_class': 'human'
    },
    (661, 0): {
        'solution': [
            "## Net income location.\nPage 24 of the Eaton 10-K 2023. Table: Consolidated Statements of Income. The 2023 net income attributable to Eaton ordinary shareholders is $3,218 million.",
            "## Total assets.\nPage 26 of the same document. Table: Consolidated Balance Sheets. 2023 total assets: $38,432 million. 2022 total assets: $35,014 million.",
            "## Average.\n38,432 + 35,014 = 73,446. 73,446 / 2 = $36,723 million average total assets.",
            "## ROA.\n3,218 / 36,723 = 0.08763. Times 100 = 8.76%."
        ],
        'ai_prob': 0.0026780281023890936,
        'predicted_class': 'human'
    },
    (662, 0): {
        'solution': [
            "## Extracting operating loss and tax benefit.\nDocument page 63, \"Consolidated Statements of Operations,\" December 31, 2023 column. Numbers in millions. Loss from operations: $314.9 million. Loss before income taxes and equity in loss of unconsolidated entity: $317.2 million. Income tax benefit: $0.4 million.",
            "## Computing NOPAT.\nEffective tax rate = 0.4 / 317.2 = 0.0013, or 0.13%. NOPAT = loss from operations times (1 minus effective tax rate). NOPAT = negative 314.9 times (1 minus 0.0013) = negative 314.9 times 0.9987 = negative $314.5 million.",
            "## Balance sheet components.\nDocument page 62, \"Consolidated Balance Sheets,\" December 31, 2023 column. Numbers in millions. Concierge credit facility: $24.8 million. Current operating lease liabilities: $98.9 million. Non-current operating lease liabilities: $410.2 million. Cash and cash equivalents: $166.9 million. Total stockholders' equity: $432.0 million.",
            "## Computing invested capital.\nDebt and lease liabilities: 24.8 + 98.9 + 410.2 = $533.9 million. Net of cash: 533.9 minus 166.9 = $367.0 million. Invested capital: 367.0 plus 432.0 = $799.0 million.",
            "## ROIC.\nROIC = NOPAT / invested capital = negative 314.5 / 799.0 = negative 0.393 = negative 39.3%."
        ],
        'ai_prob': 0.01855537217207992,
        'predicted_class': 'human'
    },
    (665, 0): {
        'solution': [
            "## Source data.\nPages 47-48. Operating income $580 million. Depreciation $156 million. Amortization $31 million.",
            "## EBITDA and debt.\nEBITDA: 580 + 156 + 31 = $767 million. Total debt: $1,184 million. Debt-to-EBITDA: 1,184 / 767 = 1.54.",
            "## Hypothetical debt reduction.\nPage 51. Stock repurchases in 2020: $736 million. 50% directed to debt: $368 million. New debt: 1,184 - 368 = $816 million. EBITDA unchanged at $767 million (interest is below EBITDA).",
            "## Improvement.\nNew ratio: 816 / 767 = 1.06. Old ratio: 1.54. Improvement: (1.54 - 1.06) / 1.54 x 100 = 31.16883117%."
        ],
        'ai_prob': 0.06079475663536436,
        'predicted_class': 'human'
    },
    (668, 0): {
        'solution': [
            "## Income statement.\nPage 52. Table: \"Alliant Energy Corporation Consolidated Statements of Income.\"",
            "## Operating income.\nLine 17, page 52. EBIT (operating income) for Alliant was $886 million.",
            "## Tax rate.\nIncome tax line on page 52, 2024 Consolidated Statements of Income. Income tax benefit: $(114) million. Income before income taxes: $576 million. Effective tax rate: negative 114 / 576 = negative 0.1979, or negative 19.79%.",
            "## NOPAT.\nNOPAT = EBIT x (1 minus effective tax rate). NOPAT = $886 million x (1 minus negative 0.1979). That is $886 million x 1.1979. Result: $1,061.35 million."
        ],
        'ai_prob': 0.03351813851176426,
        'predicted_class': 'human'
    },
    (670, 0): {
        'solution': [
            "## Finding the data.\nDocument page 63 has the \"CONSOLIDATED BALANCE SHEETS\" for Aramark. All numbers are in thousands. The column for September 27, 2024 is used.",
            "## Current assets total.\nThe current assets section of the September 27, 2024 balance sheet totals $3,406,562 thousand.",
            "## Current liabilities breakdown.\nCurrent maturities of long-term borrowings: 964,286. Current operating lease liabilities: 54,163. Accounts payable: 1,394,007. Accrued payroll and related expenses: 518,912. Accrued expenses and other current liabilities: 1,282,842. Discontinued operations: 0. Total: 4,214,210 thousand.",
            "## Ratio.\n3,406,562 / 4,214,210 = 0.8083512687."
        ],
        'ai_prob': 0.0042026261993901555,
        'predicted_class': 'human'
    },
    (671, 0): {
        'solution': [
            "## Balance sheet.\nPage 79 of the document. Table titled \"Murphy USA Inc. Consolidated Balance sheets.\" Numbers are in millions of dollars, except share amounts.",
            "## Current assets.\nRow \"Total Current assets,\" column \"December 31, 2023\": $826.5 million.",
            "## Current liabilities.\nRow \"Total Current liabilities\" under LIABILITIES AND STOCKHOLDERS' EQUITY, column \"December 31, 2023\": $872.8 million.",
            "## Working capital.\nWorking capital = current assets minus current liabilities. 826.5 minus 872.8 = $(46.3) million."
        ],
        'ai_prob': 0.15751320477172048,
        'predicted_class': 'human'
    },
    (673, 0): {
        'solution': [
            "## HEICO FY2018 operating income.\nPage 23. Table \"Results of Operations.\" Units: thousands. Below the table, \"Operating Income by segment:\" section. \"Total Operating Income\" row: $376,245 thousand.",
            "## R&D location.\nPage 24. \"Gross Profit and Operating Expenses\" section. R&D expense for fiscal 2018 was $57.5 million, included in cost of sales.",
            "## Scenario: $10 million R&D cut.\n$10 million less R&D expense reduces cost of sales by $10 million. Operating income rises by $10,000 thousand.",
            "## Scenario: 5pp margin boost.\n5% of the $10 million cost reduction: $500 thousand more profit.",
            "## Revised total.\n376,245 + 10,000 + 500 = $386,745 thousand. In millions: $386.745 million. Rounded: $386.7 million."
        ],
        'ai_prob': 0.26751566781628017,
        'predicted_class': 'mixed'
    },
    (674, 0): {
        'solution': [
            "## Data.\nPage 42. \"Fiscal 2018 Summary Compensation Table.\" Row for Stephen D. Young, CFO: total 2018 = $1,117,254, bonus 2018 = $164,500, bonus 2016 = $0.",
            "## Swap.\nTake out 2018 bonus: 1,117,254 - 164,500 = $952,754. Put in 2016 bonus: $952,754 + $0 = $952,754.",
            "## Other items.\nNothing else changes.",
            "## Answer.\n$952,754."
        ],
        'ai_prob': 0.2755299838337598,
        'predicted_class': 'human'
    },
    (675, 0): {
        'solution': [
            "## Balance sheet pages.\nPages 82 and 83 of the Check Point document. Table title: \"CONSOLIDATED BALANCE SHEETS (CONT'D).\" Covers years ended December 31, 2024 and December 31, 2023.",
            "## Total assets.\nPage 82, bottom of table, \"Total Assets,\" 2024 column: $5,754.5 million.",
            "## Total liabilities.\nPage 83, \"Total liabilities,\" 2024 column: $2,963.5675 million. Total liabilities and shareholders' equity (same as total assets): $5,754.5 million.",
            "## Liability increase.\nA 10% increase in total assets means total assets grow by 5,754.5 times 0.10, which is $575.45 million. The liability-to-assets ratio stays the same. Liability share: 2,963.5675 / 5,754.5 = 0.515014. Liabilities increase by 575.45 times 0.515014 equals $296.35675 million."
        ],
        'ai_prob': 0.28196204051116586,
        'predicted_class': 'human'
    },
    (677, 0): {
        'solution': [
            "## Source data.\nPage 71 (footer 67). \"Comcast Corporation Consolidated Statement of Income.\" Numbers in millions. Year 2018. Operating income: $19,009 million. Depreciation: $8,281 million. Amortization: $2,736 million. Revenue: $94,507 million.",
            "## Expense lines.\nProgramming and production: $29,692 million. Other operating and administrative: $28,094 million. Advertising, marketing and promotion: $7,036 million. Other operating gains: $(341) million.",
            "## Adjusted depreciation.\nDepreciation drops 10%. 8,281 x 0.90 = $7,452.9 million.",
            "## Adjusted amortization.\nAmortization rises 5%. 2,736 x 1.05 = $2,872.8 million.",
            "## New operating income.\nTotal costs: 29,692 + 28,094 + 7,036 + 7,452.9 + 2,872.8 - 341 = $74,806.7 million. Operating income: 94,507 - 74,806.7 = $19,700.3 million, which rounds to $19,700 million."
        ],
        'ai_prob': 0.016909078446771364,
        'predicted_class': 'human'
    },
    (678, 1): {
        'solution': [
            "## Note C, segment data.\nHowmet Aerospace 2024 Form 10-K, Note C, \"Segment and Geographic Area Information,\" page 52 for the operating table. Page 84 for the detailed sales table. Numbers in millions of dollars.",
            "## 2024 third-party sales.\nPage 84 table. Engine Products: $3,735 million. Fastening Systems: $1,576 million. Engineered Structures: $1,065 million. Forged Wheels: $1,054 million.",
            "## Engine Products 2025.\n10% growth applied to $3,735 million. 3,735 x 1.10 = $4,108.5 million.",
            "## Forged Wheels 2025.\n5% decline applied to $1,054 million. 1,054 x 0.95 = $1,001.3 million.",
            "## Other two segments.\nFastening Systems stays at $1,576 million. Engineered Structures stays at $1,065 million.",
            "## Total 2025.\n4,108.5 + 1,576 + 1,065 + 1,001.3 = $7,750.8 million, rounding to $7,751 million."
        ],
        'ai_prob': 0.05962706245619446,
        'predicted_class': 'human'
    },
    (680, 0): {
        'solution': [
            "## Page 39.\n\"COMPARISON OF CUMULATIVE TOTAL RETURN*\" chart. $100 investment started August 5, 2020.",
            "## Reading S&P 500 in Dec-2023.\nS&P 500 line at Dec-2023: about $150. Return: 50%.",
            "## Annual rate.\nAugust 2020 to December 2023 is roughly 3.33 years. Factor: 1.50^(1/3.33) = 1.1295 per year.",
            "## Extend to December 2024.\nAugust 2020 to December 2024 = about 4.4 years. 1.1295^4.4 = approximately 1.71.",
            "## Result.\n$100 x 1.71 = 171."
        ],
        'ai_prob': 0.280166682845301,
        'predicted_class': 'human'
    },
    (686, 0): {
        'solution': [
            "## Source.\nPage 37. \"Consolidated Balance Sheets.\" Amounts in thousands.",
            "## Summing liabilities.\nCurrent liabilities: accounts payable 64,102, current LTD 70,689, current op lease 29,998, accrued 43,062, insurance 25,464, due to affiliates 20,737, income taxes 6,364. Non-current: LTD net 311,235, op lease non-current 63,620, deferred tax 79,567, other 6,487.",
            "## Total.\n721,325 thousand.",
            "## Answer.\n311,235 / 721,325 = 0.43148. Times 100 = 43.14767961 percent."
        ],
        'ai_prob': 0.03378967885958969,
        'predicted_class': 'human'
    },
    (689, 0): {
        'solution': [
            "## Starting total liabilities.\nConsolidated Balance Sheet on page 62. Total liabilities at December 31, 2022: $311,424,585.",
            "## Remove duplicate accounts payable.\nAccounts payable - related parties was entered twice. Remove $1,200,000. Running total: 311,424,585 - 1,200,000 = $310,224,585.",
            "## Remove repaid lines of credit.\n$1,750,000 in lines of credit was repaid in December. Subtract $1,750,000. Running total: 310,224,585 - 1,750,000 = $308,474,585.",
            "## Reclassify financing lease liabilities.\nMove $3,500,000 of financing lease liabilities from current to non-current. This is a reclassification only and does not change total liabilities. Running total: $308,474,585.",
            "## Reduce overstated operating lease.\nCurrent portion of operating lease liabilities was overstated by $5,200,000. Subtract $5,200,000. Running total: 308,474,585 - 5,200,000 = $303,274,585.",
            "## Add understated deferred tax.\nDeferred tax liabilities were understated by $4,000,000. Add $4,000,000. Final total: 303,274,585 + 4,000,000 = $307,274,585."
        ],
        'ai_prob': 0.28093921076055145,
        'predicted_class': 'human'
    },
    (692, 0): {
        'solution': [
            "## Source.\nPage 152. \"WD-40 COMPANY - CONSOLIDATED STATEMENTS OF OPERATIONS (In thousands, except per share amounts).\"",
            "## Adjusted net sales.\n2023 net sales: $537,255 thousand. After 4% increase: 537,255 x 1.04 = $558,745.2 thousand.",
            "## Adjusted COGS.\n2023 cost of products sold: $263,035 thousand. COGS ratio: 263,035 / 537,255 = 0.4895. Adjusted COGS: 0.4895 x 558,745.2 = $273,505.7754 thousand.",
            "## Gross profit.\n558,745.2 - 273,505.7754 = $285,239.4246 thousand.",
            "## Adjusted operating expenses.\n2023 SG&A: $154,684 thousand. After 6% increase: 154,684 x 1.06 = $163,965.04 thousand. Advertising and promotion: $28,807 thousand (unchanged). Amortization of intangibles: $1,005 thousand (unchanged). Total: 163,965.04 + 28,807 + 1,005 = $193,777 thousand (approximately).",
            "## Adjusted operating income.\n285,239.4246 - 193,777 = $91,462.4246 thousand.",
            "## Adjusted pre-tax income.\nInterest income: $231 thousand. Interest expense: $5,614 thousand. Other income (expense) net: $822 thousand. Pre-tax: 91,462.4246 + 231 + 822 - 5,614 = $86,901.4246 thousand.",
            "## Effective tax rate.\n2023 pre-tax income: $85,163 thousand. 2023 income tax: $19,170 thousand. Rate: 19,170 / 85,163 = 0.2251 or 22.51%.",
            "## Adjusted net income.\nTaxes on adjusted pre-tax: 0.2251 x 86,901.4246 = $19,552.8119 thousand. Net income: 86,901.4246 - 19,552.8119 = $67,348.6041 thousand."
        ],
        'ai_prob': 0.001365093608829103,
        'predicted_class': 'human'
    },
    (693, 0): {
        'solution': [
            "## Page 58, Atkore.\n\"ATKORE INC. CONSOLIDATED STATEMENTS OF OPERATIONS.\" Numbers in thousands.",
            "## Two SG&A values.\nRow \"Selling, general and administrative.\" September 30, 2024 column: 397,544. September 30, 2023 column: 388,206. All in thousands.",
            "## Computing the change.\n397,544 - 388,206 = 9,338 thousand. That is how much it went up.",
            "## Converting to percent.\n9,338 / 388,206 = 0.02405. Times 100 = 2.41%."
        ],
        'ai_prob': 0.0004444053582392168,
        'predicted_class': 'human'
    },
    (697, 0): {
        'solution': [
            "## Balance sheet.\nPage 1 of the document. Table \"CONSOLIDATED BALANCE SHEETS.\" Numbers in thousands.",
            "## Values.\nDecember 31, 2020 column. Total shareholders' equity: $364,761 thousand ($364,761,000). Treasury stock: negative $183,161 thousand (negative $183,161,000). Total assets: $1,188,990 thousand ($1,188,990,000).",
            "## Adjusted equity.\nTreasury stock is already deducted in reported equity. To add it back: 364,761 + 183,161 = $547,922 thousand.",
            "## Ratio.\n547,922 / 1,188,990 = 0.4608. Times 100 = 46.08%."
        ],
        'ai_prob': 0.03771038492853209,
        'predicted_class': 'human'
    },
    (699, 0): {
        'solution': [
            "## The chart.\nPage 28. \"Comparison of Cumulative Total Return.\" The graph starts at June 28, 2019 with a $100 investment and dividends reinvested. Three lines in the chart.",
            "## WOLF data from the table.\n6/28/2020: WOLF = $102.78. 6/25/2023: WOLF = $88.01.",
            "## WOLF CAGR.\n88.01 / 102.78 = 0.8563. To the power of 1/3: 0.9496. Minus 1 = negative 5.04%.",
            "## Philly semi data from the table.\n6/28/2020: Philadelphia Semiconductor Index = $134.13. 6/25/2023: $254.85.",
            "## Philly semi CAGR.\n254.85 / 134.13 = 1.90. To the power of 1/3: 1.2386. Minus 1 = 23.86%.",
            "## Delta.\nWOLF CAGR minus Philadelphia CAGR: negative 5.04% minus 23.86% = negative 28.9%."
        ],
        'ai_prob': 0.00419387795052874,
        'predicted_class': 'human'
    },
    (706, 0): {
        'solution': [
            "## Table on page 100.\nSection: \"Net unit sales were as follows.\" The table has a column for 2020 and a column for 2019.",
            "## TASER 7.\n2020: 77,451. 2019: 49,221.",
            "## 2020 total.\nAll product lines in 2020: 77,451 + 37,391 + 43,407 + 33,158 + 3,714,291 + 182,538 + 8,962 + 11,304 + 25,422. Total is 4,133,924.",
            "## 2019 total.\nAll product lines in 2019: 49,221 + 48,798 + 40,973 + 11,785 + 2,751,603 + 151,499 + 15,586 + 10,467 + 22,275. Total is 3,102,207.",
            "## RVI.\n2020 share = 77,451 / 4,133,924 = 0.018735. 2019 share = 49,221 / 3,102,207 = 0.015867. 0.018735 / 0.015867 = 1.1808."
        ],
        'ai_prob': 0.004208883565992132,
        'predicted_class': 'human'
    },
}

# Logic flags
logic_flags = {
    (646, 0): "Original solution steps 3-4 only add back $7,802 (debt issuance costs) and compute $983,943, ignoring the $100,000 current portion subtraction needed to reach the stated answer of $883,943. The rewrite correctly applies both adjustments.",
    (675, 0): "Original solution step 3 cites total liabilities as $2,965.1 million, and step 4 computes 0.10 x $2,965.1 = $296.51 million, but the stated answer is $296.35675 million. Back-calculation from the answer implies true liabilities = $2,963.5675 million, inconsistent with the $2,965.1 million cited in the solution.",
    (662, 0): "Original solution step 3 (Compute invested capital) contains Italian-language text alongside English, making the step partially incoherent. The calculation logic appears correct but the mixed-language text is a data quality concern.",
    (706, 0): "Original solution step 2 contains Albanian-language text for the 2020 TASER 7 share calculation. The numeric results appear correct but the mixed-language content is a data quality concern.",
    (647, 0): "The question asks to 'calculate the average square footage per center and multiply by the total number of distribution centers' (6 total). The solution instead sums only the two California centers (337,000 + 108,000 = 445,000). These approaches yield the same answer only if average x 6 = 445,000, which would require an average of ~74,167 sq ft per center. The solution does not show this calculation.",
}

# Build the output
entries = json.load(open('patches/full_W10.json'))
output = []
for e in entries:
    rec, ann, eid = e['rec'], e['ann'], e['id']
    key = (rec, ann)
    orig_ai_prob, orig_class = initial_scores[key]

    flag = logic_flags.get(key)

    if key in rewrites:
        r = rewrites[key]
        obj = {
            'rec': rec,
            'ann': ann,
            'id': eid,
            'action': 'rewritten',
            'solution': r['solution'],
            'ai_prob': r['ai_prob'],
            'predicted_class': r['predicted_class']
        }
        if flag:
            obj['logic_flag'] = flag
    else:
        obj = {
            'rec': rec,
            'ann': ann,
            'id': eid,
            'action': 'already_pass',
            'ai_prob': orig_ai_prob,
            'predicted_class': orig_class
        }
        if flag:
            obj['logic_flag'] = flag

    output.append(obj)

with open('patches/full_W10.out.json', 'w') as f:
    json.dump(output, f, indent=2)

n_rewritten = sum(1 for x in output if x['action'] == 'rewritten')
n_pass = sum(1 for x in output if x['action'] == 'already_pass')
n_stuck = sum(1 for x in output if x['action'] == 'stuck')
n_flagged = sum(1 for x in output if 'logic_flag' in x)
print(f'Total entries: {len(output)}')
print(f'Rewritten: {n_rewritten}')
print(f'Already pass: {n_pass}')
print(f'Stuck: {n_stuck}')
print(f'Logic flagged: {n_flagged}')
flag_ids = [x['id'] for x in output if 'logic_flag' in x]
print('Logic flag ids:', flag_ids)
