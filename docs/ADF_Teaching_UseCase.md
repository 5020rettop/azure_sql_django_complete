# Teaching Azure Data Factory with the Azure SQL Django App

This document outlines a practical use case for teaching **Azure Data Factory (ADF)** and **ETL (Extract, Transform, Load)** concepts using the existing Azure SQL Django application.

## 1. Scenario: E-commerce Analytics Pipeline

### The Business Problem
The "Azure SQL Django" e-commerce application stores data in two different systems:
1.  **Azure SQL Database**: Stores structured transactional data (Orders, Products, Stores).
2.  **MongoDB**: Stores unstructured customer feedback (Product Reviews).

The business intelligence team wants a **Unified Product Performance Dashboard** that correlates **sales volume** (from SQL) with **customer sentiment** (from MongoDB) to answer questions like:
*   *"Do higher-rated products sell more?"*
*   *"Which products have high sales but low ratings?"*

### The Solution (ETL Pipeline)
We will build an ADF pipeline to:
1.  **Extract**: Raw data from Azure SQL (Orders/Products) and MongoDB (Reviews).
2.  **Transform**: Join the datasets, aggregate sales counts, and calculate average review ratings.
3.  **Load**: Save the enriched dataset into an **Analytics Table in Azure SQL** for easy reporting.

---

## 2. Prerequisites

To complete this lesson, students need:
*   **Azure Subscription** (Free Tier is sufficient).
*   **Azure Data Factory** resource (V2).
*   **Azure SQL Database** (deployed for the Django App).
*   **MongoDB** (Cosmos DB for MongoDB API or a Mongo instance accessible from Azure).
*   **Azure Storage Account** (Blob Storage) with a container named `data-lake`.

---

## 3. Step-by-Step Implementation Guide

### Phase 1: Connect to Data Sources (Linked Services)
*Concepts: Linked Services, Integration Runtimes.*

1.  Open Azure Data Factory Studio.
2.  Go to **Manage** > **Linked Services** > **New**.
3.  **Azure SQL**: Connect to the Django App's database.
4.  **MongoDB**: Connect to the instance storing reviews.
5.  **Azure Blob Storage**: Connect to the `data-lake` container.

### Phase 2: Ingest Data (Copy Data Tool)
*Concepts: Datasets, Copy Activity, Source & Sink.*

We need to stage the raw data in the Data Lake before transformation.

1.  Create a new **Pipeline** named `Ingest_Raw_Data`.
2.  Add a **Copy Data** activity for **Products**:
    *   **Source**: Azure SQL Table `api_product`.
    *   **Sink**: Blob Storage `data-lake/raw/products.csv`.
3.  Add a **Copy Data** activity for **Orders**:
    *   **Source**: Azure SQL Table `api_order` (and `api_orderitem`).
    *   **Sink**: Blob Storage `data-lake/raw/orders.csv`.
4.  Add a **Copy Data** activity for **Reviews**:
    *   **Source**: MongoDB Collection `reviews`.
    *   **Sink**: Blob Storage `data-lake/raw/reviews.json`.

### Phase 3: Transform Data (Mapping Data Flows)
*Concepts: Data Flows, Joins, Aggregates, Derived Columns.*

1.  Create a new **Data Flow** named `Transform_Product_Analytics`.
2.  **Add Sources**:
    *   Source 1: `raw/products.csv`
    *   Source 2: `raw/orders.csv`
    *   Source 3: `raw/reviews.json`
3.  **Aggregate Sales**:
    *   Group `orders` by `product_id`.
    *   Aggregate: `TotalSales = count(order_id)`.
4.  **Aggregate Reviews**:
    *   Group `reviews` by `product_id`.
    *   Aggregate: `AvgRating = avg(rating)`, `ReviewCount = count(review_id)`.
5.  **Join Data**:
    *   Join `Products` with `SalesAgg` (Inner Join on ID).
    *   Join result with `ReviewsAgg` (Left Outer Join on ID - to keep products with no reviews).
6.  **Clean/Format**:
    *   Use **Derived Column** to handle null ratings (e.g., set to 0).
    *   Select only relevant columns: `ProductName`, `Price`, `TotalSales`, `AvgRating`, `ReviewCount`.

### Phase 4: Load to Destination (Sink)
*Concept: Writing Final Output.*

1.  Add a **Sink** to the Data Flow.
2.  **Dataset**: Create a new dataset for **Azure SQL Database**.
3.  **Table**: Select "Edit" and enter a new table name, e.g., `ProductAnalytics`.
4.  **Settings**: Check **"Auto create table"** to allow ADF to create the table schema automatically based on the data flow.
5.  Run the Data Flow via a **Pipeline**.

### Phase 5: Verify Data in SQL
*Concept: Consuming the processed data.*

1.  Use SQL Management Studio or the Azure Portal Query Editor.
2.  Run `SELECT * FROM ProductAnalytics`.
3.  Verify that you see the combined data with sales counts and review ratings.

---

## 4. Extension: Importing External Data (Blob to SQL)
*Scenario: "Planned vs. Actual" Analysis.*

In the real world, **Sales Targets** are often set in spreadsheets (offline data) by business teams, while **Actual Sales** happen in the database (online data).

We use `target_sales.csv` to teach students how to:
1.  **Ingest offline data**: Bring the CSV from Blob Storage into Azure SQL.
2.  **Perform Comparative Analytics**: Once loaded, they can write a SQL query to join `ProductAnalytics` (Actuals) with `SalesTargets` (Targets) to calculate **% Performance**.

### Step 1: Prepare Data
    *   Locate the file `csv/target_sales.csv` in the repository.
    *   Upload this file to your Blob Storage container (e.g., `data-lake/input/target_sales.csv`).

2.  **Create Pipeline `Import_Sales_Targets`**:
    *   Add a **Copy Data** activity.
    *   **Source**: Blob Storage (`input/target_sales.csv`).
    *   **Sink**: Azure SQL Database.
        *   Create a new table named `SalesTargets`.
        *   Enable **"Auto create table"**.

3.  **Run & Verify**:
    *   Trigger the pipeline.
    *   Check Azure SQL to confirm the `SalesTargets` table exists and contains data.

---

## 5. Key Teaching Points

*   **Hybrid Data Integration**: Demonstrates handling both Relational (SQL) and NoSQL (Mongo) data.
*   **Schema Drift**: Discuss how ADF handles changing schemas in MongoDB (NoSQL) vs Fixed Schemas in SQL.
*   **Orchestration**: Show how to chain the Ingestion Pipeline to trigger the Transformation Pipeline upon success.
*   **Monitoring**: Use the Monitor tab to check pipeline runs, data preview, and debug errors.

---

## 6. Extension Activities

1.  **Logic Apps**: Trigger an email alert if a product's average rating drops below 3 stars.
2.  **Power BI**: Connect Power BI to the `ProductAnalytics` sink to visualize the dashboard.
3.  **Parameters**: Make the pipeline dynamic to handle different dates or regions.
