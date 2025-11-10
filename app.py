from flask import Flask,render_template,request,redirect, session,url_for,flash
app = Flask(__name__)

app.secret_key = 'MelaNIE12345_pI'

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apeido = request.form['apeido']
        dia = request.form['dia']
        mes = request.form['mes']
        anio = request.form['anio']
        genero = request.form['genero']
        email = request.form['exampleInputEmail1']
        password = request.form['exampleInputPassword1']
        actividad = request.form['nivelactividad']
        peso = request.form['peso']
        altura = request.form['altura']
        
        flash(f'Registro exitoso ¡Bienvenido a Sabores y Saberes {nombre}!')
        return redirect(url_for('principal'))  
    
    return render_template('formulario.html')

@app.route('/')
def principal():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)