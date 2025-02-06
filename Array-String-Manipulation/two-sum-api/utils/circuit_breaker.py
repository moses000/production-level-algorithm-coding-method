# ===================== CIRCUIT BREAKER =====================
# utils/circuit_breaker.py
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
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.open = True
            raise

breaker = CircuitBreaker()
