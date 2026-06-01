# Basic Singleton (lazy initialization)

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# --- Main ---
if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()

    print(s1 is s2)   # True





# Thread-safe Singleton

import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        return cls._instance

# --- Main ---
if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()

    print(s1 is s2)   # True
