"""Static educational content for the Learning Module.

Each article contains an explanation, real-world examples, practical tips,
and common mistakes to avoid — used to render the learning pages.
"""

LEARNING_ARTICLES = {
    "savings": {
        "title": "Savings: Building Your Financial Foundation",
        "category": "Fundamentals",
        "icon": "bi-piggy-bank",
        "summary": "Learn why saving early and consistently is the foundation of financial security.",
        "explanation": [
            "Saving is the practice of setting aside a portion of your income instead of spending it immediately, so it is available for future needs, goals, or emergencies.",
            "The most important savings habit is building an emergency fund — typically 3 to 6 months of essential living expenses — kept in a liquid, easily accessible account. This protects you from having to take on debt when unexpected expenses like medical bills or job loss occur.",
            "Beyond emergencies, savings help you fund short-term goals (a vacation, a gadget) and act as the seed capital that eventually gets invested for long-term goals like buying a home or retirement.",
        ],
        "examples": [
            "Priya earns ₹30,000/month and automatically transfers ₹3,000 (10%) to a separate savings account the day she is paid — this is the 'pay yourself first' principle.",
            "Rahul lost his job for two months but survived comfortably because he had built a 6-month emergency fund of ₹1,80,000 in a savings account.",
            "A Recurring Deposit (RD) of ₹2,000/month for 12 months helps build disciplined saving habits with predictable returns.",
        ],
        "tips": [
            "Automate your savings — set up an auto-debit so saving doesn't depend on willpower.",
            "Keep your emergency fund separate from your everyday spending account.",
            "Start small — even ₹500/month builds a habit that compounds over time.",
            "Review and increase your savings rate whenever your income increases.",
        ],
        "mistakes": [
            "Treating savings as 'whatever is left over' at the end of the month instead of a fixed priority.",
            "Keeping emergency funds in illiquid investments that can't be accessed quickly.",
            "Not having any separation between savings and spending money, leading to accidental spending.",
        ],
    },
    "digital-banking": {
        "title": "Digital Banking: Banking in the Modern Age",
        "category": "Digital Finance",
        "icon": "bi-bank",
        "summary": "Understand net banking, mobile banking, and how to use digital banking tools safely.",
        "explanation": [
            "Digital banking allows you to perform banking activities — checking balances, transferring funds, paying bills, applying for loans — through websites and mobile apps instead of visiting a physical branch.",
            "Core digital banking channels include Net Banking (web-based), Mobile Banking apps, ATMs/Cash Recyclers, and increasingly, WhatsApp or chatbot banking.",
            "Digital banking has made financial services more accessible and convenient, but it also introduces new risks such as phishing, fake apps, and account takeover if not used carefully.",
        ],
        "examples": [
            "Using your bank's official mobile app to transfer money via IMPS in seconds instead of visiting a branch.",
            "Setting up e-mandates for automatic bill payments (electricity, insurance premiums) through net banking.",
            "Using a virtual/one-time card number for online purchases to protect your primary debit card.",
        ],
        "tips": [
            "Only download banking apps from official app stores and verify the publisher name.",
            "Enable biometric or strong PIN locks on your banking apps.",
            "Log out of net banking sessions on shared or public computers.",
            "Regularly check your account statements for unfamiliar transactions.",
        ],
        "mistakes": [
            "Using public Wi-Fi to log into net banking or make payments.",
            "Saving banking passwords in browsers on shared devices.",
            "Clicking banking links sent via SMS or email instead of typing the official URL directly.",
        ],
    },
    "upi-safety": {
        "title": "UPI Safety: Pay Digitally Without Getting Scammed",
        "category": "Digital Finance",
        "icon": "bi-phone",
        "summary": "Master the fundamentals of UPI and the safety practices that prevent the most common scams.",
        "explanation": [
            "UPI (Unified Payments Interface) enables instant, real-time money transfer between bank accounts using a mobile app, without needing account or IBAN numbers.",
            "A critical concept many people misunderstand: to RECEIVE money, you never need to enter your UPI PIN. The PIN is required only when you are SENDING or authorizing a payment.",
            "Most UPI frauds exploit this confusion — a scammer sends a 'collect request' disguised as a refund or cashback, and the victim enters their PIN, unknowingly authorizing a payment OUT of their account.",
        ],
        "examples": [
            "A fraudster posing as an online marketplace seller sends a payment 'collect request' for ₹1 claiming it's for verification — approving it can deduct real money.",
            "QR code scams: a fraudster asks you to scan a QR code to 'receive' money — scanning and entering PIN actually sends money away.",
            "A genuine example of safe use: scanning a shop's QR code and entering your PIN to pay for groceries.",
        ],
        "tips": [
            "Remember: Scan + Enter PIN = Pay. You never need a PIN to receive money.",
            "Always double check the payee name and amount shown before entering your UPI PIN.",
            "Set a reasonable per-transaction UPI limit in your banking app.",
            "Use the 'report and block' feature in UPI apps for suspicious requests.",
        ],
        "mistakes": [
            "Approving unknown collect requests without reading the payee details.",
            "Sharing your UPI PIN with anyone, including someone claiming to be a bank employee.",
            "Scanning random QR codes shared by strangers to 'receive' payments.",
        ],
    },
    "cyber-security": {
        "title": "Cyber Security: Protecting Yourself from Digital Fraud",
        "category": "Safety & Security",
        "icon": "bi-shield-lock",
        "summary": "Learn to recognize phishing, vishing, and social engineering attacks targeting your finances.",
        "explanation": [
            "Cyber fraud refers to criminal activity conducted through digital channels — emails, calls, SMS, apps, or websites — aimed at stealing money or personal/financial information.",
            "Common attack types include Phishing (fake emails/websites), Vishing (voice call scams), Smishing (SMS scams), and social engineering, where attackers manipulate victims psychologically rather than exploiting technical bugs.",
            "Banks, RBI, and financial institutions never ask for your PIN, password, CVV, or OTP over phone calls, SMS, or email. Any such request is a guaranteed sign of fraud.",
        ],
        "examples": [
            "A caller claiming to be from 'bank customer support' asks you to install a remote screen-sharing app to 'resolve an issue' — this lets them see your banking app and steal credentials.",
            "An SMS saying 'Your KYC will expire, click here to update' links to a fake bank website that captures your login details.",
            "A fake job offer requiring an upfront 'registration fee' before you can start working.",
        ],
        "tips": [
            "Never share OTP, PIN, CVV, or passwords with anyone — not even bank staff.",
            "Verify suspicious calls by hanging up and calling the bank's official number yourself.",
            "Enable transaction alerts via SMS/email so you notice unauthorized activity immediately.",
            "If defrauded, report immediately at cybercrime.gov.in or call the national helpline 1930.",
        ],
        "mistakes": [
            "Installing remote access/screen-sharing apps at the request of unknown callers.",
            "Trusting caller ID alone, since numbers can be spoofed.",
            "Delaying reporting a fraud — the first few hours are critical for fund recovery.",
        ],
    },
    "mutual-funds": {
        "title": "Mutual Funds: Investing Made Accessible",
        "category": "Investing",
        "icon": "bi-pie-chart",
        "summary": "Understand how mutual funds work, key terms, and how to start investing through SIPs.",
        "explanation": [
            "A mutual fund pools money from many investors and invests it in a diversified portfolio of stocks, bonds, or other securities, managed by a professional fund manager.",
            "Key terms: NAV (Net Asset Value) is the per-unit price of the fund; Expense Ratio is the annual fee charged for management; SIP (Systematic Investment Plan) lets you invest a fixed amount regularly instead of a lump sum.",
            "Mutual funds are broadly categorized into Equity funds (higher risk/return, invest in stocks), Debt funds (lower risk, invest in bonds), and Hybrid funds (a mix of both).",
        ],
        "examples": [
            "Starting a SIP of ₹1,000/month in an equity mutual fund to build long-term wealth for a goal 10+ years away.",
            "Choosing a debt mutual fund for a 2-year goal like a wedding, where capital protection matters more than high growth.",
            "Comparing two funds' expense ratios (1% vs 2%) to understand how fees eat into long-term returns.",
        ],
        "tips": [
            "Start with SIPs to build discipline and benefit from rupee-cost averaging.",
            "Match the fund type to your investment horizon and risk tolerance.",
            "Check that the fund is registered with SEBI and managed by a recognized AMC.",
            "Review your portfolio periodically, but avoid reacting to short-term market noise.",
        ],
        "mistakes": [
            "Investing in equity funds for short-term goals (under 3 years) where volatility can cause losses.",
            "Stopping SIPs during a market downturn instead of continuing to average out costs.",
            "Chasing funds purely based on last year's top returns without checking consistency.",
        ],
    },
    "inflation": {
        "title": "Inflation: Why Your Money Loses Value Over Time",
        "category": "Fundamentals",
        "icon": "bi-graph-down-arrow",
        "summary": "Understand what inflation is and how to protect your savings from losing purchasing power.",
        "explanation": [
            "Inflation is the general, sustained rise in prices of goods and services over time, which reduces the purchasing power of money — the same ₹100 buys less in the future than it does today.",
            "In India, inflation is commonly measured using the Consumer Price Index (CPI) and Wholesale Price Index (WPI), tracked and managed by the RBI and government agencies.",
            "'Real return' is your investment return after subtracting inflation. If a savings account gives 3% interest but inflation is 6%, your real return is actually -3% — you are losing purchasing power.",
        ],
        "examples": [
            "A movie ticket that cost ₹50 a decade ago might cost ₹200 today — that's the visible effect of inflation.",
            "₹10,00,000 kept purely as idle cash for 20 years at 6% average inflation would have significantly less real purchasing power than the same amount invested to outpace inflation.",
            "Fixed deposits at 6% interest during a period of 7% inflation result in a negative real return.",
        ],
        "tips": [
            "Don't just save — invest a portion of your money in assets that historically outpace inflation over the long run, like equities.",
            "Account for inflation when setting long-term goals (retirement, children's education) — the target amount needed will be much higher in the future.",
            "Review fixed-income investments periodically to ensure they still make sense versus current inflation rates.",
        ],
        "mistakes": [
            "Assuming that a 'safe' fixed deposit is always a good long-term choice without checking real (inflation-adjusted) returns.",
            "Underestimating future costs for long-term goals by ignoring inflation in planning.",
            "Keeping large amounts of money as idle cash for many years.",
        ],
    },
    "insurance": {
        "title": "Insurance: Protecting What Matters",
        "category": "Risk Management",
        "icon": "bi-umbrella",
        "summary": "Learn the basics of life and health insurance and how to choose the right cover.",
        "explanation": [
            "Insurance is a financial product that transfers the risk of an uncertain, costly event (death, illness, accident, property damage) from an individual to an insurance company, in exchange for a periodic payment called a premium.",
            "Term life insurance provides a large payout to your family if you pass away during the policy term, at a relatively low premium — it is pure protection, not an investment.",
            "Health insurance covers hospitalization and medical treatment costs, protecting your savings from being wiped out by a medical emergency.",
        ],
        "examples": [
            "A 30-year-old buying a ₹1 crore term insurance policy for an annual premium of a few thousand rupees, ensuring family financial security in case of an untimely death.",
            "A family floater health insurance policy covering hospitalization expenses for the policyholder, spouse, and children under one sum insured.",
            "Filing a claim after a hospitalization, where the insurer settles the eligible medical bills as per the policy terms.",
        ],
        "tips": [
            "Buy term insurance early — premiums are lower when you are younger and healthier.",
            "Always disclose accurate health and lifestyle information — non-disclosure can lead to claim rejection.",
            "Choose adequate health cover considering rising medical inflation, not just the cheapest premium.",
            "Read policy exclusions carefully before purchasing.",
        ],
        "mistakes": [
            "Confusing investment-linked insurance plans with pure protection (term) plans.",
            "Being underinsured — buying a cover amount too small to actually protect the family's needs.",
            "Hiding pre-existing conditions to get a lower premium, risking claim denial later.",
        ],
    },
    "tax-basics": {
        "title": "Tax Basics: Understanding Your Obligations",
        "category": "Fundamentals",
        "icon": "bi-receipt",
        "summary": "Get familiar with income tax, deductions, and why filing returns matters.",
        "explanation": [
            "Income tax is a direct tax levied by the government on the income earned by individuals and businesses, used to fund public services and infrastructure.",
            "Tax deductions (like under Section 80C in India) allow you to reduce your taxable income by investing in specified instruments such as PPF, ELSS mutual funds, or life insurance premiums.",
            "Filing an Income Tax Return (ITR) is a legal requirement once your income crosses the basic exemption limit, and it also serves as proof of income for loans, visas, and other financial needs.",
        ],
        "examples": [
            "Investing ₹1,50,000 in eligible instruments under Section 80C to reduce taxable income by the same amount.",
            "TDS (Tax Deducted at Source) being automatically deducted from a salary each month by the employer and deposited with the government.",
            "GST being an indirect tax added to the price of goods and services you purchase, distinct from income tax.",
        ],
        "tips": [
            "Plan tax-saving investments early in the financial year instead of rushing in the last quarter.",
            "Keep records of income, investments, and deductions organized for easy filing.",
            "File your ITR even if not strictly mandatory — it helps build a financial history.",
            "Understand the difference between the old and new tax regimes before choosing one.",
        ],
        "mistakes": [
            "Making tax-saving investments purely for tax benefit without considering if the product fits your goals.",
            "Missing the ITR filing deadline, resulting in penalties.",
            "Not keeping proof of deductions claimed, which can cause issues during assessment.",
        ],
    },
    "budgeting": {
        "title": "Budgeting: Take Control of Your Money",
        "category": "Fundamentals",
        "icon": "bi-wallet2",
        "summary": "Learn practical budgeting frameworks to manage income, control spending, and reach goals.",
        "explanation": [
            "A budget is a plan that helps you track income and expenses over a period, ensuring you spend intentionally and save consistently rather than running out of money before the month ends.",
            "A popular framework is the 50-30-20 rule: 50% of income for needs (rent, groceries, bills), 30% for wants (entertainment, dining out), and 20% for savings and debt repayment.",
            "Budgeting isn't about restriction — it's about giving every rupee a purpose so your spending aligns with your priorities and goals.",
        ],
        "examples": [
            "An individual earning ₹40,000/month allocating ₹20,000 to needs, ₹12,000 to wants, and ₹8,000 to savings following the 50-30-20 rule.",
            "Using a simple expense-tracking app or spreadsheet to log daily spending for a month to identify unnecessary expenses.",
            "Creating a 'sinking fund' — saving a small amount monthly for a predictable annual expense like insurance premiums or festival shopping.",
        ],
        "tips": [
            "Track your expenses for at least one month before creating your first budget — you can't manage what you don't measure.",
            "Automate fixed expenses and savings transfers so they happen without relying on memory.",
            "Review and adjust your budget monthly as circumstances change.",
            "Build small rewards into your budget so it feels sustainable, not restrictive.",
        ],
        "mistakes": [
            "Creating an unrealistic budget that leaves no room for any discretionary spending, causing it to fail quickly.",
            "Not accounting for irregular expenses (annual insurance, festivals, gifts) leading to budget breakdowns.",
            "Giving up on budgeting entirely after one bad month instead of adjusting and continuing.",
        ],
    },
}


LEARNING_CATEGORY_ORDER = [
    "savings",
    "digital-banking",
    "upi-safety",
    "cyber-security",
    "mutual-funds",
    "inflation",
    "insurance",
    "tax-basics",
    "budgeting",
]
