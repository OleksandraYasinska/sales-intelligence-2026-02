# Strategic Sales Intelligence Dashboard 2026

## Project Overview
This repository contains a professional analytical dashboard for monitoring and analyzing strategic sales performance. The application is built using Python and Streamlit, providing a high-level overview of key business metrics (KPIs), geographical distribution, and product profitability.

## Live Demo
Access the deployed application here: 
https://sales-intelligence-2026-02-nn77fc2ypvkggkxw45g2cy.streamlit.app/

## Key Features
* **Executive Summary**: High-level view of Total Revenue, Net Profit, Average Order Value (AOV), and Active Customers.
* **Integrated Profitability Analysis**: Profit margins are displayed directly within the profit metric cards for context.
* **Trend Tracking**: Monthly dynamics of revenue and profit to identify seasonal patterns and growth rates.
* **Market Geography**: Interactive choropleth maps showing global sales distribution.
* **Operational Data View**: Searchable and sortable transaction registry with conditional formatting for profit analysis.

## Tech Stack
* **Language**: Python 3.13
* **Framework**: Streamlit (Web UI)
* **Data Manipulation**: Pandas (ETL and styling)
* **Visualization**: Plotly (Interactive charts and maps)
* **Color Theory**: Matplotlib (Used for advanced data frame color gradients)

## Project Structure
* `app.py`: Main application logic and UI configuration.
* `src/data_loader.py`: Module for data ingestion and cleaning.
* `data/`: Directory containing source CSV datasets.
* `requirements.txt`: List of dependencies for environment replication.
* `.gitignore`: Configuration to exclude unnecessary files and virtual environments from the repository.

## Installation and Local Deployment
1. Clone the repository:
   git clone https://github.com/OleksandraYasinska/sales-intelligence-2026-02.git
   
2. Install dependencies:
   pip install -r requirements.txt
   
3. Run the application:
   streamlit run app.py

## Business Logic and KPIs
The dashboard calculates several critical indicators:
* **Margin (%)**: Derived as (Total Profit / Total Sales) * 100.
* **AOV**: Calculated as the mean of the Sales column across the filtered dataset.
* **Profit Heatmap**: The operational data table uses a 'Blues' color map to highlight high-profit transactions automatically.

## Contact Information
Developed by Oleksandra Yasinska.
