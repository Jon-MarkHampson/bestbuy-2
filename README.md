# Store Management App
A simple command-line based Python application that simulates a store's inventory management.
You can list products, check total stock, and place orders by choosing from a menu.

------------------------------

## Overview
This Store Management App is a small project designed for learning Python classes, methods, and user interaction via a command-line interface. The key components are:

### Product:
Defines a product's name, price, stock quantity, and whether it is active.
### Store:
Manages a list of Product objects, providing helper methods for adding products, removing products, displaying product inventory, calculating total stock, and processing orders.
### Main Script:
Provides a menu-driven CLI for users to list products, view total quantities, and make orders.

## Project Structure

```bash
.
├── main.py
├── products.py
├── store.py
└── README.md
```
### main.py

Initializes some product instances and creates a Store object.
Displays a text-based menu to the user, prompting for actions.
Uses a dispatcher approach to call different functions based on the menu selection.

### products.py

Contains the Product class definition.
Implements attributes (name, price, quantity, active) and methods (buy, activate, deactivate, etc.).


### store.py

Implements the Store class, which keeps track of a list of products.
Includes methods for adding products, removing products, retrieving active products, computing total quantity, and processing an order.


## Installation and Setup
### Clone the repository

clone https://github.com/Jon-MarkHampson/bestbuy.git

```bash
cd bestbuy
```


Create and activate a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

Currently, there are no external dependencies.
If there are in future there will be a requirements.txt (Skip for now - if they exist in the future use the command below.)

```bash

pip install -r requirements.txt
```

------------------------------

## Features
## Product Management

Create, update, or remove Product instances.
Automatically deactivates products when stock hits zero.
Store Management

Aggregate and display total quantity of all products in one place.
List active products.
Ordering System

Buy a specified quantity of a product; automatically adjusts the product’s stock.
Throws exceptions if insufficient stock or product is inactive.

## Contributing
### Contributions are welcome! Here’s how you can get involved:
- Fork the repository.
- Create a new feature branch:
```bash
git checkout -b feature/<your-feature-name>
```

- Commit your changes:
```bash
git commit -m "feat: add a cool new feature"
```

- Push to your branch:
```bash
git push origin feature/<your-feature-name>
```

- Create a Pull Request describing your changes.

------------------------------
## License
This project is open source under the MIT License. Feel free to adapt and use it for your needs.