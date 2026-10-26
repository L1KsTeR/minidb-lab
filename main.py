import os
import shutil
from database import MiniDB

def demo():
    db_path = "./mydb"
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    db = MiniDB(db_path)
    
    print("=== 1. Создание таблиц ===")
    db.create_table("datasets", {"id": "INT", "name": "STRING", "task": "STRING", "size": "INT"}, "id")
    db.create_table("models", {"id": "INT", "name": "STRING", "version": "STRING"}, "id")
    db.create_table("experiments", {"id": "INT", "dataset_id": "INT", "model_id": "INT", "accuracy": "FLOAT", "status": "STRING"}, "id")
    
    print("\n=== 2. INSERT ===")
    for i in range(1, 6):
        db.insert("datasets", {"id": i, "name": f"dataset_{i}", "task": "classification", "size": 1000*i})
        db.insert("models", {"id": i, "name": f"model_{i}", "version": f"v{i}.0"})
    
    for exp in [
        {"id": 1, "dataset_id": 1, "model_id": 1, "accuracy": 0.91, "status": "completed"},
        {"id": 2, "dataset_id": 1, "model_id": 2, "accuracy": 0.88, "status": "completed"},
        {"id": 3, "dataset_id": 2, "model_id": 1, "accuracy": 0.76, "status": "running"},
        {"id": 4, "dataset_id": 3, "model_id": 2, "accuracy": 0.95, "status": "completed"},
        {"id": 5, "dataset_id": 2, "model_id": 3, "accuracy": 0.82, "status": "failed"},
    ]:
        db.insert("experiments", exp)
    print("  Вставлено 5 experiments")

    print("\n=== 3. SELECT все ===")
    for r in db.select("experiments"):
        print(f"  {r}")

    print("\n=== 4. SELECT с условием (accuracy > 0.85) ===")
    for r in db.select("experiments", where=lambda r: r["accuracy"] > 0.85):
        print(f"  {r}")

    print("\n=== 5. UPDATE ===")
    db.update("experiments", where=lambda r: r["id"] == 3, updates={"status": "completed", "accuracy": 0.79})
    print("  experiment id=3 обновлён")

    print("\n=== 6. DELETE ===")
    db.delete("experiments", where=lambda r: r["id"] == 5)
    print("  experiment id=5 удалён")

    print("\n=== 7. Проверка сохранности ===")
    print(f"  Таблиц: {len(db.list_tables())}")
    print(f"  Datasets: {len(db.select('datasets'))}")
    print(f"  Models: {len(db.select('models'))}")
    print(f"  Experiments: {len(db.select('experiments'))}")
    
    print("\n Все операции выполнены успешно!")

if __name__ == "__main__":
    demo()
