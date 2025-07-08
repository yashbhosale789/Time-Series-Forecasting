# Time Series Forecasting

This repository contains a complete pipeline for cleaning, validating, and forecasting sales data using Python. The project is designed to handle raw sales data, apply robust data cleaning techniques, and generate accurate future sales predictions using various time series models.

## Features

- **Data Cleaning Pipeline:**  
  - Handles missing values, zero values, and outliers.
  - Validates and standardizes date and column formats.
  - Rule-based validation for negative and unrealistic sales.
  - Visualization tools for exploring trends and anomalies.

- **Forecasting Models:**  
  - Implements models such as ARIMA, and others.
  - Calculates MAPE (Mean Absolute Percentage Error) for model evaluation.
  - Generates and saves future sales predictions.

- **Jupyter Notebooks:**  
  - `clean-datasheet.ipynb`: Data cleaning and validation pipeline.
  - `future_prediction.ipynb`: Time series forecasting and evaluation.

- **Streamlit App:**  
  - `app.py`: Interactive dashboard for visualizing results and metrics.

## Project Structure

```
├── app.py
├── clean-datasheet.ipynb
├── future_prediction.ipynb
├── mape_scores_monthly.csv
├── future_predictions_monthly.csv
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yashbhosale789/Time-Series-Forecasting.git
   ```

2. **Install dependencies:**
   - Recommended: Use a virtual environment.
   - Install required packages:
     ```bash
     pip install pandas numpy matplotlib seaborn statsmodels openpyxl scikit-learn pmdarima streamlit
     ```

3. **Run the Jupyter notebooks:**
   - Open `clean-datasheet.ipynb` and `future_prediction.ipynb` in Jupyter or VS Code.

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## Usage

- Place your raw sales Excel files in the project directory.
- Run the cleaning notebook to generate cleaned data.
- Use the forecasting notebook to train models and generate predictions.
- Visualize results in the Streamlit dashboard.

## Outputs

- **Cleaned_Sales_History.xlsx**: Cleaned sales data (ignored in git).
- **mape_scores_monthly.csv**: Model evaluation scores.
- **future_predictions_monthly.csv**: Forecasted sales.

## License

This project is for educational and research purposes.

---

*Created by Yash Bhosale*
