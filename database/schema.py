class Schema:
    def __init__(self, **fields):
        self.fields = fields

    def validate(self, data):
        validated_data = {}
        for field, field_type in self.fields.items():
            if field in data:
                if isinstance(data[field], field_type):
                    validated_data[field] = data[field]
                else:
                    raise ValueError(f"Field {field} must be of type {
                                     field_type.__name__}")
            else:
                raise ValueError(f"Field {field} is missing")
        return validated_data
