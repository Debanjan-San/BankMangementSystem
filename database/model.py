class Model:
    def __init__(self, collection_name, schema, db_instance):
        self.collection_name = collection_name
        self.schema = schema
        self.db = db_instance

    def validate_data(self, data):
        return self.schema.validate(data)

    def create(self, data):
        validated_data = self.validate_data(data)
        return self.db.insert(self.collection_name, validated_data)

    def update(self, query, update_fields):
        validated_update_fields = self.validate_data(update_fields)
        return self.db.update_one(self.collection_name, query, validated_update_fields)

    def find(self, query={}):
        return self.db.find(self.collection_name, query)

    def find_one(self, query={}):
        return self.db.find_one(self.collection_name, query)

    def delete(self, query):
        return self.db.delete_one(self.collection_name, query)
