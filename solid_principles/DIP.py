# Dependency Injection vs Dependency Inversion
# Dependency Inversion : Depend on abstractions rather than concrete implementations. (A design principle)
# Dependency Injection : A technique used to achieve that.


# class MySQLDatabase:  # Low-level module
#     def save_to_sql(self, data):
#         print(f"Executing SQL Query: INSERT INTO users VALUES('{data}');")
#
#
# class MongoDBDatabase:  # Low-level module
#     def save_to_mongo(self, data):
#         print(f"Executing MongoDB Function: db.users.insert({{name: '{data}'}})")
#
#
# class UserService:  # High-level module (tightly coupled)
#     def __init__(self):
#         self.sql_db = MySQLDatabase()     # Direct dependency
#         self.mongo_db = MongoDBDatabase() # Direct dependency
#
#     def store_user_to_sql(self, user):
#         # MySQL-specific code
#         self.sql_db.save_to_sql(user)
#
#     def store_user_to_mongo(self, user):
#         # MongoDB-specific code
#         self.mongo_db.save_to_mongo(user)
#
#
# def main():
#     service = UserService()
#     service.store_user_to_sql("Aditya")
#     service.store_user_to_mongo("Rohit")
#
#
# if __name__ == "__main__":
#     main()



# ---------------------------------- DIP followed -----------------------------------------

from abc import ABC, abstractmethod


# Abstraction (interface)
class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass


# Low-level modules implement the abstraction
class MySQLDatabase(Database):
    def save(self, data):
        print(f"Executing SQL Query: INSERT INTO users VALUES('{data}');")


class MongoDBDatabase(Database):
    def save(self, data):
        print(f"Executing MongoDB Function: db.users.insert({{name: '{data}'}})")


# High-level module depends on abstraction, not concrete classes
class UserService:
    def __init__(self, database: Database):
        self.database = database  # Inject dependency

    def store_user(self, user):
        self.database.save(user)


def main():
    sql_service = UserService(MySQLDatabase())
    mongo_service = UserService(MongoDBDatabase())

    sql_service.store_user("Aditya")
    mongo_service.store_user("Rohit")


if __name__ == "__main__":
    main()