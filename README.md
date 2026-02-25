# Inventory-Management-System
This is my python project for Advanced Python Certification in SLIPD

A desktop inventory management application built with **Python 3**, **Tkinter**, and **MySQL**. This system helps businesses track products, manage stock levels, record transactions, and generate insights about their inventory.

## Project structure 


├── assets

├── output    

├── .gitignore   

├── setup_database.py 

├── main.py

├── config.py

├── requirements.txt

└── README.md           



**Screenshots**
<img width="1910" height="886" alt="image" src="https://github.com/user-attachments/assets/abe2e26f-2a56-43e4-8b95-c59467f25678" />
<img width="1854" height="587" alt="image" src="https://github.com/user-attachments/assets/4f19c7c1-c94d-4e7a-8adf-b2db12e3d80c" />
<img width="1889" height="883" alt="image" src="https://github.com/user-attachments/assets/77babb22-3b1d-49ee-b77d-aa2158f6ee2c" />
<img width="1864" height="636" alt="image" src="https://github.com/user-attachments/assets/2a4f5728-73c0-4f04-9f80-404b612c30fd" />

**Prerequisites**

- Python 3.7 
- MySQL Server 5.7 
- MySQL Connector

  ## Installation

### 1. Clone the Repository

git clone https://github.com/lavindulcpperera-cell/inventory-management-system.git
cd inventory-management-system
``
### 2. Install Dependencies

pip install -r requirements.txt
```

Or install manually:
```bash
pip install mysql-connector-python
```

### 3. Setup the Database

Run the database setup script:

```bash
python setup_database.py
```
## Database Schema

### Categories Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Category ID |
| name | VARCHAR(100) | Category name |
| description | TEXT | Category description |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last update |

### Products Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Product ID |
| name | VARCHAR(200) | Product name |
| sku | VARCHAR(100) | Stock Keeping Unit (unique) |
| description | TEXT | Product description |
| category_id | INT (FK) | Reference to category |
| quantity | INT | Current stock quantity |
| price | DECIMAL(10,2) | Product price |
| min_stock_level | INT | Minimum stock threshold |
| created_at | TIMESTAMP | Creation date |
| updated_at | TIMESTAMP | Last update |

### Transactions Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Transaction ID |
| product_id | INT (FK) | Reference to product |
| transaction_type | ENUM | 'IN' or 'OUT' |
| quantity | INT | Quantity moved |
| notes | TEXT | Transaction notes |
| user | VARCHAR(100) | User who made the transaction |
| created_at | TIMESTAMP | Transaction date |

## Usage Guide

### Adding a Product
1. Click "Products" in the sidebar or menu
2. Click "+ Add Product" button
3. Fill in product details (Name, SKU, Quantity, Price)
4. Select a category (optional)
5. Click "Save Product"

### Managing Stock
1. Select a product from the list
2. Click "Stock In/Out" button
3. Choose movement type (In/Out)
4. Enter quantity and notes
5. Click "Save"

### Low Stock Alerts
- Navigate to "Low Stock" to see products below minimum threshold
- Products are automatically flagged when stock is low


  
