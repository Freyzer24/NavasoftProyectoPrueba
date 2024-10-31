from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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
    password = db.Column(db.String(128), nullable=False)  # Aumentado para el hash

    def __repr__(self):
        return f'<Registro {self.nombre}>'

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Ruta para mostrar la página de inicio con todos los registros
@app.route('/')
def index():
    return render_template('indexadmin.html')

@app.route('/tAdmin')
def tAdmin():
    return render_template('tAdmin.html')

@app.route('/menuAdmin')
def menuAdmin():
    return render_template('menuAdmin.html')

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']
    
    print(f'Usuario: {usuario}, Contraseña: {password}')  # Verifica que los datos se están recibiendo correctamente

    registro = Registro.query.filter_by(usuario=usuario).first()

    if registro and check_password_hash(registro.password, password):
        print('Inicio de sesión exitoso')  # Verifica que se pasa esta condición
        return redirect(url_for('menuAdmin'))
    else:
        print('Usuario o contraseña incorrectos')  # Verifica que se pasa esta condición
        flash('Usuario o contraseña incorrectos.')
        return redirect(url_for('index'))


# Ruta para agregar un nuevo registro
@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    usuario = request.form['usuario']
    rol = request.form['rol']
    password = request.form['password']

    nuevo_registro = Registro(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        usuario=usuario,
        rol=rol,
        password=generate_password_hash(password)  # Hash de la contraseña
    )
    db.session.add(nuevo_registro)
    db.session.commit()

    flash('Registro guardado con éxito')
    return redirect(url_for('mostrar'))  # Redirige a la vista de mostrar registros

# Ruta para mostrar todos los registros
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

if __name__ == '__main__':
    app.run(debug=True)
