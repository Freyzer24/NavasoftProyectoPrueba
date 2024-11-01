from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Cambia esto en producción

# Configuración de la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://practicantes:Ora$sys1@u1268360.onlinehome-server.com/navasoftsoluciones'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para los registros
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<Registro {self.nombre}>'

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('indexAdmin.html')

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

# Ruta para manejar el inicio de sesión
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

@app.route('/menuEmpleado')
def menuEmpleado():
    return render_template('indexempleado.html')  # Asegúrate de tener esta plantilla creada
@app.route('/Empleado')
def Empleado():
    return render_template('menuEmpleado.html')
@app.route('/templeado')
def templeado():
    return render_template('templeado.html')


# Ruta para agregar un nuevo registro
@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    usuario = request.form['usuario']
    rol = request.form['rol']
    password = request.form['password']

    # Validar la contraseña
    if not validar_contrasena(password):
        flash('La contraseña debe tener al menos 8 caracteres, una letra mayúscula, una letra minúscula y un número.')
        return redirect(url_for('nuevo_usuario'))  # Redirigir al formulario de nuevo usuario

    # Hash de la contraseña antes de guardarla
    hashed_password = generate_password_hash(password)
    print(f"Hash de la contraseña guardada: {hashed_password}")  # Verifica el hash

    nuevo_registro = Registro(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        usuario=usuario,
        rol=rol,
        password=hashed_password  # Guardamos la contraseña hasheada
    )

    db.session.add(nuevo_registro)
    db.session.commit()

    flash('Registro guardado con éxito')
    return redirect(url_for('mostrar'))

def validar_contrasena(contrasena):
    if (len(contrasena) < 8 or 
        not re.search(r"[A-Z]", contrasena) or  # Al menos una letra mayúscula
        not re.search(r"[a-z]", contrasena) or  # Al menos una letra minúscula
        not re.search(r"[0-9]", contrasena)):   # Al menos un número
        return False
    return True

# Rutas restantes
@app.route('/mostrar')
def mostrar():
    registros = Registro.query.all()
    return render_template('Mostrar.html', registros=registros)


@app.route('/nuevo_usuario')
def nuevo_usuario():
    return render_template('index.html')

# Ruta para editar un registro
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    registro = Registro.query.get_or_404(id)
    registro.nombre = request.form['nombre']
    registro.telefono = request.form['telefono']
    registro.correo = request.form['correo']
    registro.usuario = request.form['usuario']
    registro.rol = request.form['rol']
    registro.password = generate_password_hash(request.form['password'])  # Hash de la contraseña
    db.session.commit()

    flash('Registro actualizado con éxito')
    return redirect(url_for('index'))
@app.route('/perfil')
def perfil():
    # Aquí renderizas la página de perfil
    return render_template('perfil.html')

# Ruta para eliminar un registro
@app.route('/eliminar/<int:id>')
def eliminar(id):
    registro = Registro.query.get_or_404(id)
    db.session.delete(registro)
    db.session.commit()

    flash('Registro eliminado con éxito')
    return redirect(url_for('index'))

# Ruta para mostrar una lista de usuarios específicos
@app.route('/usuarios')
def lista_usuarios():
    registros = Registro.query.with_entities(Registro.nombre, Registro.rol, Registro.telefono).all()
    return render_template('usuarios.html', usuarios=registros)
@app.route('/tAdmin')
def tAdmin():
    return render_template('tAdmin.html')


if __name__ == '__main__':
    app.run(debug=True)
# 