import sqlite3


def get_unique_manufacturers(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Manuf FROM wheelbearing_LSODS ORDER BY Manuf ASC")
    manufacturers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return manufacturers


def get_models(db_path, manufacturer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT Model FROM wheelbearing_LSODS WHERE Manuf = ? ORDER BY Model ASC",
        (manufacturer,),
    )
    models = [row[0] for row in cursor.fetchall()]
    conn.close()
    return models


def get_engine_sizes(db_path, manufacturer, model):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT EngineSize FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? ORDER BY EngineSize ASC",
        (manufacturer, model),
    )
    engine_sizes = [str(row[0]) for row in cursor.fetchall()]
    conn.close()
    return engine_sizes


def get_mark_series(db_path, manufacturer, model, engine_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT mark_series FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? ORDER BY mark_series ASC",
        (manufacturer, model, engine_size),
    )
    mark_series = [row[0] for row in cursor.fetchall()]
    conn.close()
    return mark_series


def get_drive_types(db_path, manufacturer, model, engine_size, mark_series):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT TRWDansDRWDive FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ? ORDER BY TRWDansDRWDive ASC",
        (manufacturer, model, engine_size, mark_series),
    )
    drive_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return drive_types


def get_positions(db_path, manufacturer, model, engine_size, mark_series, drive_type):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT MPos FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ? AND TRWDansDRWDive = ? ORDER BY MPos ASC",
        (manufacturer, model, engine_size, mark_series, drive_type),
    )
    positions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return positions


def get_parts(db_path, criteria):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT DISTINCT LSODS_PartNumber, Bearing_1_Size, jpeg FROM wheelbearing_LSODS WHERE Manuf = ?"
    params = [criteria["manufacturer"]]

    if criteria["model"]:
        query += " AND Model = ?"
        params.append(criteria["model"])
    if criteria["engine_size"]:
        query += " AND EngineSize = ?"
        params.append(criteria["engine_size"])
    if criteria["mark_series"]:
        query += " AND mark_series = ?"
        params.append(criteria["mark_series"])
    if criteria["drive_type"]:
        query += " AND TRWDansDRWDive = ?"
        params.append(criteria["drive_type"])
    if criteria["position"]:
        query += " AND MPos = ?"
        params.append(criteria["position"])

    query += " ORDER BY LSODS_PartNumber ASC"

    cursor.execute(query, params)
    parts = cursor.fetchall()
    conn.close()
    return parts
