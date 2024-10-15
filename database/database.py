import json
import os


class Database:
    def __init__(self, db_path="database.json"):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)  # Initialize with an empty dictionary

    def _load_db(self):
        with open(self.db_path, "r") as f:
            return json.load(f)

    def _save_db(self, db_content):
        with open(self.db_path, "w") as f:
            json.dump(db_content, f, indent=4)

    def find(self, collection_name, query={}):
        db = self._load_db()
        collection = db.get(collection_name, [])
        if not collection:
            return []
        # Case-insensitive search and matching logic
        return [
            doc
            for doc in collection
            if all(str(doc.get(k)).lower() == str(v).lower() for k, v in query.items())
        ]

    def find_one(self, collection_name, query=None):
        # Reuse the find method to get the first matching document
        result = self.find(collection_name, query)
        return result[0] if result else None

    def insert(self, collection_name, document):
        db = self._load_db()
        if collection_name not in db:
            db[collection_name] = []
        db[collection_name].append(document)
        self._save_db(db)
        return document

    def update_one(self, collection_name, query, update_fields):
        db = self._load_db()
        collection = db.get(collection_name, None)
        if collection is None:
            return None
        for doc in collection:
            if all(doc.get(k) == v for k, v in query.items()):
                doc.update(update_fields)
                db[collection_name] = collection
                self._save_db(db)
                return doc

        return None

    def delete_one(self, collection_name, query):
        db = self._load_db()
        collection = db.get(collection_name, [])
        new_collection = [
            doc
            for doc in collection
            if not all(doc.get(k) == v for k, v in query.items())
        ]
        if len(collection) != len(new_collection):
            db[collection_name] = new_collection
            self._save_db(db)
            return True
        return False
