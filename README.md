# StockMaster: Inventory Management System

## Overview
This project is an Inventory Management System from our proposal "Inventory Management Optimization: A Hill Climbing Approach for Dynamic Restocking Alerts" designed to optimize reorder quantities using a modified hill climb algorithm with Economic Order Quantity (EOQ) model as the fitness function. The system dynamically calculates the optimal reorder quantity, while considering discounts based on quantity ranges, and optimal reorder point with standard ROP formula.

## Features
- **Product Management**: Add, update, and delete product information.
- **Dynamic Restocking Alerts**: Alerts for low stock levels and optimal reorder quantities.
- **Modified Steepest-Ascent Hill Climb Algorithm**: Optimizes reorder quantities using a proposed EOQ formula.
- **Discount Management**: Incorporates discounts based on quantity ranges from an Excel file.

## Technologies Used
### Frontend
- HTML, CSS, JS
- Bootstrap
- jQuery

### Backend
- Python
- Flask
- SQLite
- SQLAlchemy
- Pandas

## Notes
* Ensure you have Python installed and accessible from your command line environment.

## Installation
* STEP 1: Download the `G8_ProjectProposal` folder in [G8_ProjectImplementation](https://drive.google.com/drive/folders/1dh6g2RoXLxTW-dIzJq0iZj8p8pYjqZjx?usp=sharing) and unzip it to your preferred directory.

* STEP 2: Open a terminal or command prompt and navigate to the directory where you unzipped G8_ProjectProposal

* STEP 3: Install dependencies on your terminal using the package manager [pip](https://pip.pypa.io/en/stable/). Flask, SQLAlchemy, and pandas are required to run the application. Only install Flask-Migrate when you want to migrate changes from your `models.py` file to the SQLite database.

    ```bash 
    pip install Flask SQLAlchemy pandas Flask-Migrate
    ```

## Usage
1. Run the application
    * Start the application by running `app.py`

    ```python
    Your\Preferred\Directory\G8_ProjectProposal> python app.py
    ```
2. Access the application
    * Open your web browser and go to http://localhost:5000 to access the application. 
3. Login
    * Click on `'Get Started'` and use the following credentials: admin@gmail.com / password
4. Explore the dashboard
    * Use the dashboard to manage products.
5. Restock Optimization
    * Click `'edit'` on any product, enter necessary optimization inputs, and click `'optimize'`
    * To save the optimized values, enter the values from the optimized results into the product information and click `'Save Changes'` 

## Credits
Polytechnic University of the Philippines - Manila, Philippines  
BS Computer Science 2-5  

**Group 8 Members:**
- Bolado, Aaron John C.
- Millano, Ryan Kris F.
- Oseña Krystine Hermionne E.
- Pailden, Catherine Joy R.