# 📊 Retail Sales Data Analytics


An end-to-end retail sales analytics project built with **Python, Pandas, Matplotlib, and Streamlit**. This project demonstrates data cleaning, data quality validation, exploratory data analysis, visualization, and interactive dashboard development using a synthetic retail sales dataset.


## 🚀 Project Overview

The project transforms a deliberately messy retail sales dataset into structured, validated data and presents the results through an interactive dashboard.

### Key Features

- **Data generation:** Created a synthetic dataset containing 1,000,000 retail sales records.
- **Data auditing:** Identified missing values, duplicate records, invalid values, and inconsistent text.
- **Data cleaning:** Standardized data and handled missing and invalid records.
- **Data validation:** Checked data quality, transaction IDs, and revenue calculations.
- **Exploratory data analysis:** Analyzed sales by product, region, payment method, and month.
- **Data visualization:** Generated charts to highlight sales patterns and performance.
- **Interactive dashboard:** Built a Streamlit dashboard with date ranges, filters, key performance indicators (KPIs), charts, and CSV downloads.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Streamlit
- Git and GitHub

## 📁 Project Structure

```text
RetailDataCleaning/
├── app.py
├── data/
│   └── raw/
│       └── retail_sales_sample.csv
├── reports/
│   ├── charts/
│   ├── cleaning_report.txt
│   ├── missing_values_report.csv
│   ├── monthly_sales.csv
│   ├── sales_by_payment_method.csv
│   ├── sales_by_product.csv
│   └── sales_by_region.csv
├── src/
│   ├── generate_dataset.py
│   ├── inspect_dataset.py
│   ├── audit_dataset.py
│   ├── clean_dataset.py
│   ├── validate_dataset.py
│   ├── analyze_sales.py
│   └── visualize_sales.py
├── .gitignore
└── README.md
```

## 📈 Dataset and Results

The full synthetic dataset initially contained **1,000,000 records**. After cleaning and validation, the resulting dataset contained **929,553 records** and an additional calculated `Revenue` column.

Key results:

- **Records retained:** 929,553
- **Date range:** January 2022 – December 2025
- **Missing values after cleaning:** 0
- **Exact duplicate records after cleaning:** 0
- **Total calculated revenue:** 557,649,692,622.96

*Note: The dataset is synthetic, and the currency is unspecified. The full raw and cleaned datasets are excluded from this GitHub repository because of their size. The included sample dataset and source scripts support exploration of the project.*

## 📊 Visualizations

The project generates the following charts:

1. Revenue by product
2. Revenue by region
3. Monthly revenue trend
4. Revenue by payment method

The charts are available in `reports/charts/`.

## 💻 Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Enes-arch-hub/retail-sales-data-analytics.git
cd retail-sales-data-analytics
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install pandas numpy matplotlib streamlit pyarrow
```

### 4. Launch the dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

**Note:** The dashboard expects the cleaned dataset at `data/processed/retail_sales_clean.csv`. Since the full cleaned dataset is excluded from the repository, you must generate or obtain that file before running the dashboard. The scripts in `src/` provide the data-processing workflow.

## 🎯 Learning Outcomes

This project strengthened practical skills in:

- Data quality assessment and cleaning
- Working with large CSV datasets
- Exploratory data analysis
- Data aggregation and business reporting
- Statistical visualization
- Building interactive data applications
- Organizing a reproducible Python project
- Version control with Git and GitHub

## 👨‍💻 Author

**Enes Mumeita**

Data Science student interested in data analytics, machine learning, and building practical data-driven applications.

- GitHub: [@Enes-arch-hub](https://github.com/Enes-arch-hub)

---

*Built as a practical data analytics portfolio project.*
