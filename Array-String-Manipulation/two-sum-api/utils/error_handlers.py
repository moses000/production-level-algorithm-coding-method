# ===================== ERROR HANDLERS =====================
# utils/error_handlers.py
import logging
import sys
from flask import jsonify

logging.basicConfig(filename="logs/errors.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def global_exception_handler(exctype, value, traceback):
    logging.error(f"Unhandled Exception: {value}")

sys.excepthook = global_exception_handler

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            return jsonify({"error": str(e)}), 400
    return wrapper
