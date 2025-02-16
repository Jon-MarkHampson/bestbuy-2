# **Store Management App**  
A simple **command-line** Python application for managing a store’s inventory. Users can **list products, check stock, and place orders** through an interactive menu.

---

## **Overview**  
This Store Management App is a learning project that covers **Python classes, methods, and user interaction** in a command-line environment.  

### **Key Components**  
#### **Product Module**  
- Defines a product's name, price, stock quantity, and active status.  
- Supports different product types: **Stocked Products, Non-Stocked Products, Limited Products, and Add-Ons**.  
- Implements automatic deactivation when stock reaches zero.  

#### **Store Module**  
- Manages a list of `Product` objects.  
- Provides helper methods for:  
  - Listing active products  
  - Checking total stock  
  - Processing orders  

#### **Main Script**  
- Provides a **menu-driven CLI** to interact with the store.  
- Uses a **dispatcher pattern** for efficient function handling.  

---

## **Project Structure**  

```bash
.
├── main.py
├── products.py
├── store.py
├── promotions.py
├── text_colour_helper.py
├── requirements.txt
└── README.md
```

### **`main.py`**  
- Initializes products and creates a `Store` instance.  
- Displays a **menu-driven CLI** for product management and ordering.  
- Uses **color-coded text formatting** (via `text_colour_helper.py`).  

### **`products.py`**  
- Contains the `Product` class with various product types.  
- Implements methods like `buy()`, `activate()`, and `deactivate()`.  

### **`store.py`**  
- Implements the `Store` class to manage products.  
- Handles orders and stock tracking.  

### **`promotions.py`**  
- Implements promotional offers like **percentage discounts** and **buy-one-get-one deals**.  

### **`text_colour_helper.py`**  
- Adds **color-coded** output for better CLI readability.  

---

## **Installation and Setup**  

### **Clone the Repository**  
```bash
git clone https://github.com/Jon-MarkHampson/bestbuy-2.git
cd bestbuy-2
```

### **Create a Virtual Environment** (Optional, Recommended)  
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\\Scripts\\activate      # Windows
```

### **Install Dependencies**  
```bash
pip install -r requirements.txt
```

---

## **Features**  

### **Product Management**  
✅ Add, update, or remove products.  
✅ Automatically deactivates **out-of-stock** products.  
✅ Supports **different product types** (Stocked, Non-Stocked, Limited, Add-Ons).  

### **Store Management**  
✅ Lists active products with quantity, price, and promotions.  
✅ Aggregates total stock quantity.  

### **Ordering System**  
✅ **New: Order Menu UI Improvements!**  
✅ Supports **stocked & non-stocked** products.  
✅ **Limited Products now enforce purchase limits.**  
✅ **Shopping cart displays name, quantity, unit price, and subtotal.**  
✅ Prevents duplicate **one-time purchase add-ons** from being added multiple times.  
✅ Order validation ensures correct quantity selection.  

---

## **Contributing**  
Contributions are welcome! To contribute:  

1. **Fork** the repository.  
2. **Create a new feature branch:**  
   ```bash
   git checkout -b feature/<your-feature-name>
   ```
3. **Make changes and commit:**  
   ```bash
   git commit -m "feat: add a cool new feature"
   ```
4. **Push to your branch:**  
   ```bash
   git push origin feature/<your-feature-name>
   ```
5. **Create a Pull Request** describing your changes.  

---

## **License**  
This project is open source under the **MIT License**. Feel free to adapt and use it!  

---
