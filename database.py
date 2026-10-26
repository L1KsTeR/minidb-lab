from storage import Storage
from table import Table
from typing import List, Dict, Any, Optional, Callable

class MiniDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.storage = Storage(db_path)
        self.tables: Dict[str, Table] = {}
        self._load()

    def _load(self):
        schema = self.storage.load_schema()
        for tname, info in schema.items():
            t = Table(tname, info["fields"], info["types"], info["pk"])
            loaded = self.storage.load_table(tname)
            if loaded:
                t.rows = loaded["rows"]
                if t.rows:
                    t._next_id = max(int(r[t.pk]) for r in t.rows if r[t.pk] is not None) + 1
            self.tables[tname] = t

    def _save(self):
        schema = {name: {"fields": t.fields, "types": t.types, "pk": t.pk} for name, t in self.tables.items()}
        self.storage.save_schema(schema)
        for name, t in self.tables.items():
            self.storage.save_table(name, t.fields, t.types, t.pk, t.rows)

    def create_table(self, name: str, fields: Dict[str, str], pk: str) -> Table:
        if name in self.tables:
            raise ValueError(f"Table '{name}' already exists")
        t = Table(name, list(fields.keys()), fields, pk)
        self.tables[name] = t
        self._save()
        return t

    def insert(self, table_name: str, row: Dict[str, Any]) -> Any:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found")
        pk_val = self.tables[table_name].insert(row)
        self._save()
        return pk_val

    def select(self, table_name: str, columns: Optional[List[str]] = None, where: Optional[Callable] = None) -> List[Dict]:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found")
        return self.tables[table_name].select(columns, where)

    def update(self, table_name: str, where: Callable, updates: Dict[str, Any]) -> int:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found")
        count = self.tables[table_name].update(where, updates)
        self._save()
        return count

    def delete(self, table_name: str, where: Callable) -> int:
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found")
        count = self.tables[table_name].delete(where)
        self._save()
        return count

    def list_tables(self) -> List[str]:
        return list(self.tables.keys())
