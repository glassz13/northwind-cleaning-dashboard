# 📊 Northwind Business Intelligence Dashboard

An end-to-end Data Cleaning and Business Intelligence Dashboard project using the **Northwind dataset**.
Built using **Python, Pandas, Plotly, and Streamlit**, this dashboard offers deep insights into customer behavior, shipping performance, revenue trends, and product sales across countries.

---

## 🌍 Live Preview

> * [ https://northwind-cleaning-dashboard-fpqvt2a4eyv4fj6kbvkwqs.streamlit.app/] Streamlit Share 


---

## 🔍 Project Features

* Cleaned and merged **6+ raw CSVs** into one master dataset.
* Engineered revenue, shipping, and time-related features.
* Built a **responsive interactive dashboard** with:

  * Time series analysis
  * Choropleth map for country-wise revenue
  * Treemap for top products
  * Customer revenue ranking
  * Boxplot for freight cost analysis
* Downloadable filtered data.
* Sidebar filters for time, category, and country.

---

## ⚖️ Technologies Used

* **Python** (Pandas, datetime, regex)
* **Plotly** (Express + Graph Objects)
* **Streamlit** (Web framework)
* **Data Cleaning & Feature Engineering**

---

## 📄 Dataset Info

**Source:** Northwind Traders (Sample Business Dataset)
**Files Used:**

* `orders.csv`
* `order_details.csv`
* `products.csv`
* `categories.csv`
* `customers.csv`
* `shippers.csv`

---

## 🤧 Data Cleaning & Merging Highlights

> Script: `northwind_cleaning_script.py`

* Removed duplicates and filled missing values.
* Standardized string columns, phone numbers, and null handling.
* Merged **orders + products + customers + shippers + categories**.
* Engineered:

  * `Revenue = Quantity x UnitPrice`
  * `DeliveryDays = ShippedDate - OrderDate`
  * `OrderMonth = OrderDate.to_period('M')`
* Removed unnecessary columns like fax, supplier info, stock levels.

**Final Output:** `northwind_master_dataset.csv`

---

## 🔍 Dashboard Insights

### ✅ Executive Summary

* **Total Revenue**
* **Average Order Value**
* **Order and Customer Count**
* **Best and Fastest Shippers**
* **On-time Shipment %**

### 📊 Monthly Revenue Trend

> Area plot with time-series annotations for peak revenue month.

### 💲 Top 10 Customers

> Horizontal bar chart with dollar value labels and sorting.

### 🍬 Top Products (Treemap)

> Interactive treemap grouped by category, showing top 5 per category.

### 🌎 Global Revenue Map

> Choropleth of revenue by country.

### 🚶️ Freight Cost Distribution

> Boxplot grouped by country and shipper, with mean line.

### 📃 Filtered Data Table + Download Button

> View/export selected data instantly.

---

## 🔧 How to Run This Project Locally

```bash
# 1. Clone this repo
https://github.com/your-username/northwind-dashboard

# 2. Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install requirements
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run app.py
```

---

## 🔍 Folder Structure

```
├── app.py                      # Streamlit dashboard script
├── northwind_cleaning_script.py   # Full data cleaning + merging code
├── northwind_master_dataset.csv  # Final processed dataset
├── customers.csv, orders.csv, etc. # Raw data files
└── README.md
```

---

## ✨ Future Improvements

* Add user login & dashboard saving feature
* Deploy on Streamlit Cloud / HuggingFace
* Add forecasting model for revenue prediction
* Add visual time range brushing for trend graphs

---

## 👤 Author

**Mohit Kumar**
IIT Delhi | Data Science & Machine Learning Enthusiast
[GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)

---

## 📅 Project Timeline

* Data Cleaning: 1 Day
* Dashboard Design: 2 Days
* Testing & Polishing: 1 Day

---

## 🎯 Outcome

This project demonstrates:

* Real-world dataset handling
* Cleaning + joining + feature engineering
* Business storytelling via dashboarding
* Industry-ready coding practices in EDA

---

> If you liked this project, consider giving it a ⭐ on GitHub!
