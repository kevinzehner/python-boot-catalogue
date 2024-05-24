import sqlite3

def get_unique_manufacturers(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Manuf FROM wheelbearing_LSODS")
    manufacturers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return manufacturers

def get_models(db_path, manufacturer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Model FROM wheelbearing_LSODS WHERE Manuf = ?", (manufacturer,))
    models = [row[0] for row in cursor.fetchall()]
    conn.close()
    return models

def get_engine_sizes(db_path, manufacturer, model):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT EngineSize FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ?", 
                   (manufacturer, model))
    engine_sizes = [str(row[0]) for row in cursor.fetchall()]
    conn.close()
    return engine_sizes

def get_mark_series(db_path, manufacturer, model, engine_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT mark_series FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ?", 
                   (manufacturer, model, engine_size))
    mark_series = [row[0] for row in cursor.fetchall()]
    conn.close()
    return mark_series

def get_drive_types(db_path, manufacturer, model, engine_size, mark_series):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT TRWDansDRWDive FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ?", 
                   (manufacturer, model, engine_size, mark_series))
    drive_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return drive_types

def get_positions(db_path, manufacturer, model, engine_size, mark_series, drive_type):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT MPos FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ? AND TRWDansDRWDive = ?", 
                   (manufacturer, model, engine_size, mark_series, drive_type))
    positions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return positions

def get_parts(db_path, manufacturer, model, engine_size, mark_series, drive_type, position):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT DISTINCT LSODS_PartNumber, Bearing_1_Size FROM wheelbearing_LSODS
        WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ? AND TRWDansDRWDive = ? AND MPos = ?
    """
    cursor.execute(query, (manufacturer, model, engine_size, mark_series, drive_type, position))
    parts = cursor.fetchall()
    conn.close()
    return parts