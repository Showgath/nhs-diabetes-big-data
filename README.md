# NHS Diabetes Prescriptions — Big Data & Streaming

This project applies big data tools to analyse NHS England metformin prescriptions and build an end‑to‑end analytics workflow, combining **PySpark**, **Power BI**, **Streamlit**, and **Kafka**. It was developed as part of the CC6058 Big Data and Visualisation module and showcases both batch and real‑time data processing. [file:181][file:184]

---

## 1. Project overview

The work is split into two main parts:

- **Part 1 – Batch analytics with Spark (NHS prescriptions)**  
  - Ingests a large prescription dataset (`Diabetes.csv`) for metformin across GP practices in Tower Hamlets. [file:183][file:184]  
  - Performs full data engineering in PySpark: cleaning, imputation, feature engineering, scaling, and clustering. [file:181][file:184]  
  - Trains and evaluates linear regression models to predict prescription `ACTUALCOST`, comparing:
    - Original target model: R ≈ 0.63 and RMSE ≈ 56.25.  
    - Log‑transformed target model: R² ≈ 0.995 and RMSE ≈ 0.0935. [file:181][file:184]  
  - Visualises results with interactive Power BI dashboards (practice‑level totals, time series, geospatial map, and drill‑down dashboard). [file:184]

- **Part 2 – Real‑time streaming with Kafka (IBM stock data)**  
  - Uses a Kafka **producer** to fetch IBM stock prices from the Alpha Vantage API at 5‑minute intervals and push them into a Kafka topic. [file:184]  
  - A Kafka **consumer** reads the stream, prints messages, computes descriptive statistics (average volume, max close, min open), and appends the data to CSV for long‑term storage. [file:184]

A Streamlit dashboard complements the Spark pipeline by giving an interactive front‑end for exploring the transformed dataset. [file:182][file:184]

---

## 2. Repository contents

- **`First Spark Session.ipynb`**  
  PySpark notebook that drives the batch analytics pipeline: [file:181][file:184]  
  - Reads `Diabetes.csv` into a Spark DataFrame and prints schema/metadata (14078 rows, 15 columns).  
  - Cleans data and imputes 94 missing values in `POSTCODE`, `PRACTICELATITUDE`, and `PRACTICELONGITUDE` for practice `F84714` using default records.  
  - Drops low‑information columns (`BNFCHAPTERPLUSCODE`, `PRACTICECODE`, `PRACTICENAME`, `POSTCODE`) and engineers new features.  
  - Converts `YEARMONTH` into separate numeric `YEAR` and `MONTH` features.  
  - Encodes categorical variables:
    - `CHEMICALSUBSTANCEBNFDESCR` with `StringIndexer`.  
    - `BNFDESCRIPTION` with `StringIndexer` + `OneHotEncoder` due to higher cardinality.  
  - Applies log transforms to skewed numeric fields (`TOTALQUANTITY`, `NIC`, `ADQUSAGE`, `ACTUALCOST`) and scales features using `StandardScaler` and `MinMaxScaler`.  
  - Clusters practices into 4 geospatial clusters based on latitude and longitude (E1, E2, E3, E14 postcodes) using `KMeans`.  
  - Builds two ML pipelines:
    - Pipeline 1: predicts `LOGACTUALCOST`.  
    - Pipeline 2: predicts `ACTUALCOST` directly.  
    - Both use an 80/20 train‑test split and `LinearRegression`.  
  - Evaluates both pipelines with RMSE and R/R² and writes the final transformed dataset to `transformeddata.csv` for downstream tools.

- **`Diabetes.csv`**  
  Raw NHS England metformin prescription data including: [file:183][file:184]  
  - Practice identifiers and locations (`PRACTICECODE`, `POSTCODE`, `PRACTICELATITUDE`, `PRACTICELONGITUDE`).  
  - Time (`YEARMONTH`), quantities (`TOTALQUANTITY`, `ITEMS`, `QUANTITY`).  
  - Cost fields (`NIC`, `ADQUSAGE`, `ACTUALCOST`).  
  - Drug details (`CHEMICALSUBSTANCEBNFDESCR`, `BNFDESCRIPTION`).

- **`Streamlit_dashboard.py`**  
  Streamlit app to explore the transformed data interactively: [file:182][file:184]  
  - Loads a user‑uploaded transformed CSV (e.g. `transformeddata.csv`).  
  - Uses a `reversetransformdata` function to invert scaling and log transforms, allowing comparison between transformed and original‑scale values.  
  - Features:
    - Toggle between **“Original Data”** and **“Transformed Data”** views.  
    - Line and bar charts over selected columns for quick EDA.  
    - Search and filter by any column, displaying matching rows dynamically.

- **`Report.pdf`**  
  Full academic report documenting the methodology, Spark vs MapReduce comparison, experimental results, Power BI dashboards, Kafka producer/consumer design, and reflective discussion. [file:184]

- **`Diabetes.pbix`**  
  Power BI report with: [file:184]  
  - Practice‑level ranking of total metformin prescriptions (e.g. Goodmans Field Health Centre ≈ 1.72M prescriptions, highest).  
  - Monthly time‑series of actual cost (August ≈ £51.5k, June ≈ £40.5k).  
  - Geospatial map of total prescriptions per practice.  
  - An interactive dashboard with practice slicer and linked visuals.

---

## 3. How to run the Spark pipeline

1. **Environment setup**

   ```bash
   conda create -n big-data python=3.10
   conda activate big-data
   pip install pyspark pandas numpy scikit-learn tabulate
   ```

2. **Run the notebook**

   - Ensure `Diabetes.csv` is in the repository folder or adjust the file path in the notebook.  
   - Start Jupyter:

     ```bash
     jupyter notebook
     ```

   - Open `First Spark Session.ipynb` and run all cells to:
     - Clean and transform the data.  
     - Train and evaluate linear regression models.  
     - Export `transformeddata.csv` for visualisation and the Streamlit app.

---

## 4. How to use the Streamlit dashboard

1. Install Streamlit (same environment):

   ```bash
   pip install streamlit
   ```

2. Make sure you have `transformeddata.csv` generated by the notebook.

3. Run:

   ```bash
   streamlit run Streamlit_dashboard.py
   ```

4. In the web UI:

   - Upload `transformeddata.csv` via the file uploader.  
   - Use the **View Original Data** checkbox to toggle between transformed and original‑scale data.  
   - Select columns for visualisation to generate line/bar charts.  
   - Use the search and filter controls to focus on specific subsets (e.g. a practice, month, or cost range). [file:182][file:184]

---

## 5. Kafka streaming (described in report)

The Kafka component is documented in `Report.pdf` and demonstrates real‑time data processing: [file:184]

- **Producer (`producer.py`, described)**  
  - Connects to Alpha Vantage’s intraday IBM endpoint.  
  - Fetches 5‑minute OHLCV bars and publishes JSON messages to a Kafka topic (e.g. `stock-stream`).

- **Consumer (`consumer.py`, described)**  
  - Subscribes to the same topic.  
  - Prints each message and calculates:
    - Average volume in the current batch.  
    - Maximum close price.  
    - Minimum open price.  
  - Appends records to `stockdata.csv` for later analysis.

These scripts illustrate how to extend the batch analytics skillset into streaming architectures using Kafka.

---

## 6. Skills demonstrated

- Distributed data processing with **Apache Spark (PySpark)**. [file:181][file:184]  
- Feature engineering: imputation, encoding, log transforms, scaling, and clustering.  
- Supervised learning with **linear regression** and pipeline APIs.  
- Data visualisation in **Power BI** and **Streamlit**. [file:182][file:184]  
- Real‑time **Kafka** producer–consumer design with external APIs. [file:184]

