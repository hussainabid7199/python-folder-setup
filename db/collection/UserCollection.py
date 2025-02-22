
# from dependency_injector import containers, providers
# from db.connection import dbConnection

# db = providers.Singleton(dbConnection)  
# class UserCollection:
#      def create_collection(self, collection_name):
#         if collection_name not in self.db.list_collection_names():
#             self.db.create_collection(collection_name)
#             print(f"Creating collection '{collection_name}'")
#         else:
#             print("Collection '{collection_name}' already exists")
#             return self.db[collection_name]

#     def get_collection(self, collection_name):
#         return self.db[collection_name]