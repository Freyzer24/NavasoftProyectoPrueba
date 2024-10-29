from flask import Flask, render_template, request, redirect, url_for, flash;
from flask_sqlalchemy import SQLAlchemy;

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
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Registro {self.nombre}>'

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Ruta para mostrar el formulario
@app.route('/')
def index():
    registros = Registro.query.all()
    return render_template('index.html', registros=registros)

# Ruta para agregar un nuevo registro
@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    correo = request.form['correo']
    usuario = request.form['usuario']
    rol = request.form['rol']
    password = request.form['password']

    nuevo_registro = Registro(nombre=nombre, telefono=telefono, correo=correo, usuario=usuario, rol=rol, password=password)
    db.session.add(nuevo_registro)
    db.session.commit()

    flash('Registro guardado con éxito')
    return redirect(url_for('index'))

# Ruta para editar un registro
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    registro = Registro.query.get_or_404(id)
    registro.nombre = request.form['nombre']
    registro.telefono = request.form['telefono']
    registro.correo = request.form['correo']
    registro.usuario = request.form['usuario']
    registro.rol = request.form['rol']
    registro.password = request.form['password']
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
@app.route('/usuarios')
def lista_usuarios():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT nombre, rol, telefono FROM registro")
    usuarios = cursor.fetchall()
    cursor.close()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
