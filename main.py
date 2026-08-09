
from abc import ABC, abstractmethod



class OrderTracker:
    """
    Singleton Class:
    Guarantees only a single instance exists to manage global order counting.
    """
    _instance = None  # Holds the single instance

    def __new__(cls):
        # If no instance exists yet, create one
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.order_count = 0  # Global order counter
        return cls._instance

    def get_next_order_id(self) -> int:
        """Increments and returns the next sequential order number."""
        self.order_count += 1
        return self.order_count

