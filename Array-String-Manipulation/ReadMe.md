# Two Sum API - Advanced Production-Ready Solution

## 📌 Overview
This project is a **high-performance API** that finds two numbers in a dataset that sum to a given target. Designed for **large-scale production environments**, it incorporates:

- **Asynchronous execution** (asyncio)
- **Multi-threading & multi-processing** (for performance optimization)
- **Excel file import** (to handle large datasets)
- **Redis caching** (to improve response times)
- **PostgreSQL database integration** (to store results)
- **Advanced error handling** (circuit breakers, logging, structured responses)

---

## 🚀 Features
✅ **Reads from Excel files** (Pandas)  
✅ **Caches results in Redis** (for faster performance)  
✅ **Stores results in PostgreSQL** (for persistence)  
✅ **Handles large datasets efficiently** (multi-threading & multi-processing)  
✅ **Asynchronous API** (Flask + asyncio)  
✅ **Circuit breaker pattern** (to prevent repeated failures)  
✅ **Structured error handling** (logging, decorators, global exception handling)  

---

## 🛠 Installation

### 1️⃣ **Clone the Repository**
```sh
 git clone https://github.com/moses000/two-sum-api.git
 cd two-sum-api
```

### 2️⃣ **Set Up a Virtual Environment**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Set Up PostgreSQL Database**
1. Install PostgreSQL if not already installed.
2. Create a database:
   ```sql
   CREATE DATABASE twosumdb;
   ```
3. Update the `DATABASE_URL` in `config.py`:
   ```python
   DATABASE_URL = "postgresql://username:password@localhost/twosumdb"
   ```
4. Run migrations:
   ```sh
   python setup_db.py
   ```

### 5️⃣ **Set Up Redis Cache**
Ensure Redis is installed and running:
```sh
redis-server
```

---

## ⚡ Usage

### **Start the Server**
```sh
python app.py
```

### **API Endpoints**

#### 1️⃣ Find Two Sum Pair
**POST** `/two_sum`
##### **Request Body:**
```json
{
  "nums": [2, 7, 11, 15],
  "target": 9
}
```
##### **Response:**
```json
{
  "indices": [0, 1],
  "numbers": [2, 7]
}
```

#### 2️⃣ Find Two Sum Pair from Excel File
**POST** `/two_sum`
##### **Request Body:**
```json
{
  "filepath": "data/numbers.xlsx",
  "target": 9
}
```
##### **Response:**
```json
{
  "indices": [10, 22],
  "numbers": [4, 5]
}
```

---

## 🏗️ Project Structure
```
📂 two-sum-api/
├── 📄 app.py            # Main Flask application
├── 📄 setup_db.py       # Database setup script
├── 📄 config.py         # Configuration settings
├── 📄 requirements.txt  # Dependencies
├── 📂 models/           # Database models
├── 📂 utils/            # Utility functions (Excel parsing, Redis caching, etc.)
├── 📂 logs/             # Log files
└── 📂 data/             # Sample Excel files
```

---

## 🛡 Advanced Error Handling
- **Logging Errors Instead of Just Printing** (Stored in `logs/errors.log`)
- **Using `assert` for Quick Debugging** (During development)
- **Error Handling with Decorators** (For reusable error management)
- **Error Handling in Multi-Threading & Multi-Processing**
- **Global Exception Handling (`sys.excepthook`)**
- **Structured Error Responses for APIs**
- **Circuit Breakers for Resilience**
- **Error Handling in Asynchronous Code (`asyncio`)**

---

## 👨‍💻 Contributing
### 1️⃣ **Fork the Repository**
Click on the `Fork` button at the top of this repository.

### 2️⃣ **Clone Your Fork**
```sh
git clone https://github.com/yourusername/two-sum-api.git
cd two-sum-api
```

### 3️⃣ **Create a New Branch**
```sh
git checkout -b feature-name
```

### 4️⃣ **Make Your Changes & Commit**
```sh
git add .
git commit -m "Added new feature"
```

### 5️⃣ **Push to Your Fork & Create Pull Request**
```sh
git push origin feature-name
```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## ⭐ Acknowledgments
Special thanks to **githun.com/@moses000** for building this scalable and resilient API. If you find this project helpful, please **star 🌟 the repository**!

