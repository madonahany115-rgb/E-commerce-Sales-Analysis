import pandas as pd

df = pd.read_csv(r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\data\raw\Dataset.csv")


print(df.shape)

print(df.columns)

#missing values

print(df.isna().sum())

# Example: if numeric column has missing values
numeric_columns = df.select_dtypes(include="number").columns
for column in numeric_columns:
    if df[column].isna().sum() > 0:
        df[column] = df[column].fillna(df[column].median())

# Example: if categorical column has missing values
categorical_columns = df.select_dtypes(include="str").columns

for column in categorical_columns:
    if df[column].isna().sum() > 0:
        df[column] = df[column].fillna(df[column].mode()[0])


# =========================
# 3. Duplicates
# =========================
print(df.duplicated().sum())
if df.duplicated().sum() > 0:
    df = df.drop_duplicates()

# =========================
# 4. Data Types
# =========================
print(df.dtypes)
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["SignupDate"] = pd.to_datetime(df["SignupDate"], errors="coerce")


# =========================
# 5. Clean Text Columns
# =========================
categorical_columns = df.select_dtypes(include="str").columns
for column in categorical_columns:
    df[column] = df[column].str.strip()

# =========================
# 6. Numerical Validation
# =========================
print(df.describe())

# =========================
# 8. Outliers - IQR + Clipping
# =========================
numeric_columns = df.select_dtypes(include="number").columns
for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[column] = df[column].clip(lower=lower_bound,upper=upper_bound)

# =========================
# 9. Check IDs
# =========================

if "OrderID" in df.columns:
    print("\nDuplicate OrderID:",
          df["OrderID"].duplicated().sum())

# =========================
# 10. Date Validation
# =========================
date_columns = ["OrderDate", "SignupDate"]
for column in date_columns:

    if column in df.columns:
        print(f"\n{column}")

        print("Min:", df[column].min())
        print("Max:", df[column].max())

        print("Missing after conversion:",
              df[column].isna().sum())

# =========================
# 11. Final Validation
# =========================

print("\n========== FINAL CHECK ==========")

print("Shape:", df.shape)

print("\nMissing Values:")
print(df.isna().sum())

print("\nDuplicates:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nFinal Numerical Summary:")
print(df.describe())


# =========================
# Sales Overview
# =========================
total_sales = df["Sales"].sum()

total_orders = df["OrderID"].nunique()

total_quantity = df["Quantity"].sum()

average_order_value = df["OrderValue"].mean()

print("Total Sales:", total_sales)
print("Total Orders:", total_orders)
print("Total Quantity:", total_quantity)
print("Average Order Value:", average_order_value)

df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
df["Day"] = df["OrderDate"].dt.day

df["MonthName"] = df["OrderDate"].dt.month_name()

monthly_sales = (
    df.groupby(["Year", "Month", "MonthName"])["Sales"]
    .sum()
    .reset_index()
)

print(monthly_sales)


import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6)) #بتنشئ مساحة الرسم عرض وارتفاع 

months = (
    monthly_sales["Year"].astype(str)
    + "-"
    + monthly_sales["Month"].astype(str).str.zfill(2)
)  #عملتى المتغير ده وحفظت التاريخ بالشكل ده


plt.plot(
    months,
    monthly_sales["Sales"],
    marker="o",
    linewidth=2
)

plt.title("Monthly Sales Trend", fontsize=16, fontweight="bold")#العنوان 
plt.xlabel("Month", fontsize=12) 
plt.ylabel("Total Sales", fontsize=12)

plt.xticks(rotation=45) #اسماء الشهور مائله زاويه45 
plt.grid(axis="y", linestyle="--", alpha=0.5)  #دي بتضيف خطوط مساعدة في الرسم على yوالفا دى الشفافيه   

for x, y in zip(months, monthly_sales["Sales"]):
    plt.text(
        x,
        y + 3000,
        f"{y:,.0f}",
        ha="center",
        fontsize=8
    )#كتابة قيمة المبيعات على الرسم 

plt.tight_layout()#دي بتخلي Python يحاول يرتب عناصر الرسم تلقائيًا
plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\monthly_sales_trend.png",
    bbox_inches="tight"
)

plt.show()


#========================
#   Sales by Category
#========================
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(category_sales)


category_orders = (
    df.groupby("Category")["OrderID"]
    .nunique()
    .sort_values(ascending=False)
)

print(category_orders)



import matplotlib.pyplot as plt

plt.figure(figsize=(7, 5))

plt.bar(
    category_sales.index,
    category_sales.values,
    width=0.3  
)

plt.title("Sales by Category", fontsize=14, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Total Sales")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
# Save the visualization
plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\sales_by_category.png",
    bbox_inches="tight"
)
plt.show()



product_sales = (
    df.groupby("ProductName")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(product_sales)


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))

plt.barh(
    product_sales.index,
    product_sales.values
)

plt.title("Sales by Product", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales")
plt.ylabel("Product")

plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\sales_by_product.png",
    bbox_inches="tight"
)


plt.show()



#========================
# Customer Analysis
#========================

total_customers = df["CustomerID"].nunique()

print("Total Customers:", total_customers)


#========================
# Top Cities by Sales
#========================

city_sales = (
    df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(city_sales)



import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.barh(
    city_sales.index[::-1],
    city_sales.values[::-1],
    height=0.6
)

plt.title("Sales by City", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales")
plt.ylabel("City")

plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\sales_by_city.png",
    bbox_inches="tight"
)

plt.show()

#==========================
# TAverage Customer Age
#==========================

average_age = df["Age"].mean()

print("Average Customer Age:", average_age)


#==========================
#   Top Customers
#==========================
top_customers = (
    df.groupby("CustomerID")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_customers)

#==========================
#  Discount Analysis
#==========================
average_discount = df["Discount"].mean()

print("Average Discount:", average_discount)


discount_sales = (
    df.groupby("Discount")["Sales"]
    .agg(["mean", "sum", "count"])
    .sort_index()
)

print(discount_sales)


import matplotlib.pyplot as plt

plt.figure(figsize=(7, 5))

plt.bar(
    discount_sales.index.astype(str),
    discount_sales["mean"],
    width=0.3
 )

plt.title("Discount vs Average Sales", fontsize=14, fontweight="bold")
plt.xlabel("Discount (%)")
plt.ylabel("Average Sales")

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

# Save the visualization
plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\discount_vs_average_sales.png",
    bbox_inches="tight"
)

plt.show()

#=======================
#Best-Selling Products
#=======================
best_selling_products = (
    df.groupby("ProductName")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print(best_selling_products)



top10_products = best_selling_products.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top10_products.index[::-1],
    top10_products.values[::-1],
    height=0.6
)

plt.title("Top 10 Best-Selling Products", fontsize=14, fontweight="bold")
plt.xlabel("Total Quantity")
plt.ylabel("Product")

plt.grid(axis="x", linestyle="--", alpha=0.5)

plt.tight_layout()
# Save the visualization
plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\top_10_best_selling_products.png",
    bbox_inches="tight"
)

plt.show()


#=========================
#Highest Revenue Products
#========================
highest_revenue_products = (
    df.groupby("ProductName")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(highest_revenue_products)


low_selling_products = (
    df.groupby("ProductName")["Quantity"]
    .sum()
    .sort_values(ascending=True)
)

print(low_selling_products)



category_revenue = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(category_revenue)


#======================
#Status Distribution
#======================

status_counts = df["Status"].value_counts()

print(status_counts)


status_percentage = df["Status"].value_counts(normalize=True) * 100

print(status_percentage)


status_sales = (
    df.groupby("Status")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(status_sales)




import matplotlib.pyplot as plt

plt.figure(figsize=(7, 7))

plt.pie(
    status_percentage,
    labels=status_percentage.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Order Status Distribution")
plt.tight_layout()

plt.savefig(
    r"C:\Users\ZBook G3\Downloads\E-commerce Sales Analysis\visualizations\order_status_distribution.png",
    bbox_inches="tight"
)

plt.show()



#=========================
#Business Insights
#========================

highest_category = category_revenue.idxmax()
highest_category_sales = category_revenue.max()

print("Highest Revenue Category:", highest_category)
print("Total Sales:", highest_category_sales)
#Electronics generated the highest total sales among all categories, with total sales of 1,483,727.5.


best_product = best_selling_products.idxmax()
best_product_quantity = best_selling_products.max()

print("Best-Selling Product:", best_product)
print("Total Quantity Sold:", best_product_quantity)

# Notebook was the best-selling product by quantity,
# with a total quantity sold of 9,881.


highest_revenue_product = highest_revenue_products.idxmax()
highest_revenue = highest_revenue_products.max()

print("Highest Revenue Product:", highest_revenue_product)
print("Total Revenue:", highest_revenue)


# Business Insight:
# Headphones generated the highest total sales among all products,
# with total sales of 296,625.0.


highest_sales_city = city_sales.idxmax()
highest_city_sales = city_sales.max()

print("Highest Sales City:", highest_sales_city)
print("Total Sales:", highest_city_sales)

# Business Insight:
# Tehran generated the highest total sales among all cities,
# with total sales of 825,436.5.

completed_percentage = status_percentage["Completed"]

print("Completed Orders Percentage:", completed_percentage)

# Business Insight:
# Completed orders represented approximately 91.98% of all orders.

print("Average Discount:", average_discount)

# Business Insight:
# The average discount across all orders was approximately 7.29%.

# =========================
# Recommendations
# =========================

# Recommendation 1:
# Focus on the Electronics category because it generated
# the highest total sales among all categories.

# Recommendation 2:
# Maintain sufficient stock of Notebook because it had
# the highest total quantity sold among all products.

# Recommendation 3:
# Give attention to Headphones because it generated
# the highest total sales among all products.

# Recommendation 4:
# Focus on maintaining and supporting sales activities in Tehran,
# as it generated the highest total sales among all cities.

# Recommendation 5:
# Maintain the current order completion performance and
# monitor cancelled and returned orders for possible improvements.


df.to_csv("cleaned_ecommerce_sales.csv", index=False)

print("Cleaned dataset saved successfully.")


# ==========================================
# 12. Final Project Summary
# ==========================================

# Total Sales: 2,932,240.0
# Total Orders: 49,222
# Total Customers: 9,820
# Average Order Value: 59.57
# Average Discount: 7.29%

# Highest Revenue Category: Electronics
# Best-Selling Product by Quantity: Notebook
# Highest Revenue Product: Headphones
# Highest Sales City: Tehran
# Completed Orders: 91.98%

# Main Recommendations:
# - Focus on the Electronics category.
# - Maintain sufficient stock of Notebook.
# - Give attention to Headphones.
# - Support sales activities in Tehran.
# - Monitor cancelled and returned orders.