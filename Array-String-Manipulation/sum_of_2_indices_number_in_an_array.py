import logging
import threading
import multiprocessing
import functools
import sys
import asyncio
import redis
import psycopg2
import pandas as pd
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ===================== CONFIGURATION =====================

# Logging Setup
logging.basicConfig(filename="errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Global Exception Handler for Debugging
def global_exception_handler(exctype, value, traceback):
    logging.error(f"Unhandled Exception: {value}")

sys.excepthook = global_exception_handler

# PostgreSQL Database Setup
DATABASE_URL = "postgresql://username:password@localhost/twosumdb"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Redis Cache Setup
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Flask App Setup
app = Flask(__name__)

# ===================== DATABASE MODEL =====================
class TwoSumResult(Base):
    __tablename__ = "two_sum_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    target = Column(Integer, nullable=False)

Base.metadata.create_all(engine)

# ===================== CIRCUIT BREAKER =====================
class CircuitBreaker:
    def __init__(self, failure_threshold=3):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.open = False

    def call(self, func, *args, **kwargs):
        if self.open:
            raise RuntimeError("Circuit breaker is open. Too many failures.")

        try:
            result = func(*args, **kwargs)
            self.failure_count = 0  # Reset on success
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.open = True  # Open circuit to prevent further calls
            raise

breaker = CircuitBreaker()

# ===================== ERROR HANDLING DECORATOR =====================
def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return jsonify({"error": str(e)}), 400
    return wrapper

# ===================== TWO SUM FUNCTION =====================
def two_sum(nums, target):
    assert isinstance(nums, list), "Input must be a list"
    assert isinstance(target, int), "Target must be an integer"

    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i, num, complement]
        seen[num] = i
    raise ValueError("No valid pair found")

# ===================== MULTI-THREADED EXECUTION =====================
def threaded_two_sum(nums, target):
    result = None

    def worker():
        nonlocal result
        try:
            result = breaker.call(two_sum, nums, target)
        except Exception as e:
            logging.error(f"Threaded Execution Error: {e}")

    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    return result

# ===================== MULTI-PROCESSING EXECUTION =====================
def parallel_two_sum(nums, target):
    with multiprocessing.Pool(processes=4) as pool:
        chunk_size = len(nums) // 4
        chunks = [nums[i:i + chunk_size] for i in range(0, len(nums), chunk_size)]
        results = pool.starmap(two_sum, [(chunk, target) for chunk in chunks])
        return next((res for res in results if res is not None), None)

# ===================== REDIS CACHE =====================
def get_cached_result(nums, target):
    key = f"two_sum:{tuple(nums)}:{target}"
    cached = redis_client.get(key)
    if cached:
        return eval(cached.decode())
    return None

def cache_result(nums, target, result):
    key = f"two_sum:{tuple(nums)}:{target}"
    redis_client.setex(key, 3600, str(result))  # Cache expires in 1 hour

# ===================== DATABASE STORAGE =====================
def save_to_db(num1, num2, target):
    result = TwoSumResult(num1=num1, num2=num2, target=target)
    session.add(result)
    session.commit()

# ===================== EXCEL FILE IMPORT =====================
def read_excel_file(filepath):
    try:
        df = pd.read_excel(filepath)
        return df["Numbers"].tolist()  # Assuming column name is 'Numbers'
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise ValueError("Invalid Excel file format")

# ===================== API ENDPOINT =====================
@app.route("/two_sum", methods=["POST"])
@error_handler
async def async_two_sum():
    data = await request.get_json()
    nums = data.get("nums", [])
    target = data.get("target")
    filepath = data.get("filepath")

    # Read data from Excel if provided
    if filepath:
        try:
            nums = read_excel_file(filepath)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # Error Handling
    if not isinstance(nums, list) or len(nums) < 2:
        return jsonify({"error": "Invalid input array"}), 400
    if not isinstance(target, int):
        return jsonify({"error": "Target must be an integer"}), 400

    # Check Cache
    cached_result = get_cached_result(nums, target)
    if cached_result:
        return jsonify({"indices": cached_result[:2], "numbers": cached_result[2:]})

    # Compute Result
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, threaded_two_sum, nums, target)

    if result is None:
        return jsonify({"error": "No valid pair found"}), 400

    # Store Result in DB and Cache
    num1, num2 = result[2], result[3]
    save_to_db(num1, num2, target)
    cache_result(nums, target, result)

    return jsonify({"indices": result[:2], "numbers": [num1, num2]})

# ===================== RUN SERVER =====================
if __name__ == "__main__":
    app.run(debug=True)
