from data.db_config import get_connection

def insertar_usuario(nombreUsuario, contraUsuario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Usuarios (nombreUsuario, contraUsuario) VALUES (?, ?)", (nombreUsuario, contraUsuario))
        conn.commit()
    except:
        pass
    conn.close()

def verificar_usuario(nombreUsuario, contraUsuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE nombreUsuario = ? AND contraUsuario = ?", (nombreUsuario, contraUsuario))
    user = cursor.fetchone()
    conn.close()
    return user

def eliminar_usuario(idUsuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuarios  WHERE idUsuario = ? ",(idUsuario))
    conn.commit()
    conn.close()

