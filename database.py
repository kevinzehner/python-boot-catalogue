import sqlite3


def get_unique_manufacturers(db_path):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Manuf FROM boots ORDER BY Manuf ASC")
    manufacturers = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(f"Manufacturers retrieved: {manufacturers}")
    return manufacturers


def get_models(db_path, manufacturer):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT Model FROM boots WHERE Manuf = ? ORDER BY Model ASC",
        (manufacturer,),
    )
    models = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(f"Models for {manufacturer} retrieved: {models}")
    return models


def get_engine_sizes(db_path, manufacturer, model):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT EngineSize FROM boots WHERE Manuf = ? AND Model = ? ORDER BY EngineSize ASC",
        (manufacturer, model),
    )
    engine_sizes = [str(row[0]) for row in cursor.fetchall()]
    conn.close()
    print(f"Engine sizes for {manufacturer}, {model} retrieved: {engine_sizes}")
    return engine_sizes


def get_mark_series(db_path, manufacturer, model, engine_size):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT MarkSeries FROM boots WHERE Manuf = ? AND Model = ? AND EngineSize = ? ORDER BY MarkSeries ASC",
        (manufacturer, model, engine_size),
    )
    mark_series = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(
        f"Mark series for {manufacturer}, {model}, {engine_size} retrieved: {mark_series}"
    )
    return mark_series


def get_drive_types(db_path, manufacturer, model, engine_size, mark_series):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT TransDrive FROM boots WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND MarkSeries = ? ORDER BY TransDrive ASC",
        (manufacturer, model, engine_size, mark_series),
    )
    drive_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(
        f"Drive types for {manufacturer}, {model}, {engine_size}, {mark_series} retrieved: {drive_types}"
    )
    return drive_types


def get_positions(db_path, manufacturer, model, engine_size, mark_series, drive_type):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT MPos FROM boots WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND MarkSeries = ? AND TransDrive = ? ORDER BY MPos ASC",
        (manufacturer, model, engine_size, mark_series, drive_type),
    )
    positions = [row[0] for row in cursor.fetchall()]
    conn.close()
    print(
        f"Positions for {manufacturer}, {model}, {engine_size}, {mark_series}, {drive_type} retrieved: {positions}"
    )
    return positions


def get_parts(db_path, criteria):
    print(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT DISTINCT PartNumber, PartSize FROM boots WHERE Manuf = ?"
    params = [criteria["manufacturer"]]

    if criteria["model"]:
        query += " AND Model = ?"
        params.append(criteria["model"])
    if criteria["engine_size"]:
        query += " AND EngineSize = ?"
        params.append(criteria["engine_size"])
    if criteria["mark_series"]:
        query += " AND MarkSeries = ?"
        params.append(criteria["mark_series"])
    if criteria["drive_type"]:
        query += " AND TransDrive = ?"
        params.append(criteria["drive_type"])
    if criteria["position"]:
        query += " AND MPos = ?"
        params.append(criteria["position"])

    query += " ORDER BY PartNumber ASC"

    cursor.execute(query, params)
    parts = cursor.fetchall()
    conn.close()
    print(f"Parts retrieved for criteria {criteria}: {parts}")
    return parts
