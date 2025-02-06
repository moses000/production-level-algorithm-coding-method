# ===================== API APPLICATION =====================
# app.py
import asyncio
from flask import Flask, request, jsonify
from utils.error_handlers import error_handler
from utils.cache import get_cached_result, cache_result
from utils.circuit_breaker import breaker
from utils.excel_reader import read_excel_file
from models.twosum_result import TwoSumResult, Session

app = Flask(__name__)
session = Session()

@app.route("/two_sum", methods=["POST"])
@error_handler
async def async_two_sum():
    data = await request.get_json()
    nums = data.get("nums", [])
    target = data.get("target")
    filepath = data.get("filepath")

    if filepath:
        try:
            nums = read_excel_file(filepath)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    if not isinstance(nums, list) or len(nums) < 2:
        return jsonify({"error": "Invalid input array"}), 400
    if not isinstance(target, int):
        return jsonify({"error": "Target must be an integer"}), 400

    cache_key = f"two_sum:{tuple(nums)}:{target}"
    cached_result = get_cached_result(cache_key)
    if cached_result:
        return jsonify({"indices": cached_result[:2], "numbers": cached_result[2:]})

    def two_sum():
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i, num, complement]
            seen[num] = i
        raise ValueError("No valid pair found")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, lambda: breaker.call(two_sum))

    if result is None:
        return jsonify({"error": "No valid pair found"}), 400

    num1, num2 = result[2], result[3]
    db_result = TwoSumResult(num1=num1, num2=num2, target=target)
    session.add(db_result)
    session.commit()
    cache_result(cache_key, result)

    return jsonify({"indices": result[:2], "numbers": [num1, num2]})

if __name__ == "__main__":
    app.run(debug=True)
