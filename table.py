from typing import List, Dict, Any, Optional, Callable

class Table:
    def __init__(self, name: str, fields: List[str], types: Dict[str, str], pk: str):
        self.name = name
        self.fields = fields
        self.types = types
        self.pk = pk
        self.rows: List[Dict[str, Any]] = []
        self._next_id = 1

    def _cast(self, val: Any, dtype: str) -> Any:
        if dtype == "INT":
            return int(val)
        elif dtype == "FLOAT":
            return float(val)
        return str(val)

    def insert(self, row: Dict[str, Any]) -> int:
        casted = {}
        for fld in self.fields:
            if fld in row:
                casted[fld] = self._cast(row[fld], self.types[fld])
            else:
                casted[fld] = None

        pk_val = casted.get(self.pk)
        if pk_val is not None:
            for existing in self.rows:
                if existing[self.pk] == pk_val:
                    raise ValueError(f"Duplicate primary key '{self.pk}'={pk_val} in table '{self.name}'")

        if pk_val is None and self.types.get(self.pk) == "INT":
            casted[self.pk] = self._next_id
            self._next_id = max(self._next_id, casted[self.pk] + 1)
        elif pk_val is not None:
            self._next_id = max(self._next_id, int(pk_val) + 1)

        self.rows.append(casted)
        return casted[self.pk]

    def select(self, columns: Optional[List[str]] = None, where: Optional[Callable] = None) -> List[Dict]:
        if columns is None:
            columns = self.fields
        results = []
        for row in self.rows:
            if where is None or where(row):
                results.append({c: row[c] for c in columns})
        return results

    def update(self, where: Callable, updates: Dict[str, Any]) -> int:
        count = 0
        for row in self.rows:
            if where(row):
                for fld, val in updates.items():
                    row[fld] = self._cast(val, self.types[fld])
                count += 1
        return count

    def delete(self, where: Callable) -> int:
        to_delete = []
        for i, row in enumerate(self.rows):
            if where(row):
                to_delete.append(i)
        for i in reversed(to_delete):
            self.rows.pop(i)
        return len(to_delete)
