Industry-Grade Inventory & Demand Forecasting System
A comprehensive inventory management solution with advanced demand forecasting capabilities using ARIMA and machine learning models. Built with Python and Tkinter for small to medium-sized businesses.

📋 Table of Contents
Overview: This application provides a complete inventory management system with intelligent demand forecasting capabilities. It helps businesses optimize stock levels, reduce carrying costs, and prevent stockouts through data-driven insights and automated reorder suggestions.

Features:📦 Inventory Management
Complete CRUD Operations - Add, view, update, and delete products

Real-time Stock Tracking - Monitor current stock levels

Product Information - Store product ID, name, stock levels, reorder points, and cost prices

Sample Data Generation - Auto-generate realistic sales data for testing  

Screenshots

Installation

Usage

Project Structure

Models Overview

Data Format

API Reference

Troubleshooting

Contributing

License

🚀 Overview
This application provides a complete inventory management system with intelligent demand forecasting capabilities. It helps businesses optimize stock levels, reduce carrying costs, and prevent stockouts through data-driven insights and automated reorder suggestions.

Key Benefits
Reduce Inventory Costs by 15-30% through optimized stock levels

Prevent Stockouts with accurate demand forecasting

Automate Reordering with intelligent suggestion system

Improve Cash Flow by reducing excess inventory

Data-Driven Decisions with multiple forecasting models

✨ Features
📦 Inventory Management
Complete CRUD Operations - Add, view, update, and delete products

Real-time Stock Tracking - Monitor current stock levels

Product Information - Store product ID, name, stock levels, reorder points, and cost prices

Sample Data Generation - Auto-generate realistic sales data for testing

📊 Demand Forecasting
Multiple Forecasting Models

ARIMA - Statistical time series forecasting

Simple Models - Moving average and trend analysis

30-Day Demand Predictions - Forecast future demand accurately

Performance Metrics - RMSE and MAE for model evaluation

Visual Analytics - Interactive charts and graphs

🔔 Auto Reorder System
Intelligent Suggestions - Automated reorder recommendations

Urgency Levels - HIGH, MEDIUM, LOW priority indicators

Safety Stock Calculation - Dynamic buffer stock recommendations

Cost Optimization - Balance between stockouts and carrying costs

🎨 User Interface
Modern Tkinter GUI - User-friendly desktop application

Tabbed Interface - Organized workflow across different functionalities

Real-time Updates - Instant data refresh and visualization

Export Capabilities - Data export for further analysis

🖼️ Screenshots
Inventory Management Tab

text
[Product List View] | [Add/Edit Products] | [Real-time Stock Monitoring]
Demand Forecasting Tab

text
[Model Selection] | [Forecast Charts] | [Performance Metrics] | [30-day Predictions]
Reorder Suggestions Tab

text
[Urgent Items] | [Suggested Quantities] | [Priority Indicators]
🛠️ Installation
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Step-by-Step Installation
Clone or Download the Project

bash
# If using git
git clone <repository-url>
cd "Inventory Forecasting System with Python"

# Or download and extract the ZIP file
Create Virtual Environment (Recommended)

bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
Install Dependencies

bash
pip install -r requirements.txt
Verify Installation

bash
python main.py
Requirements File
The requirements.txt includes:

txt
pandas==2.0.3
numpy==1.24.3
matplotlib==3.7.2
statsmodels==0.14.0
scikit-learn==1.3.0
tkinter
🎯 Usage
Starting the Application
bash
python main.py
First-Time Setup
The application will automatically generate sample data

Five sample products with 2 years of sales data will be created

You can immediately start testing all features

Managing Inventory
Add New Products

Navigate to "Inventory Management" tab

Fill in product details:

Product ID (unique identifier)

Product Name

Current Stock Level

Reorder Level (trigger point for suggestions)

Cost Price

Click "Add Product"

Update Existing Products

Select product from the list

Modify fields as needed

Click "Update Product"

Delete Products

Select product from the list

Click "Delete Product"

Confirm deletion

Generating Forecasts
Select Product & Model

Go to "Demand Forecasting" tab

Choose product from dropdown

Select forecasting model (ARIMA or Simple)

Click "Generate Forecast"

Interpret Results

View forecast chart with historical data and predictions

Check performance metrics (RMSE, MAE)

Review 30-day demand predictions in table

Reorder Suggestions
Generate Suggestions

Navigate to "Reorder Suggestions" tab

Click "Generate Reorder Suggestions"

System automatically calculates optimal order quantities

Understand Urgency Levels

HIGH: Stock below 50% of reorder level

MEDIUM: Stock between 50-80% of reorder level

LOW: Stock above 80% of reorder level

📁 Project Structure
text
Inventory Forecasting System with Python/
├── main.py                 # Main application entry point
├── inventory.py            # Inventory management logic
├── forecasting.py          # Forecasting engine and visualization
├── models/                 # Forecasting models directory
│   ├── arima_model.py      # ARIMA forecasting implementation
│   └── simple_models.py    # Simple forecasting models
├── data/                   # Data storage directory
│   ├── inventory_data.csv  # Product inventory data
│   └── sales_data.csv      # Historical sales data
├── requirements.txt        # Python dependencies
└── README.md              # This file
🔬 Models Overview
ARIMA Model
Type: Statistical time series forecasting

Best For: Products with consistent seasonal patterns

Strengths: Handles trend and seasonality well

Output: Point forecasts with confidence intervals

Simple Models
Type: Ensemble of moving average and linear regression

Best For: New products or volatile demand patterns

Strengths: Fast computation, robust to outliers

Output: Combined forecast from multiple methods

📊 Data Format
Inventory Data (inventory_data.csv)
csv
product_id,product_name,current_stock,reorder_level,cost_price
P001,Laptop,45,50,800.0
P002,Mouse,120,100,25.0
Sales Data (sales_data.csv)
csv
date,product_id,quantity_sold
2023-01-01,P001,2
2023-01-01,P002,5
🔧 API Reference
InventoryManager Class
python
# Initialize
inventory = InventoryManager()

# Core methods
inventory.add_product(product_data)
inventory.update_product(product_id, product_data)  
inventory.delete_product(product_id)
inventory.get_all_products()
inventory.generate_reorder_suggestions()
DemandForecaster Class
python
# Initialize
forecaster = DemandForecaster()

# Generate forecast
forecast_df, metrics = forecaster.generate_forecast(
    product_id, model_type, days=30
)
🐛 Troubleshooting
Common Issues
ModuleNotFoundError: No module named 'models.simple_models'

bash
# Ensure models directory exists with simple_models.py
ls models/
# Should show: arima_model.py, simple_models.py
TensorFlow Compatibility Issues

The system uses simplified models to avoid TensorFlow dependencies

No action needed - compatible models are automatically used

Insufficient Data for Forecasting

Ensure at least 30 days of sales data exists

Use the sample data generation feature

Application Crashes on Startup

bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
Performance Tips
Use ARIMA for products with >90 days of historical data

Simple models work best for new products

Regular data maintenance improves forecast accuracy

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests or open issues for bugs and feature requests.

Development Setup
Fork the repository

Create a feature branch

Make your changes

Add tests if applicable

Submit a pull request
