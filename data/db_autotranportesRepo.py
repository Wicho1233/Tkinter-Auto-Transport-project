from data.db_config  import get_connection

def crear_tabla_si_no_existe():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cardenasAdaptacion (
            tr INTEGER,   
            nombreAdaptacion TEXT,
            mantenimiento TEXT,
            fechaMant TEXT,
            kiloActu INTEGER,
            kiloMant INTEGER,
            costo REAL,
            estado TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cardenasDivision (
            tr INTEGER,   
            numero INTEGER,
            nombreDivision TEXT,
            mantenimiento TEXT,
            fechaMant TEXT,
            kiloActu INTEGER,
            kiloMant INTEGER,
            costo REAL,
            estado TEXT
        );
    ''')
    conn.commit()
    conn.close()

def eliminar_mantenimiento_adaptacion(tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM cardenasAdaptacion
        WHERE tr = ? AND nombreAdaptacion = ? AND mantenimiento = ? AND fechaMant = ? 
        AND kiloActu = ? AND kiloMant = ? AND costo = ? AND estado = ?
    ''', (tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado))
    conn.commit()
    conn.close()

def eliminar_mantenimiento_division(tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM cardenasDivision 
        WHERE tr = ? AND numero = ? AND nombreDivision = ? AND mantenimiento = ? AND fechaMant = ? 
        AND kiloActu = ? AND kiloMant = ? AND costo = ? AND estado = ?
    ''', (tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado))
    conn.commit()
    conn.close()

def insertar_mantenimiento_adaptacion(tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cardenasAdaptacion (tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado))
    conn.commit()
    conn.close()

def insertar_mantenimiento_division(tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cardenasDivision (tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado))
    conn.commit()
    conn.close()

def obtener_mantenimientos_por_nombreAdaptacion(nombreAdaptacion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado
        FROM cardenasAdaptacion
        WHERE nombreAdaptacion = ?
    ''', (nombreAdaptacion,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_mantenimientos_por_division(nombreDivision):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr, numero, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado
        FROM cardenasDivision
        WHERE nombreDivision = ?
    ''', (nombreDivision,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_todos_mantenimientos_mal_estado_adaptacion():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado
        FROM cardenasAdaptacion
        WHERE estado = 'Mal estado'
    ''')
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_todos_mantenimientos_mal_estado_division():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado
        FROM cardenasDivision
        WHERE estado = 'Mal estado'
    ''')
    datos = cursor.fetchall()
    conn.close()
    return datos

def actualizar_mantenimiento_adaptacion(tr, nombreAdaptacion, mantenimiento_original, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cardenasAdaptacion
        SET mantenimiento = ?, fechaMant = ?, kiloActu = ?, kiloMant = ?, costo = ?, estado = ?
        WHERE tr = ? AND nombreAdaptacion = ? AND mantenimiento = ?
    ''', (mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado, tr, nombreAdaptacion, mantenimiento_original))
    conn.commit()
    conn.close()

def actualizar_mantenimiento_division(tr, numero, nombreDivision, mantenimiento_original, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cardenasDivision
        SET mantenimiento = ?, fechaMant = ?, kiloActu = ?, kiloMant = ?, costo = ?, estado = ?
        WHERE tr = ? AND numero = ? AND nombreDivision = ? AND mantenimiento = ?
    ''', (mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado, tr, numero, nombreDivision, mantenimiento_original))
    conn.commit()
    conn.close()

def buscar_por_tr_adaptacion(tr):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr, nombreAdaptacion, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado
        FROM cardenasAdaptacion
        WHERE tr = ?
    ''', (tr,))
    datos = cursor.fetchall()
    conn.close()
    return datos

def buscar_por_tr_division(tr):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tr, numero, nombreDivision, mantenimiento, fechaMant, kiloActu, kiloMant, costo, estado
        FROM cardenasDivision
        WHERE tr = ?
    ''', (tr,))
    datos = cursor.fetchall()
    conn.close()
    return datos