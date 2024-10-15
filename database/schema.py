class Schema:
    def __init__(self, **fields):
        self.fields = fields

    def validate(self, data):
        validated_data = {}
        for field, field_type in self.fields.items():
            if field not in data:
                raise ValueError(f"Missing field: {field}")
            if not isinstance(data[field], field_type):
                raise TypeError(
                    f"Field '{field}' must be of type {field_type.__name__}."
                )
            validated_data[field] = data[field]
        return validated_data
