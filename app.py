from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    nombre = request.form.get('nombre')
    mensaje = f"Hola, {nombre}! Gracias por enviar el formulario."
    return render_template('index.html', mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True)
