import sqlite3
from datetime import datetime

def setup_database():
    # Connect to the database (creates mlops_registry.db)
    conn = sqlite3.connect('mlops_registry.db')
    cursor = conn.cursor()

    # Enforce foreign key constraints in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Datasets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            annotation_format TEXT NOT NULL,
            image_count INTEGER NOT NULL,
            domain TEXT
        )
    ''')

    # 2. Create Models Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            architecture TEXT NOT NULL,
            parameters_millions REAL,
            target_hardware TEXT
        )
    ''')

    # 3. Create Training Runs Table (Links Models and Datasets)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER,
            dataset_id INTEGER,
            epochs INTEGER,
            map_score REAL,
            inference_fps REAL,
            run_date TEXT,
            FOREIGN KEY (model_id) REFERENCES models (model_id),
            FOREIGN KEY (dataset_id) REFERENCES datasets (dataset_id)
        )
    ''')

    # --- Insert Professional Mock Data ---

    # Insert Datasets (e.g., drone botany detection, legal document parsing)
    datasets_data = [
        ('Agri-Drone-Canopy-v1', 'COCO', 15000, 'Botany/Agriculture'),
        ('Legal-Doc-Layouts', 'YOLO', 8500, 'LegalTech'),
        ('Urban-Traffic-Edge', 'COCO', 22000, 'Surveillance')
    ]
    cursor.executemany('''
        INSERT INTO datasets (dataset_name, annotation_format, image_count, domain)
        VALUES (?, ?, ?, ?)
    ''', datasets_data)

    # Insert Models (e.g., Edge deployment architectures)
    models_data = [
        ('YOLOv8-Nano', 3.2, 'NVIDIA Jetson'),
        ('DINOv2-Small', 21.0, 'Cloud GPU'),
        ('MobileNet-V3', 2.5, 'Edge TPU')
    ]
    cursor.executemany('''
        INSERT INTO models (architecture, parameters_millions, target_hardware)
        VALUES (?, ?, ?)
    ''', models_data)

    # Insert Training Runs (Mapping performance metrics)
    runs_data = [
        (1, 1, 100, 0.82, 45.0, '2026-04-10'), # YOLO on Agri-Drone
        (2, 2, 50, 0.94, 12.5, '2026-04-12'),  # DINOv2 on Legal Docs
        (1, 3, 150, 0.78, 60.0, '2026-05-01')  # YOLO on Urban Traffic
    ]
    cursor.executemany('''
        INSERT INTO training_runs (model_id, dataset_id, epochs, map_score, inference_fps, run_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', runs_data)

    conn.commit()
    conn.close()
    print("Professional MLOps database 'mlops_registry.db' created successfully.")

if __name__ == "__main__":
    setup_database()