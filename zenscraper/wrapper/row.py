import hashlib
from typing import List, Any


class RowFieldValue(str):
    def __init__(self, value: str = ""):
        self._value = value

    @property
    def value(self) -> str:
        return str(self._value)

    @value.setter
    def value(self, new_value: str):
        self._value = new_value

    def is_missing(self):
        """Return True if the value is empty, else False."""
        self._value == ""

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"RowFieldValue({self._value!r})"


class Row:
    def __init__(self, fields: List[str]):
        self._field_values = {}
        self._init_field: List[str] = fields
        self._fields = [self._normalize_field_name(field) for field in fields]
        for field in self._fields:
            self._field_values[field] = RowFieldValue()

    def __getattr__(self, name):
        if name in self._field_values:
            return self._field_values[name]
        raise NotInRowAttributeError(type(self).__name__, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        elif name in self._field_values:
            if isinstance(value, RowFieldValue):
                self._field_values[name] = value
            else:
                self._field_values[name].value = value
        else:
            raise NotInRowAttributeError(type(self).__name__, name)

    @staticmethod
    def _normalize_field_name(field: str):
        """Normalize the field name to be a valid Python attribute name."""
        return field.lower().replace(" ", "_")

    @property
    def header(self) -> List[str]:
        """List of column names."""
        return self._init_field

    def clear(self):
        """Clear all field values."""
        for field in self._field_values:
            self._field_values[field].value = ""

    @property
    def values(self) -> List[str]:
        """List of current field values."""
        return [self._field_values[field].value for field in self._fields]

    def compute_key(self) -> str:
        """Compute the row's unique ObjectKey based on it's content."""
        str_rep = str([v for v in self.values]).encode()
        return hashlib.sha256(str_rep).hexdigest()

    def __str__(self):
        """Provide a simple string representation of the Row."""
        return f"Row({', '.join(f'{field}={self._field_values[field].value}' for field in self._fields)})"


class NotInRowAttributeError(Exception):
    """Missing row attribute error"""

    def __init__(self, cur_obj: Any, name: str):
        super().__init__(f"{cur_obj} object has not attribute {name}")
