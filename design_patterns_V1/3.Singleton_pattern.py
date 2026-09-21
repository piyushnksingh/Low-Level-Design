# ============================================================
# SINGLETON PATTERN
# ============================================================
#
# Definition:
# Ensures that a class has ONLY ONE instance and provides
# a common/shared access point to that instance.
#
# Common examples:
# - Logger
# - Configuration Manager
# - Cache Manager
# - Database Connection Manager
#
#
# BASIC IMPLEMENTATION:
#
# __new__() controls object creation in Python.
#
# First call:
#     Create the instance.
#
# Later calls:
#     Return the existing instance.
#
#
# IMPORTANT:
# Use `is` to verify Singleton:
#
#     s1 is s2
#
# instead of:
#
#     s1 == s2
#
#
# THREAD-SAFE SINGLETON:
#
# Multiple threads can try to create the object simultaneously.
#
# Use a Lock to ensure only one thread creates the instance.
#
# Double-checked locking:
#
#     if instance is None:          # First check
#         with lock:
#             if instance is None:  # Second check
#                 create instance
#
#
# WHY DOUBLE CHECK?
# Avoid acquiring the lock every time after the instance
# has already been created.
#
#
# ADVANTAGES:
# - Guarantees a single shared instance.
# - Controlled object creation.
# - Useful for shared resources.
#
# DRAWBACKS:
# - Introduces global/shared state.
# - Can make testing harder.
# - Can create hidden dependencies.
# - Often overused.
#
#
# INTERVIEW ONE-LINER:
# "Singleton ensures that a class has only one instance and
# provides a global/shared access point to that instance."
#
# ============================================================

class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()

    print(s1 == s2)


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

if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()

    print(s1 == s2)


