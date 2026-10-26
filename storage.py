import os
from typing import List, Dict, Optional, Any

MAGIC = "MINIDB"
VERSION = "1.0"
SEP = "|"

class Storage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        if not os.path.exists(db_path):
            os.makedirs(db_path, exist_ok=True)

    def _table_file(self, table_name: str) -> str:
        return os.path.join(self.db_path, f"{table_name}.mdb")

    def _schema_file(self) -> str:
        return os.path.join(self.db_path, "_schema.mdb")

    def save_schema(self, tables: Dict[str, Dict]) -> None:
        with open(self._schema_file(), "w", encoding="utf-8") as f:
            f.write(f"{MAGIC}{SEP}{VERSION}\n")
            for name, info in tables.items():
                fields_str = SEP.join(f"{fld}:{info['types'][fld]}" for fld in info["fields"])
                f.write(f"TABLE{name}{SEP}{fields_str}{SEP}pk:{info['pk']}\n")

    def load_schema(self) -> Dict[str, Dict]:
        path = self._schema_file()
        if not os.path.exists(path):
            return {}
        tables = {}
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split(SEP)
            table_name = parts[0][len("TABLE"):]
            fields, types, pk = [], {}, None
            for p in parts[1:]:
                if p.startswith("pk:"):
                    pk = p[3:]
                else:
                    fname, ftype = p.split(":")
                    fields.append(fname)
                    types[fname] = ftype
            tables[table_name] = {"fields": fields, "types": types, "pk": pk}
        return tables

    def save_table(self, table_name: str, fields: List[str], types: Dict[str, str], pk: str, rows: List[Dict]) -> None:
        path = self._table_file(table_name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{MAGIC}{SEP}{VERSION}\n")
            schema_parts = [f"{fld}:{types[fld]}" for fld in fields]
            f.write(f"SCHEMA{SEP}{SEP.join(schema_parts)}{SEP}pk:{pk}\n")
            for row in rows:
                vals = [str(row[fld]) for fld in fields]
                f.write(f"DATA{SEP}{SEP.join(vals)}\n")

    def load_table(self, table_name: str) -> Optional[Dict]:
        path = self._table_file(table_name)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        fields, types, pk, rows = [], {}, None, []
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split(SEP)
            tag = parts[0]
            if tag == "SCHEMA":
                for p in parts[1:]:
                    if p.startswith("pk:"):
                        pk = p[3:]
                    else:
                        fname, ftype = p.split(":")
                        fields.append(fname)
                        types[fname] = ftype
            elif tag == "DATA":
                vals = parts[1:]
                row = {}
                for i, fld in enumerate(fields):
                    row[fld] = self._cast(vals[i], types[fld])
                rows.append(row)
        return {"fields": fields, "types": types, "pk": pk, "rows": rows}

    def _cast(self, val: str, dtype: str) -> Any:
        if dtype == "INT":
            return int(val)
        elif dtype == "FLOAT":
            return float(val)
        return val
