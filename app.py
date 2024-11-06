import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, flash, session
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
    
    
#Pantalla que se muestra con /
@app.route('/')
def index():
    return render_template('indexadmin.html')


@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario'].strip()
    password = request.form['password'].strip()

    # Verifica si el usuario existe en la base de datos
    registro = Registro.query.filter_by(usuario=usuario).first()
    
    if registro:
        print(f"Usuario encontrado: {registro.usuario}")  # Verifica el usuario
        is_correct = check_password_hash(registro.password, password)
        print(f"Contraseña correcta: {is_correct}")  # Imprime True si coincide

        if is_correct:
            # Guarda los datos del usuario en la sesión
            session['usuario'] = registro.usuario
            session['correo'] = registro.correo
            session['telefono'] = registro.telefono
            session['rol'] = registro.rol

            # Redirecciona dependiendo del rol
            if registro.rol in ['admin', 'super_administrador']:
                flash('Inicio de sesión exitoso - Admin')
                return redirect(url_for('menuAdmin'))
            else:
                flash('Inicio de sesión exitoso - Empleado')
                return redirect(url_for('menuEmpleado'))
        else:
            flash('Contraseña incorrecta. Por favor, inténtalo de nuevo.')
    else:
        flash('Usuario no encontrado. Verifica tus datos e intenta de nuevo.')

    return redirect(url_for('index'))




@app.route('/menuAdmin')
def menuAdmin():
    return render_template('indexadmin.html')
@app.route('/Admin')
def Admin():
    return render_template('menuAdmin.html')
@app.route('/Gtareas')#Gestión tareas
def Gtareas():
    return render_template('Gestióntareas.html')
@app.route('/DGantt')
def DGantt():
    return render_template('Diagrama de Gantt.html')
@app.route('/menuEmpleado')
def menuEmpleado():
    return render_template('indexempleado.html')  # Asegúrate de tener esta plantilla creada
@app.route('/Empleado')
def Empleado():
    return render_template('menuEmpleado.html')
@app.route('/templeado')
def templeado():
    return render_template('templeado.html')
@app.route('/nuevo_usuario')
def nuevo_usuario():
    return render_template('index.html')
@app.route('/perfil')
def perfil():
    # Verificar que el usuario esté autenticado
    if 'usuario' not in session:
        flash('Debes iniciar sesión primero.')
        return redirect(url_for('pe'))

    # Pasar los datos del usuario a la plantilla
    datos_usuario = {
        'usuario': session['usuario'],
        'correo': session['correo'],
        'telefono': session['telefono'],
        'rol': session['rol']
    }

    return render_template('perfil.html', datos=datos_usuario)
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

@app.route('/tAdmin')
def tAdmin():
    return render_template('tAdmin.html')
@app.route('/logout')  # Ruta para cerrar sesión
def logout():
    flash('Has cerrado sesión exitosamente.')
    return render_template('login.html')
# Ruta para ver todos los proyectos
@app.route('/proyectos')
def proyectos():
    proyectos = Proyecto.query.all()
    return render_template('proyectos.html', proyectos=proyectos)

# Ruta para agregar un nuevo proyecto
@app.route('/agregar_proyecto', methods=['POST'])
def agregar_proyecto():
    nombre = request.form['nombre']
    encargado = request.form['encargado']
    nuevo_proyecto = Proyecto(nombre=nombre, encargado=encargado)
    db.session.add(nuevo_proyecto)
    db.session.commit()
    flash('Proyecto agregado exitosamente.')
    return redirect(url_for('proyectos'))

# Ruta para eliminar un proyecto
@app.route('/eliminar_proyecto/<int:id>', methods=['POST'])
def eliminar_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if proyecto:
        db.session.delete(proyecto)
        db.session.commit()
        flash('Proyecto eliminado correctamente.')
    else:
        flash('Proyecto no encontrado.')
    return redirect(url_for('proyectos'))

@app.route('/editar_proyecto/<int:id>', methods=['GET'])
def editar_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if proyecto:
        return render_template('editar_proyecto.html', proyecto=proyecto)
    else:
        flash('Proyecto no encontrado.')
        return redirect(url_for('proyectos'))
@app.route('/actualizar_proyecto/<int:id>', methods=['POST'])
def actualizar_proyecto(id):
    proyecto = Proyecto.query.get(id)
    if proyecto:
        proyecto.nombre = request.form['nombre']
        proyecto.encargado = request.form['encargado']
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
def mostrar():
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
def eliminar_usuario(id):  # Cambia el nombre de la función aquí para evitar duplicados
    registro = Registro.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()

    flash('Registro eliminado con éxito')
    return redirect(url_for('mostrar'))

# Ruta para mostrar una lista de usuarios específicos
@app.route('/usuarios')
def lista_usuarios():
    registros = Registro.query.with_entities(Registro.nombre, Registro.rol, Registro.telefono).all()
    return render_template('usuarios.html', usuarios=registros)

if __name__ == '__main__':
    app.run(debug=True)
# 