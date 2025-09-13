from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, abort
from functools import wraps
from datetime import datetime
import mysql.connector
import io
from fpdf import FPDF
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '123'

####################### Configuración de uploads ###################
UPLOAD_FOLDER = os.path.join("static", "Uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Verifica extensión
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

####################### Conexión a la base ###################
def get_db():
    import mysql.connector
    return mysql.connector.connect(
        host="localhost",
        user="qruser",
        password="password123",
        database="qr_alco"
    )

####################### Decoradores ###################
def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario" not in session:
            flash("Debes iniciar sesión para acceder", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorada
################permisos de interfaz######################
def solo_admin(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if session.get("rol") != "admin":
            flash("No tienes permiso para acceder a esta sección", "error")
            return redirect(url_for("menu"))
        return f(*args, **kwargs)
    return decorada

def admin_o_supervisor(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if session.get("rol") not in ["admin", "supervisor"]:
            flash("No tienes permiso para acceder a esta sección", "error")
            return redirect(url_for("menu"))
        return f(*args, **kwargs)
    return decorada


####################### Principal para el menu ###################
@app.route("/")
@login_requerido
def menu():
    return render_template("menu.html")

####################### QR VALIDOS ###################
QRS_VALIDOS = [f"QRN{i}" for i in range(1, 21)]  # QRN1 hasta QRN20

@app.route("/check_qr")
@login_requerido
def check_qr():
    qr_id = request.args.get("qr_id", "").strip().upper()
    if qr_id not in QRS_VALIDOS:
        return jsonify({"valido": False, "activo": False, "mensaje": "QR inválido"})

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT estacion
        FROM seguimiento
        WHERE qr_id = %s
        ORDER BY fecha DESC
        LIMIT 1
    """, (qr_id,))
    ultimo = cursor.fetchone()
    cursor.close()
    conn.close()

    if ultimo and ultimo['estacion'].upper() not in ['SALIDA', 'FIN']:
        return jsonify({"valido": True, "activo": True, "mensaje": f"QR {qr_id} ya está activo en estación {ultimo['estacion']}"})

    return jsonify({"valido": True, "activo": False, "mensaje": "QR disponible"})

####################### Registro lleva al html de registro ###################
@app.route("/registro", methods=["GET", "POST"])
@login_requerido
def registro():
    if request.method == "POST":
        qr_id = request.form["qr_id"].strip().upper()
        folio = request.form["folio"]
        chofer = request.form["chofer"].strip()
        licencia = request.form["licencia"]
        empresa = request.form["empresa"]
        tipo_carga = request.form["tipo_carga"]

        if qr_id not in QRS_VALIDOS:
            flash(f"QR inválido. Solo se permiten: {', '.join(QRS_VALIDOS)}", "error")
            return redirect(url_for("registro"))

        estacion = request.form.get("estacion") if session.get("rol") == "admin" else session.get("estacion")

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # 🚫 Verificar si el chofer está prohibido
        cursor.execute("SELECT id FROM choferes_prohibidos WHERE nombre LIKE %s", (chofer,))
        prohibido = cursor.fetchone()
        if prohibido:
            flash(f"⛔ El chofer {chofer} está prohibido y no puede registrarse.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for("registro"))

        # ✅ Verificar si hay un registro activo con el mismo QR
        cursor.execute("""
            SELECT id FROM registros
            WHERE qr_id=%s AND activo=1
            ORDER BY fecha DESC LIMIT 1
        """, (qr_id,))
        activo = cursor.fetchone()
        if activo:
            flash(f"El QR {qr_id} ya tiene un registro activo. Finaliza ese primero.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for("registro"))

        # Insertar nuevo registro
        cursor.execute("""
            INSERT INTO registros (qr_id, folio, chofer, licencia, empresa, tipo_carga, estacion, fecha, activo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),1)
        """, (qr_id, folio, chofer, licencia, empresa, tipo_carga, estacion))
        registro_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()

        flash(f"QR {qr_id} registrado correctamente.", "success")
        return redirect(url_for("menu"))

    return render_template("registro.html")

####################### Revision de choferes vetados ###################
@app.route("/check_chofer")
def check_chofer():
    nombre = request.args.get("nombre", "").strip()
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM choferes_prohibidos WHERE nombre = %s", (nombre,))
    prohibido = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({"prohibido": bool(prohibido)})

####################### Registro choferes prohibidos ###################
@app.route("/registro_prohibido", methods=["GET", "POST"])
def registro_prohibido():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        curp = request.form["curp"].strip()
        fecha_nacimiento = request.form["fecha_nacimiento"]
        empresa = request.form["empresa"].strip()
        observacion = request.form["observacion"].strip()

        # Validar CURP duplicado
        cursor.execute("SELECT id FROM choferes_prohibidos WHERE curp=%s", (curp,))
        existente = cursor.fetchone()
        if existente:
            flash(f"⚠️ El CURP {curp} ya está registrado para otro chofer.", "error")
            cursor.close()
            conn.close()
            return redirect(url_for("registro_prohibido"))

        # Manejo de archivo (foto INE)
        ine_foto = None
        if "foto_ine" in request.files:
            file = request.files["foto_ine"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                ine_foto = filename
                save_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(save_path)

        # Insertar nuevo chofer prohibido
        cursor.execute("""
            INSERT INTO choferes_prohibidos (nombre, curp, fecha_nacimiento, empresa, observacion, ine_foto)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, curp, fecha_nacimiento, empresa, observacion, ine_foto))
        conn.commit()

        flash(f"Chofer {nombre} registrado como prohibido ✅", "success")

    # Traer todos los choferes prohibidos para mostrar en la lista
    cursor.execute("SELECT * FROM choferes_prohibidos ORDER BY id DESC")
    choferes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("registro_prohibido.html", choferes=choferes)

####################### Seguimiento ###################
@app.route("/seguimiento", methods=["GET", "POST"])
@login_requerido
def seguimiento():
    qr_id = request.form.get("qr_id") if request.method == "POST" else request.args.get("qr_id")
    estacion = session.get("estacion")
    mensaje = ""
    datos_qr = None
    historial = []

    if qr_id:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Tomar el último registro activo del QR
        cursor.execute("""
            SELECT * FROM registros
            WHERE qr_id=%s AND activo=1
            ORDER BY fecha DESC LIMIT 1
        """, (qr_id,))
        datos_qr = cursor.fetchone()

        if not datos_qr:
            mensaje = "⚠️ Este QR no tiene registros activos."
        else:
            registro_id = datos_qr['id']

            if request.method == "POST":
                estacion_a_registrar = request.form.get("estacion") if session.get("rol") == "admin" else estacion
                if estacion_a_registrar:
                    cursor.execute("""
                        INSERT INTO seguimiento (qr_id, registro_id, estacion, fecha)
                        VALUES (%s,%s,%s,NOW())
                    """, (qr_id, registro_id, estacion_a_registrar))
                    conn.commit()
                    mensaje = f"✅ Estación '{estacion_a_registrar}' registrada correctamente."

            # Historial del registro
            cursor.execute("""
                SELECT estacion, fecha FROM seguimiento
                WHERE registro_id=%s ORDER BY fecha
            """, (registro_id,))
            historial = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template(
        "seguimiento.html",
        qr_id=qr_id,
        mensaje=mensaje,
        datos_qr=datos_qr,
        historial=historial
    )

####################### Activos ###################
@app.route("/activos", methods=["GET", "POST"])
@login_requerido
def activos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        finalizar_id = request.form.get("finalizar_id")
        if finalizar_id:
            # Marcar como SALIDA en seguimiento y actualizar activo del registro
            cursor.execute("""
                INSERT INTO seguimiento (qr_id, registro_id, estacion, fecha)
                SELECT qr_id, id, 'SALIDA', NOW()
                FROM registros WHERE id=%s
            """, (finalizar_id,))
            cursor.execute("UPDATE registros SET activo=0 WHERE id=%s", (finalizar_id,))
            conn.commit()
            flash("Registro finalizado correctamente", "success")
            return redirect(url_for("activos"))

    # Obtener registros activos
    cursor.execute("SELECT * FROM registros WHERE activo=1 ORDER BY fecha DESC")
    registros = cursor.fetchall()

    activos_list = []
    for r in registros:
        cursor.execute("""
            SELECT estacion, fecha FROM seguimiento
            WHERE registro_id=%s ORDER BY fecha
        """, (r['id'],))
        historial = cursor.fetchall()
        ultima_estacion = historial[-1]['estacion'] if historial else r.get('estacion')
        fecha_ultima = historial[-1]['fecha'] if historial else r['fecha']
        duracion = datetime.strptime(str(fecha_ultima), "%Y-%m-%d %H:%M:%S") - datetime.strptime(str(r['fecha']), "%Y-%m-%d %H:%M:%S")
        activos_list.append({
            **r,
            "primera_estacion": r.get("estacion", "No definido"),
            "ultima_estacion": ultima_estacion,
            "fecha_ultima": fecha_ultima,
            "duracion": str(duracion),
            "historial": historial
        })

    cursor.close()
    conn.close()
    return render_template("activos.html", activos=activos_list)

####################### Ver QR ###################
@app.route("/ver_qr", methods=["GET", "POST"])
@login_requerido
def ver_qr():
    filtro_valor = ""
    fecha_inicio = ""
    fecha_fin = ""
    params = []

    # 👉 Exportar PDF por registro (recomendado)
    registro_id_pdf = request.args.get("exportar_pdf_id")
    if registro_id_pdf:
        return exportar_pdf_por_registro(registro_id_pdf)

    # (Opcional legado) Exportar PDF por qr_id (si aún usas ese link)
    qr_id_pdf = request.args.get("exportar_pdf")
    if qr_id_pdf:
        return exportar_pdf(qr_id_pdf)

    query = """
        SELECT r.id AS registro_id, r.qr_id, r.folio, r.chofer, r.empresa,
               r.estacion, r.fecha,
               MIN(s.fecha) AS entrada,
               MAX(s.fecha) AS salida
        FROM registros r
        LEFT JOIN seguimiento s ON s.registro_id = r.id
        WHERE 1=1
    """

    if request.method == "POST":
        filtro_valor = request.form.get("filtro", "").strip()
        fecha_inicio = request.form.get("fecha_inicio", "")
        fecha_fin = request.form.get("fecha_fin", "")

        if filtro_valor:
            query += " AND (r.qr_id LIKE %s OR r.folio LIKE %s OR r.chofer LIKE %s OR r.empresa LIKE %s)"
            like = f"%{filtro_valor}%"
            params.extend([like, like, like, like])

        if fecha_inicio:
            query += " AND r.fecha >= %s"
            params.append(fecha_inicio)

        if fecha_fin:
            query += " AND r.fecha <= %s"
            params.append(fecha_fin)

    query += """
        GROUP BY r.id, r.qr_id, r.folio, r.chofer, r.empresa, r.estacion, r.fecha
        ORDER BY r.fecha DESC
    """

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    resultados = []
    for r in rows:
        tiempo_dentro = None
        if r["entrada"] and r["salida"]:
            entrada_dt = r["entrada"]
            salida_dt = r["salida"]
            if isinstance(entrada_dt, str):
                entrada_dt = datetime.strptime(entrada_dt, "%Y-%m-%d %H:%M:%S")
            if isinstance(salida_dt, str):
                salida_dt = datetime.strptime(salida_dt, "%Y-%m-%d %H:%M:%S")
            tiempo_dentro = salida_dt - entrada_dt

        resultados.append({
            "registro_id": r["registro_id"],
            "qr_id": r["qr_id"],
            "folio": r["folio"],
            "chofer": r["chofer"],
            "empresa": r["empresa"],
            "estacion": r["estacion"],
            "fecha": r["fecha"],
            "tiempo_dentro": str(tiempo_dentro) if tiempo_dentro else None
        })

    historial = {}
    for r in resultados:
        cursor.execute(
            "SELECT estacion, fecha FROM seguimiento WHERE registro_id = %s ORDER BY fecha",
            (r["registro_id"],)
        )
        historial[r["registro_id"]] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "ver_qr.html",
        resultados=resultados,
        historial=historial,
        filtro_valor=filtro_valor,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

####################### Exportar PDF por registro ###################
def exportar_pdf_por_registro(registro_id):
    """Exporta el historial SOLO del registro indicado (evita mezclar usos del mismo QR)."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Datos del registro
    cursor.execute("SELECT * FROM registros WHERE id = %s", (registro_id,))
    datos = cursor.fetchone()
    if not datos:
        cursor.close()
        conn.close()
        return "Registro no encontrado", 404

    # Historial del registro
    cursor.execute(
        "SELECT estacion, fecha FROM seguimiento WHERE registro_id = %s ORDER BY fecha",
        (registro_id,)
    )
    historial_pdf = cursor.fetchall()

    # Construir PDF
    pdf = FPDF()
    pdf.add_page()

    # Registrar fuente Arial instalada en Ubuntu
    pdf.add_font('Arial', '', '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', uni=True)

    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Historial del Registro #{registro_id} (QR {datos['qr_id']})", ln=True, align="C")
    pdf.ln(10)

    # Datos del registro
    pdf.set_font("Arial", '', 12)
    campos = ["id", "qr_id", "folio", "chofer", "licencia", "empresa", "tipo_carga", "estacion", "fecha", "activo"]
    for key in campos:
        if key in datos:
            pdf.cell(0, 8, f"{key.capitalize()}: {datos[key]}", ln=True)

    # Tiempo dentro
    if historial_pdf:
        entrada = historial_pdf[0]['fecha']
        salida = historial_pdf[-1]['fecha']
        if isinstance(entrada, str):
            entrada = datetime.strptime(entrada, "%Y-%m-%d %H:%M:%S")
        if isinstance(salida, str):
            salida = datetime.strptime(salida, "%Y-%m-%d %H:%M:%S")
        tiempo_dentro = salida - entrada
        pdf.cell(0, 8, f"Tiempo dentro: {tiempo_dentro}", ln=True)
    else:
        pdf.cell(0, 8, "Tiempo dentro: N/A", ln=True)
    pdf.ln(5)

    # Historial de estaciones
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Historial de estaciones:", ln=True)
    pdf.set_font("Arial", '', 12)
    if historial_pdf:
        for h in historial_pdf:
            pdf.cell(0, 8, f"{h['fecha']} - {h['estacion']}", ln=True)
    else:
        pdf.cell(0, 8, "No hay historial", ln=True)

    # Generar PDF en memoria
    pdf_bytes = pdf.output(dest='S').encode('latin1')  # convertir a bytes
    pdf_buffer = io.BytesIO(pdf_bytes)

    cursor.close()
    conn.close()

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"registro_{registro_id}_historial.pdf",
        mimetype='application/pdf'
    )

####################### Login de entrada ###################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (usuario,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user["password"] == contrasena:
            session["usuario"] = user["username"]
            session["rol"] = user["rol"]
            session["estacion"] = user["estacion_asignada"]

            if user["rol"] in ["admin", "supervisor"]:
                return redirect(url_for("dashboard"))  # admin y supervisor van al dashboard
            else:
                return redirect(url_for("menu"))
        else:
            flash("Credenciales incorrectas", "error")

    return render_template("login/login.html")

####################### Cerrar sesión ###################
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

####################### Admin ###################
@app.route("/admin", methods=["GET", "POST"])
@solo_admin
def admin():
    mensaje = ""

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "crear":
            usuario = request.form["usuario"]
            contrasena = request.form["contrasena"]
            rol = request.form["rol"]
            estacion = request.form.get("estacion")

            try:
                cursor.execute(
                    "INSERT INTO usuarios (username, password, rol, estacion_asignada) VALUES (%s, %s, %s, %s)",
                    (usuario, contrasena, rol, estacion if estacion else None),
                )
                conn.commit()
                mensaje = "Usuario creado correctamente"
            except Exception as e:
                mensaje = f"Error al crear usuario: {str(e)}"

        elif accion == "reset":
            usuario_reset = request.form["usuario_reset"]
            nueva_contrasena = request.form["nueva_contrasena"]

            cursor.execute(
                "UPDATE usuarios SET password = %s WHERE username = %s",
                (nueva_contrasena, usuario_reset),
            )
            conn.commit()
            mensaje = f"Contraseña actualizada para el usuario '{usuario_reset}'"

        elif accion == "eliminar":
            usuario_eliminar = request.form["usuario_eliminar"]
            # Evitar que se borre a un admin actual logueado (opcional)
            if usuario_eliminar == session.get("username"):
                mensaje = "No puedes eliminar tu propio usuario mientras estás logueado."
            else:
                cursor.execute(
                    "DELETE FROM usuarios WHERE username = %s",
                    (usuario_eliminar,),
                )
                conn.commit()
                mensaje = f"Usuario '{usuario_eliminar}' eliminado correctamente"

    # Recuperar todos los usuarios para mostrarlos en la tabla
    cursor.execute("SELECT username, rol, estacion_asignada FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("login/admin.html", mensaje=mensaje, usuarios=usuarios)

####################### Botón para descargar el PowerPoint ###################
@app.route("/descargar_qrn")
def descargar_qrn():
    try:
        # Ruta absoluta del archivo en la raíz del proyecto
        ruta = os.path.join(os.path.dirname(__file__), "QRN.pptx")

        # Verificar que el archivo exista
        if not os.path.exists(ruta):
            print("Archivo no encontrado:", ruta)
            abort(404)

        # Enviar el archivo al navegador como descarga
        return send_file(
            ruta,
            as_attachment=True,
            download_name="QRN.pptx",
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

    except Exception as e:
        print("Error al descargar:", e)
        abort(500)

#################### Dashboard #################

@app.route("/dashboard")
@admin_o_supervisor
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Panel superior
    cursor.execute("SELECT COUNT(*) AS total_qr_activos FROM registros WHERE activo = 1")
    total_qr_activos = cursor.fetchone()["total_qr_activos"]

    cursor.execute("SELECT COUNT(DISTINCT chofer) AS total_choferes FROM registros WHERE activo = 1")
    total_choferes = cursor.fetchone()["total_choferes"]

    cursor.execute("SELECT COUNT(*) AS total_vetados FROM choferes_prohibidos")
    total_vetados = cursor.fetchone()["total_vetados"]

    # Últimos ingresos
    cursor.execute("""
        SELECT chofer, qr_id, empresa, estacion, fecha 
        FROM registros 
        ORDER BY fecha DESC 
        LIMIT 10
    """)
    ultimos_ingresos = cursor.fetchall()

    # Datos para gráfico: Choferes por última estación (solo activos)
    cursor.execute("""
        SELECT ultima.estacion, COUNT(*) AS cantidad
        FROM (
            SELECT r.id,
                   COALESCE(
                       (SELECT s.estacion 
                        FROM seguimiento s 
                        WHERE s.registro_id = r.id 
                        ORDER BY s.fecha DESC LIMIT 1),
                       r.estacion
                   ) AS estacion
            FROM registros r
            WHERE r.activo = 1
        ) AS ultima
        GROUP BY ultima.estacion
    """)
    resultados_estaciones = cursor.fetchall()
    labels_estaciones = [r["estacion"] for r in resultados_estaciones]
    data_estaciones = [r["cantidad"] for r in resultados_estaciones]

    # Datos para gráfico: % Choferes por empresa (solo activos)
    cursor.execute("""
        SELECT empresa, COUNT(*) AS cantidad
        FROM registros
        WHERE activo = 1
        GROUP BY empresa
    """)
    resultados_empresas = cursor.fetchall()
    labels_empresas = [r["empresa"] for r in resultados_empresas]
    data_empresas = [r["cantidad"] for r in resultados_empresas]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_qr_activos=total_qr_activos,
        total_choferes=total_choferes,
        total_vetados=total_vetados,
        ultimos_ingresos=ultimos_ingresos,
        labels_estaciones=labels_estaciones,
        data_estaciones=data_estaciones,
        labels_empresas=labels_empresas,
        data_empresas=data_empresas
    )

####################### Ejecutar aplicación ###################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)