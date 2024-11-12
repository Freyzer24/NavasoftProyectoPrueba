import re
import smtplib
import jwt
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
    encargado=db.Column(db.String(100),nullable=False)

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


# Modelo para los registros
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Registro {self.nombre}>'

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()
    
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
    return render_template('agregarTareas.html')
@app.route("/Gantt")
@token_requerido
def Gantt(current_user):
    return render_template('Diagrama de Gantt.html')
@app.route('/menuAdmin')
@token_requerido
def menuAdmin(current_user):
    return render_template('indexadmin.html')
@app.route('/admin')
def Admin():  # Nombre de la función en mayúscula
    return render_template('menuAdmin.html')
@app.route('/Empleado')
@token_requerido
def Empleado(current_user):
    return render_template('menuEmpleado.html')
@app.route('/Gtareas')#Gestión tareas
@token_requerido
def Gtareas(current_user):
    tareas = Tarea.query.all()
    return render_template('Gestióntareas.html', tareas=tareas)
@app.route('/DGantt')
@token_requerido
def DGantt(current_user):
    return render_template('Diagrama de Gantt.html')
@app.route('/menuEmpleado')
@token_requerido
def menuEmpleado(current_user):
    return render_template('indexempleado.html')  # Asegúrate de tener esta plantilla creada
@app.route('/templeado')
@token_requerido
def templeado(current_user):
    return render_template('templeado.html')
@app.route('/nuevo_usuario')
@token_requerido
def nuevo_usuario(current_user):
    return render_template('index.html')
@app.route('/perfil')
@token_requerido
def perfil(current_user):
    # Verificar que el usuario esté autenticado
    if 'usuario' not in session:
        flash('Debes iniciar sesión primero.')
        return redirect(url_for('login'))  # Redirige a la página de login si no está autenticado

    # Pasar los datos del usuario a la plantilla
    datos_usuario = {
        'usuario': session['usuario'],
        'correo': session['correo'],
        'telefono': session['telefono'],
        'rol': session['rol']
    }

    return render_template('Perfil.html', datos=datos_usuario)

@app.route('/cambiar_contrasena', methods=['POST'])
def cambiar_contrasena():
    # Verifica si el usuario ha iniciado sesión
    user_id = session.get('user_id')
    if not user_id:
        flash("Por favor, inicia sesión para cambiar tu contraseña.")
        return redirect(url_for('index'))

    # Obtiene la nueva contraseña del formulario
    nueva_contrasena = request.form.get('nueva_contrasena').strip()

    # Validaciones de la nueva contraseña (puedes ajustar según tus requisitos)
    if len(nueva_contrasena) < 8:
        flash("La nueva contraseña debe tener al menos 8 caracteres.")
        return redirect(url_for('perfil'))
    if not any(char.isdigit() for char in nueva_contrasena):
        flash("La nueva contraseña debe contener al menos un número.")
        return redirect(url_for('perfil'))
    if not any(char.isupper() for char in nueva_contrasena):
        flash("La nueva contraseña debe contener al menos una letra mayúscula.")
        return redirect(url_for('perfil'))
    if not any(char in "!@#$%^&*()-_+=" for char in nueva_contrasena):
        flash("La nueva contraseña debe contener al menos un carácter especial.")
        return redirect(url_for('perfil'))

    # Encripta la nueva contraseña
    nueva_contrasena_hash = generate_password_hash(nueva_contrasena)

    # Actualiza la contraseña en la base de datos
    usuario = Registro.query.get(user_id)
    usuario.password = nueva_contrasena_hash
    db.session.commit()

    flash("Contraseña actualizada exitosamente.")
    return redirect(url_for('perfil'))
@app.route('/editar_tarea/<int:id>', methods=['GET', 'POST'])
def editar_tarea(id):
    # Verifica si el usuario tiene el rol de 'visualizador'
    if 'rol' in session and session['rol'] == 'visualizador':
        flash('Acceso denegado: no tienes permisos para editar tareas.')
        return redirect(url_for('Gtareas'))  # Redirige a la página principal o de tareas

    # Obtener la tarea de la base de datos por su ID
    tarea = Tarea.query.get_or_404(id)

    if request.method == 'GET':
        # Mostrar el formulario con los datos de la tarea
        return render_template('editar_tarea.html', tarea=tarea)

    if request.method == 'POST':
        # Obtener los datos enviados desde el formulario
        nombre = request.form['nombre']
        proyecto = request.form['proyecto']
        encargado = request.form['encargado']
        estado = request.form['estado']

        # Actualizar los atributos de la tarea
        tarea.nombre = nombre
        tarea.proyecto = proyecto
        tarea.encargado = encargado
        tarea.estado = estado

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash('Tarea actualizada exitosamente', 'success')
        return redirect(url_for('Gtareas'))  # Redirigir a la página principal o donde desees

    return render_template('editar_tarea.html', tarea=tarea)


@app.route('/eliminar_tarea/<int:id>', methods=['POST'])
def eliminar_tarea(id):
    # Verifica si el usuario tiene el rol de 'super_administrador' o 'administrador'
    if 'rol' in session and session['rol'] in ['super_administrador', 'administrador']:
        tarea = Tarea.query.get(id)
        if tarea:
            db.session.delete(tarea)
            db.session.commit()
            flash('Tarea eliminada exitosamente.')
        else:
            flash('Tarea no encontrada.')
    else:
        flash('Acceso denegado: no tienes permisos para eliminar tareas.')
    
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
    proyectos = Proyecto.query.all()
    encargados_dict = {encargado.id: encargado.nombre for encargado in Registro.query.all()}
    return render_template('proyectos.html', proyectos=proyectos, encargados_dict=encargados_dict)


# Ruta para agregar un nuevo proyecto
@app.route('/agregar_proyecto', methods=['POST'])
def agregar_proyecto():
    # Verifica si el usuario tiene el rol de 'super_administrador' o 'administrador'
    if 'rol' in session and session['rol'] in ['super_administrador', 'administrador']:
        nombre = request.form['nombre']
        encargado = request.form['encargado']
        
        nuevo_proyecto = Proyecto(nombre=nombre, encargado=encargado)
        db.session.add(nuevo_proyecto)
        db.session.commit()
        
        flash('Proyecto agregado exitosamente.')
    else:
        flash('Acceso denegado: no tienes permisos para agregar proyectos.')
    
    return redirect(url_for('proyectos'))


# Ruta para eliminar un proyecto
from flask import flash, redirect, url_for, session

@app.route('/eliminar_proyecto/<int:id>', methods=['POST'])
def eliminar_proyecto(id):
    # Verifica si el usuario tiene el rol de 'super_administrador'
    if 'rol' in session and session['rol'] == 'super_administrador':
        proyecto = Proyecto.query.get(id)
        if proyecto:
            db.session.delete(proyecto)
            db.session.commit()
            flash('Proyecto eliminado correctamente.', 'success')
        else:
            flash('Proyecto no encontrado.', 'error')
    else:
        # Mensaje de acceso denegado si el usuario no es super administrador
        flash('Acceso denegado: solo los super administradores pueden eliminar proyectos.', 'error')

    return redirect(url_for('proyectos'))


# Ruta para actualizar un proyecto
@app.route('/actualizar_proyecto/<int:id>', methods=['POST'])
def actualizar_proyecto(id):
    # Verifica si el usuario tiene el rol de 'super_administrador' o 'administrador'
    if 'rol' in session and session['rol'] in ['super_administrador', 'administrador']:
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
    else:
        flash('Acceso denegado: no tienes permisos para actualizar proyectos.')

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
    registros = Registro.query.all()
    return render_template('Mostrar.html', registros=registros)

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
    password = request.form['password'] or 'Navasoft$0'  # Asigna la contraseña predeterminada si está vacía

    # Validar la contraseña
    if password != 'Navasoft$0' and not validar_contrasena(password):
        flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula, un número y un carácter especial.')
        return redirect(url_for('nuevo_usuario'))
    # Verificar si el usuario ya existe
    usuario_existente = Registro.query.filter_by(usuario=usuario).first()
    if usuario_existente:
        flash('El nombre de usuario ya existe. Por favor, elige otro.')
        return redirect(url_for('nuevo_usuario'))

    # Hash de la contraseña antes de guardarla
    hashed_password = generate_password_hash(password)
    print(f"Hash de la contraseña guardada: {hashed_password}")  # Verifica el hash

    nuevo_registro = Registro(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        usuario=usuario,
        rol=rol,
        password=hashed_password
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

        db.session.commit()  # Guarda los cambios en la base de datos

        flash('Registro actualizado con éxito')
        return redirect(url_for('mostrar'))  # Redirigir a la vista de mostrar registros
    else:
        # Manejar la solicitud GET para mostrar el formulario
        return render_template('editar.html', registro=registro)  # Asegúrate de tener esta plantilla

# Ruta para eliminar un registro
@app.route('/eliminar/<int:id>')
def eliminar_usuario(id):
    # Verifica si el usuario tiene el rol de 'super_administrador'
    if 'rol' in session and session['rol'] == 'super_administrador':
        registro = Registro.query.get_or_404(id)
        db.session.delete(registro)
        db.session.commit()
        flash('Registro eliminado con éxito', 'success')
    else:
        # Mensaje de acceso denegado si el usuario no es super administrador
        flash('Acceso denegado: solo los super administradores pueden eliminar usuarios.', 'error')

    return redirect(url_for('mostrar'))

# Ruta para mostrar una lista de usuarios específicos
@app.route('/usuarios')
def lista_usuarios():
    registros = Registro.query.with_entities(Registro.nombre, Registro.rol, Registro.telefono).all()
    return render_template('usuarios.html', usuarios=registros)

@app.route('/guardar_tarea', methods=['POST'])
def guardar_tarea():
    # Verifica si el usuario tiene el rol de 'visualizador'
    if 'rol' in session and session['rol'] == 'visualizador':
        flash('Acceso denegado: no tienes permisos para registrar nuevas tareas.')
        return redirect(url_for('proyectos'))  # Redirige a la página de proyectos o donde desees

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
    return redirect(url_for('proyectos'))


if __name__ == '__main__':
    app.run(debug=True)
# 