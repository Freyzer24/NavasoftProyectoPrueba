import re
import smtplib
import base64
import jwt
from flask import jsonify
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'super_secret_key' 

# Configuración de la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://practicantes:Ora$sys1@u1268360.onlinehome-server.com/navasoftsoluciones'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Proyecto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    encargado = db.Column(db.String(100), nullable=False)

    def __init__(self, nombre, encargado):
        self.nombre = nombre
        self.encargado = encargado


class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    proyecto = db.Column(db.String(100), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    encargado = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    def __init__(self, nombre, proyecto, fecha_inicio, fecha_fin, encargado, estado):



        self.nombre = nombre
        self.proyecto = proyecto
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.encargado = encargado
        self.estado = estado



class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=True)  # Columna para la imagen en binario

    def __repr__(self):
        return f'<Registro {self.nombre}>'

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

def obtener_rol_desde_token():
    token = request.cookies.get('token')
    if not token:
        return None
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token.get("rol")
    except jwt.ExpiredSignatureError:
        flash("La sesión ha expirado, por favor inicia sesión nuevamente.")
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        flash("Token inválido, por favor inicia sesión nuevamente.")
        return redirect(url_for('login'))
    
def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.cookies.get('token')  # Obtiene el token de la cookie

        if not token:
            return jsonify({"mensaje": "Token es necesario"}), 403

        # Verifica si el token ha sido revocado
        if TokenRevocado.query.filter_by(token=token).first():
            return jsonify({"mensaje": "Token revocado. Debes iniciar sesión nuevamente."}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['usuario']
        except jwt.ExpiredSignatureError:
            return jsonify({"mensaje": "El token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"mensaje": "Token inválido"}), 403

        return f(current_user, *args, **kwargs)
    
    return decorador

@app.route('/subir_imagen', methods=['POST'])
def subir_imagen():
    if 'imagen' not in request.files:
        return 'No se ha subido ninguna imagen', 400

    imagen = request.files['imagen']
    if imagen.filename != '':
        img_data = imagen.read()  # Leer la imagen como datos binarios
        registro = Registro(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            correo=request.form['correo'],
            usuario=request.form['usuario'],
            rol=request.form['rol'],
            password=request.form['password'],
            imagen=img_data  # Guardar los datos binarios de la imagen
        )
        db.session.add(registro)
        db.session.commit()

    return 'Imagen subida con éxito', 200   
    
#Pantalla que se muestra con /
@app.route('/')
def index():
    return render_template('login.html')


SECRET_KEY = "tu_clave_secreta"  # Cámbiala por una clave segura

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario'].strip()
    password = request.form['password'].strip()

    # Verifica si el usuario existe en la base de datos
    registro = Registro.query.filter_by(usuario=usuario).first()
    
    if registro:
        is_correct = check_password_hash(registro.password, password)
        
        if is_correct:
            # Genera el token con una expiración de 1 hora
            token = jwt.encode(
                {
                    "usuario": registro.usuario,
                    "correo": registro.correo,
                    "rol": registro.rol,
                    "exp": datetime.utcnow() + timedelta(hours=1)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            # Crear la respuesta de inicio de sesión
            response = make_response(redirect(url_for('menuAdmin') if registro.rol in ['administrador', 'super_administrador'] else url_for('menuEmpleado')))
            response.set_cookie('token', token, httponly=True)  # Configura el token como una cookie segura y accesible solo por el servidor (httponly)
            
            flash('Inicio de sesión exitoso')
            return response
        else:
            flash('Contraseña incorrecta. Por favor, inténtalo de nuevo.')
    else:
        flash('Usuario no encontrado. Verifica tus datos e intenta de nuevo.')

    return redirect(url_for('index'))


class TokenRevocado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    fecha_revocacion = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/agregartareas")
@token_requerido
def agregartareas(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('agregarTareas.html')
@app.route("/Gantt/<string:nombre_proyecto>")
def Gantt(nombre_proyecto):
    # tu código aquí
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    
    tareas = Tarea.query.filter_by(proyecto=nombre_proyecto).all()
    encargados = Registro.query.all()
    encargados_dict = {encargado.nombre: encargado.nombre for encargado in encargados}
    proyectos = Proyecto.query.all()
    proyectos_dict = {proyecto.nombre: proyecto.id for proyecto in proyectos}

    return render_template(
        'Diagrama de Gantt.html', 
        tareas=tareas, 
        encargados_dict=encargados_dict,
        proyectos_dict=proyectos_dict,
        proyecto_id=nombre_proyecto,
        rol=rol
    )


@app.route("/tareas/<string:nombre_proyecto>")
@token_requerido
def obtener_tareas_por_proyecto(current_user, nombre_proyecto):
    # Filtra las tareas según el nombre del proyecto
    tareas = Tarea.query.filter_by(proyecto=nombre_proyecto).all()
    
    # Convierte las tareas a JSON
    tareas_json = [
        {
            'nombre': tarea.nombre,
            'fecha_inicio': tarea.fecha_inicio.strftime('%Y-%m-%d'),
            'fecha_fin': tarea.fecha_fin.strftime('%Y-%m-%d'),
            'encargado': tarea.encargado,
            'estado': tarea.estado,
            'proyecto': tarea.proyecto  # Asegúrate de que esté presente para el filtrado en JS
        }
        for tarea in tareas
    ]
    
    return jsonify(tareas_json)




    
@app.route('/menuAdmin')
@token_requerido
def menuAdmin(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('indexadmin.html')
@app.route('/admin')
@token_requerido
def Admin(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('menuAdmin.html')
@app.route('/Empleado')
@token_requerido
def Empleado(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('menuEmpleado.html')
@app.route('/Gtareas')#Gestión tareas
@token_requerido
def Gtareas(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    tareas = Tarea.query.all()
    return render_template('Gestióntareas.html', tareas=tareas, rol=rol)

@app.route('/menuEmpleado')
@token_requerido
def menuEmpleado(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('indexempleado.html')  # Asegúrate de tener esta plantilla creada
@app.route('/templeado')
@token_requerido
def templeado(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('templeado.html')
@app.route('/nuevo_usuario')
@token_requerido
def nuevo_usuario(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    return render_template('index.html')
import base64

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    # Obtener el token de la cookie
    token = request.cookies.get('token')

    if not token:
        flash('Debes iniciar sesión primero.')
        return redirect(url_for('login'))  # Redirige a login si no hay token

    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Extraer el nombre de usuario desde el token
        usuario = payload.get('usuario')

        # Buscar el registro del usuario en la base de datos
        registro = Registro.query.filter_by(usuario=usuario).first()

        if not registro:
            flash('Usuario no encontrado.')
            return redirect(url_for('login'))

        # Convertir la imagen binaria a base64 si existe
        imagen_base64 = None
        if registro.imagen:
            imagen_base64 = base64.b64encode(registro.imagen).decode('utf-8')

        # Preparar los datos del usuario para la plantilla
        datos_usuario = {
            'usuario': registro.usuario,
            'correo': registro.correo,
            'rol': registro.rol,
            'imagen': imagen_base64  # Imagen en base64 para mostrar en HTML
        }
    except jwt.ExpiredSignatureError:
        flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.')
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        flash('Token inválido. Por favor, inicia sesión nuevamente.')
        return redirect(url_for('login'))

    return render_template('Perfil.html', datos=datos_usuario)

@app.route('/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    # Obtener datos del formulario
    usuario = request.form.get('usuario')
    contrasena_actual = request.form['contrasena_actual']
    nueva_contrasena = request.form['nueva_contrasena']
    confirmar_contrasena = request.form['confirmar_contrasena']

    # Buscar al usuario en la base de datos
    usuario = Registro.query.filter_by(usuario=usuario).first()
    if not usuario:
        flash('Usuario no encontrado.')
        return redirect(url_for('perfil'))

    # Verificar la contraseña actual
    if not check_password_hash(usuario.password, contrasena_actual):
        flash('La contraseña actual es incorrecta.')
        return redirect(url_for('perfil'))

    # Validar la nueva contraseña
    if nueva_contrasena != confirmar_contrasena:
        flash('Las contraseñas no coinciden.')
        return redirect(url_for('perfil'))
    if not validar_contrasena(nueva_contrasena):
        flash('La nueva contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.')
        return redirect(url_for('perfil'))

    # Encriptar y actualizar la nueva contraseña
    usuario.password = generate_password_hash(nueva_contrasena)
    db.session.commit()

    flash('Contraseña actualizada con éxito.')
    return redirect(url_for('perfil'))

@app.route('/editar_tarea/<int:id>', methods=['GET', 'POST'])
def editar_tarea(id):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))

    tarea = Tarea.query.get_or_404(id)
    proyectos = Proyecto.query.all()

    if request.method == 'GET':
        encargados = Registro.query.all()
        return render_template('editar_tarea.html', tarea=tarea, encargados=encargados, rol=rol, proyectos=proyectos)

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        proyecto_id = request.form['proyecto']
        encargado_id = request.form['encargado']
        estado = request.form['estado']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        # Actualizar tarea
        tarea.nombre = nombre
        tarea.proyecto_id = proyecto_id
        tarea.encargado_id = encargado_id
        tarea.estado = estado
        tarea.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        tarea.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        # Guardar en la base de datos
        try:
            db.session.commit()
            flash('Tarea actualizada exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            print("Error al guardar en la base de datos:", e)
            flash('Ocurrió un error al actualizar la tarea.', 'danger')

        return redirect(url_for('Gtareas'))


@app.route('/cambiarfoto', methods=['POST'])
def cambiarfoto():
    # Obtener el token de la cookie
    token = request.cookies.get('token')

    if not token:
        flash('Debes iniciar sesión primero.')
        return redirect(url_for('login'))  # Redirige a login si no hay token

    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Extraer el nombre de usuario desde el token
        usuario = payload.get('usuario')

        # Buscar el registro del usuario en la base de datos
        registro = Registro.query.filter_by(usuario=usuario).first()

        if not registro:
            flash('Usuario no encontrado.')
            return redirect(url_for('login'))

        # Verificar si se subió una nueva imagen
        if 'foto' in request.files:
            foto = request.files['foto']
            if foto:
                # Validar que el archivo sea una imagen (por extensión)
                filename = foto.filename
                if filename.lower().endswith(('png', 'jpg', 'jpeg')):
                    # Leer el archivo de la imagen y almacenarlo en la base de datos
                    img_bytes = foto.read()
                    registro.imagen = img_bytes
                    db.session.commit()  # Guardar los cambios en la base de datos
                    flash('Imagen de perfil actualizada con éxito.')
                    # Convertir la imagen a base64 para mostrarla inmediatamente
                    imagen_base64 = base64.b64encode(img_bytes).decode('utf-8')
                    return redirect(url_for('perfil'))  # Redirigir al perfil para mostrar la imagen actualizada

        flash('No se ha seleccionado ninguna imagen.')
        return redirect(url_for('perfil'))  # Si no hay imagen seleccionada

    except jwt.ExpiredSignatureError:
        flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente.')
        return redirect(url_for('login'))
    except jwt.InvalidTokenError:
        flash('Token inválido. Por favor, inicia sesión nuevamente.')
        return redirect(url_for('login'))



@app.route('/eliminar_tarea/<int:id>', methods=['POST'])
def eliminar_tarea(id):
        tarea = Tarea.query.get(id)
        if tarea:
            db.session.delete(tarea)
            db.session.commit()
            flash('Tarea eliminada exitosamente.')
        else:
            flash('Tarea no encontrada.')
    
        return redirect(url_for('Gtareas'))

@app.route('/tAdmin')
@token_requerido
def tAdmin(current_user):
    return render_template('tAdmin.html')
@app.route('/logout', methods=['POST'])
def logout():
    # Crear la respuesta de logout
    response = make_response(redirect(url_for('index')))
    response.set_cookie('token', '', expires=0)  # Borra la cookie configurando su expiración a 0

    flash("Has cerrado sesión correctamente.")
    return response


# Ruta para ver todos los proyectos
@app.route('/proyectos')
def proyectos():
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    proyectos = Proyecto.query.all()
    encargados_dict = {encargado.id: encargado.nombre for encargado in Registro.query.all()}
    proyectos_dict = {proyecto.id: proyecto.nombre for proyecto in proyectos}  # Diccionario de proyectos
    return render_template('proyectos.html', proyectos=proyectos, encargados_dict=encargados_dict, proyectos_dict=proyectos_dict,rol=rol)




# Ruta para agregar un nuevo proyecto
@app.route('/agregar_proyecto', methods=['POST'])
def agregar_proyecto():
    # Verifica si el usuario tiene el rol de 'super_administrador' o 'administrador'
        nombre = request.form['nombre']
        encargado = request.form['encargado']
        
        nuevo_proyecto = Proyecto(nombre=nombre, encargado=encargado)
        db.session.add(nuevo_proyecto)
        db.session.commit()
        
        flash('Proyecto agregado exitosamente.')
        return redirect(url_for('proyectos'))


# Ruta para eliminar un proyecto
from flask import flash, redirect, url_for, session

@app.route('/eliminar_proyecto/<int:id>', methods=['POST'])
def eliminar_proyecto(id):
    # Verifica si el usuario tiene el rol de 'super_administrador'
  
        proyecto = Proyecto.query.get(id)
        if proyecto:
            db.session.delete(proyecto)
            db.session.commit()
            flash('Proyecto eliminado correctamente.', 'success')
        else:
            flash('Proyecto no encontrado.', 'error')

        return redirect(url_for('proyectos'))

@app.route('/editar_proyecto/<int:id>', methods=['GET'])
def editar_proyecto(id):
        proyecto = Proyecto.query.get(id)
        
        if proyecto:
            encargados = Registro.query.all()  # Obtener todos los encargados
            return render_template('editar_proyecto.html', proyecto=proyecto, encargados=encargados)
        else:
            flash('Proyecto no encontrado.', 'error')  # Mensaje único de error si el proyecto no se encuentra
            return redirect(url_for('proyectos'))  # Redirigir a la vista de proyectos si no se encuentra el proyecto
    

# Ruta para actualizar un proyecto
@app.route('/actualizar_proyecto/<int:id>', methods=['POST'])
def actualizar_proyecto(id):
    # Verifica si el usuario tiene el rol de 'super_administrador' o 'administrador'
   
        proyecto = Proyecto.query.get(id)
        if proyecto:
            proyecto.nombre = request.form['nombre']
            encargado_id = request.form['encargado']

            # Si se selecciona un encargado, actualizar el ID del encargado
            if encargado_id:
                encargado = Registro.query.get(encargado_id)
                if encargado:
                    proyecto.encargado = encargado.id  # Guardamos el ID del encargado, no el nombre
                else:
                    flash('El encargado seleccionado no existe.')
                    return redirect(url_for('editar_proyecto', id=id))

            db.session.commit()
            flash('Proyecto actualizado correctamente.')
        else:
            flash('Proyecto no encontrado.')

        return redirect(url_for('proyectos'))



def enviar_confirmacion_correo(nombre, usuario, correo):
    remitente = "valeriapaolap49@gmail.com"
    contraseña = "syjq cptv tlus wbcp"  # Sustitúyela con la contraseña de aplicación de Gmail
    destinatario = correo

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = "Confirmación de creación de usuario"

    # Cuerpo del mensaje en HTML
    cuerpo_html = f"""
    <html>
        <body>
             <p style="font-size: 16px;">Hola <strong>{nombre}</strong>,</p>
            <p style="font-size: 14px;">Hemos creado exitosamente tu usuario llamado <strong>{usuario}</strong>.</p>
            <p style="font-size: 14px;">Tu contraseña temporal es: <strong>Navasoft$0</strong></p>
            <p style="font-size: 14px;">Saludos cordiales,<br>El equipo de Navasoft</p>
            <br>
            <img src="https://media.licdn.com/dms/image/v2/D4E3DAQFAB3gn_AzD1Q/image-scale_191_1128/image-scale_191_1128/0/1710221899179/navasoft_soluciones_cover?e=2147483647&v=beta&t=avESRYqDr4FPJ0PfXGRQwhO1mOgBzUEEIrpu55nCJck" alt="Navasoft Logo" style="width:900px;height:auto;">
        </body>
    </html>
    """
    mensaje.attach(MIMEText(cuerpo_html, 'html'))


    # Envío del correo
    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, mensaje.as_string())
        servidor.quit()  # Cierra la conexión de forma segura
        print("Correo de confirmación enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

#mostrar
@app.route('/mostrar')
@token_requerido
def mostrar(current_user):
    rol = obtener_rol_desde_token()
    if rol is None:
        return redirect(url_for('login'))
    registros = Registro.query.all()
    return render_template('Mostrar.html', registros=registros, rol=rol)

def validar_contrasena(contrasena):
    if (len(contrasena) < 8 or 
        not re.search(r"[A-Z]", contrasena) or
        not re.search(r"[a-z]", contrasena) or
        not re.search(r"[0-9]", contrasena) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena)):
        return False
    return True
    
# Ruta para agregar un nuevo registro

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    usuario = request.form['usuario']
    rol = request.form['rol']
    password = request.form['password'] or 'Navasoft$0'

    # Validar la contraseña
    if password != 'Navasoft$0' and not validar_contrasena(password):
        flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.')
        return redirect(url_for('nuevo_usuario'))

    # Verificar si el usuario ya existe
    usuario_existente = Registro.query.filter_by(usuario=usuario).first()
    if usuario_existente:
        flash('El nombre de usuario ya existe. Por favor, elige otro.')
        return redirect(url_for('nuevo_usuario'))

    # Hashear la contraseña antes de guardarla
    hashed_password = generate_password_hash(password)

    # Leer el archivo de imagen en formato binario
    imagen = request.files['imagen']
    imagen_binaria = None
    if imagen:
        imagen_binaria = imagen.read()  # Lee el archivo y guarda su contenido binario

    # Crear el nuevo registro
    nuevo_registro = Registro(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        usuario=usuario,
        rol=rol,
        password=hashed_password,
        imagen=imagen_binaria  # Guarda el contenido binario de la imagen
    )

    db.session.add(nuevo_registro)
    db.session.commit()

    # Enviar el correo de confirmación
    enviar_confirmacion_correo(nombre, usuario, correo)

    flash('Registro guardado con éxito')
    return redirect(url_for('mostrar'))


# Nueva ruta para obtener detalles del usuario
@app.route('/detalles_usuario/<int:id>')
def detalles_usuario(id):
    registro = Registro.query.get_or_404(id)
    return render_template('detalles_modal.html', registro=registro)
# Ruta para editar un registro
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    registro = Registro.query.get_or_404(id)  # Obtiene el registro o devuelve un error 404

    if request.method == 'POST':
        # Manejar la presentación del formulario
        registro.nombre = request.form['nombre']
        registro.telefono = request.form['telefono']
        registro.correo = request.form['correo']
        registro.usuario = request.form['usuario']
        registro.rol = request.form['rol']
        password = request.form['password']

        # Si se proporciona una nueva contraseña, se actualiza el hash
        if password:
            registro.password = generate_password_hash(password)  # Hashea la nueva contraseña
        
        # Manejar la imagen
        imagen = request.files.get('imagen')
        if imagen:
            registro.imagen = imagen.read()  # Guardar la imagen como binario en la base de datos

        db.session.commit()  # Guarda los cambios en la base de datos

        flash('Registro actualizado con éxito')
        return redirect(url_for('mostrar'))  # Redirigir a la vista de mostrar registros

    # Manejar la solicitud GET para mostrar el formulario
    return render_template('editar.html', registro=registro)  # Asegúrate de tener esta plantilla


# Ruta para eliminar un registro
@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    # Buscar el registro por ID
    registro = Registro.query.get_or_404(id)

    # Actualizar los proyectos asociados a este registro
    proyectos = Proyecto.query.filter_by(encargado=id).all()
    for proyecto in proyectos:
        proyecto.encargado = None  # o algún valor que indique que no tiene encargado

    # Eliminar el registro de la tabla `registro`
    db.session.delete(registro)
    db.session.commit()

    # Mensaje de éxito
    flash('Registro eliminado con éxito', 'success')

    # Redirigir a la vista principal
    return redirect(url_for('mostrar'))



# Ruta para mostrar una lista de usuarios específicos
@app.route('/usuarios')
def lista_usuarios():
    registros = Registro.query.with_entities(Registro.nombre, Registro.rol, Registro.telefono).all()
    return render_template('usuarios.html', usuarios=registros)

@app.route('/guardar_tarea', methods=['POST'])
def guardar_tarea():

    
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    proyecto = request.form['proyecto']
    fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
    fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()
    encargado = request.form['encargado']
    estado = request.form['estado']
    
    # Crear una nueva instancia de Tarea
    nueva_tarea = Tarea(
        nombre=nombre,
        proyecto=proyecto,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        encargado=encargado,
        estado=estado
    )
    
    # Guardar la nueva tarea en la base de datos
    db.session.add(nueva_tarea)
    db.session.commit()
    
    flash('Tarea registrada exitosamente.')
    return redirect(url_for('Gantt'))
@app.route('/tareas')
def obtener_tareas():
    tareas = Tarea.query.all()
    tareas_json = [
        {
            "id": tarea.id,
            "nombre": tarea.nombre,
            "proyecto": tarea.proyecto,
            "fecha_inicio": tarea.fecha_inicio.strftime("%Y-%m-%d"),
            "fecha_fin": tarea.fecha_fin.strftime("%Y-%m-%d"),
            "encargado": tarea.encargado,
            "estado": tarea.estado
        }
        for tarea in tareas
    ]
    return jsonify(tareas_json)
if __name__ == '__main__':
    app.run(debug=True)
    
# Definir el color de la barra basado en el porcentaje
def obtener_color_barra(porcentaje):
    if porcentaje == 100:
        return 'blue'
    elif porcentaje >= 65:
        return 'green'
    elif porcentaje >= 34:
        return 'yellow'
    else:
        return 'red'
