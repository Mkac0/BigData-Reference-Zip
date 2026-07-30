import pandas as pd
import sqlite3

def process_data():

    # Loading the transactions data from the CSV file into a pandas DataFrame
    file_path = r"src/data/transactions.csv" 
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    df.columns = df.columns.str.strip()
    
    # Removing any rows with missing values in the DataFrame (Use dropna or another method)
    df.dropna(inplace=True)  # You can change this to other methods if required

    # Converting the 'TransactionDate' column to a datetime format using pandas
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])

    # Setting up a connection to SQLite database and create a table if it doesn't exist
    conn = sqlite3.connect("src/data/transactions.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
    TransactionID TEXT PRIMARY KEY,
    CustomerID INTEGER,
    Product TEXT,
    Amount REAL,
    TransactionDate TEXT,
    PaymentMethod TEXT,
    City TEXT,
    Category TEXT
    )
    """)
    
    # TO DO: Insert data into the database
    # Your task: Insert the cleaned DataFrame into the SQLite database. Ensure to replace the table if it already exists.
    df.to_sql("transactions", conn, if_exists="replace", index=False)

    # Example Queries - Write SQL queries based on the instructions below

    # TO DO: Query for Top 5 Most Sold Products
    # Your task: Write an SQL query to find the top 5 most sold products based on transaction count.
    print("\n" + "="*50)
    print("Top 5 Most Sold Products:")
    print("="*50)
    cursor.execute(
        """
        SELECT Product, COUNT(*) as Total_Transactions
        FROM transactions
        GROUP BY Product
        ORDER BY Total_Transactions DESC
        LIMIT 5;
        """
    )
    for row in cursor.fetchall():
        print(row)


    # TO DO:  Query for Monthly Revenue Trend
    # Your task: Write an SQL query to find the total revenue per month.
    print("\n" + "=" * 50)
    print("Monthly Revenue Trend:")
    print("=" * 50)
    cursor.execute(
        """
        SELECT strftime('%Y-%m', TransactionDate) as Month, 
        SUM(Amount) as Total_Revenue
        FROM transactions
        GROUP BY Month
        ORDER BY Month ASC;
        """
    )
    for row in cursor.fetchall():
        print(row)

    # TO DO:  Query for Payment Method Popularity
    # Your task: Write an SQL query to find the popularity of each payment method used in transactions.
    print("\n" + "=" * 50)
    print("Payment Method Popularity:")
    print("=" * 50)
    cursor.execute(
        """
        SELECT PaymentMethod, COUNT(*) as Total_Transactions
        FROM transactions
        GROUP BY PaymentMethod
        ORDER BY Total_Transactions DESC;
        """
    )
    for row in cursor.fetchall():
        print(row)

    # TO DO:  Query for Top 5 Cities with Most Transactions
    # Your task: Write an SQL query to find the top 5 cities with the most transactions.
    print("\n" + "=" * 50)
    print("Top 5 Cities with Most Transactions:")
    print("=" * 50)
    cursor.execute(
        """
        SELECT City, COUNT(*) AS Total_Transactions
        FROM transactions
        GROUP BY City
        ORDER BY Total_Transactions DESC
        LIMIT 5;
        """
    )
    for row in cursor.fetchall():
        print(row)

    # TO DO:  Query for Top 5 High-Spending Customers
    # Your task: Write an SQL query to find the top 5 customers who spent the most in total.
    print("\n" + "=" * 50)
    print("Top 5 High-Spending Customers:")
    print("=" * 50)
    cursor.execute(
        """
        SELECT CustomerID, SUM(Amount) AS Total_Spent
        FROM transactions
        GROUP BY CustomerID
        ORDER BY Total_Spent DESC
        LIMIT 5;
        """
    )
    for row in cursor.fetchall():
        print(row)

    # TO DO:  Query for Hadoop vs Spark Related Product Sales
    # Your task: Write an SQL query to categorize products related to Hadoop and Spark and find their sales.
    print("\n" + "=" * 50)
    print("Hadoop vs Spark Related Product Sales:")
    print("=" * 50)
    cursor.execute(
        """
        SELECT CASE
            WHEN Product LIKE '%Hadoop%' THEN 'Hadoop'
            WHEN Product LIKE '%Spark%' THEN 'Spark'
            ELSE 'Other'
        END AS Product_Category,
        SUM(Amount) AS Total_Sales
        FROM transactions
        GROUP BY Product_Category;
        """
    )
    for row in cursor.fetchall():
        print(row)

    # TO DO:  Query for Top Spending Customers in Each City
    # Your task: Write an SQL query to find the top spending customer in each city using subqueries.
    print("\n" + "=" * 50)
    print("Top Spending Customers in Each City:")
    print("=" * 50)
    cursor.execute(
        """
        SELECT City, CustomerID, Total_Spent
        FROM (
            SELECT City, CustomerID, SUM(Amount) AS Total_Spent,
            RANK() OVER (PARTITION BY City ORDER BY SUM(Amount) DESC) as Rank
            FROM transactions
            GROUP BY City, CustomerID
        ) AS Ranked
        WHERE Rank = 1;
        """
    )
    for row in cursor.fetchall():
        print(row)


    # Step 8: Close the connection
    # Your task: After all queries, make sure to commit any changes and close the connection
    conn.commit()
    conn.close()
    print("\n✅ Data Processing & Advanced Analysis Completed Successfully!")

if __name__ == "__main__":
    process_data()
