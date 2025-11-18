from flask import Flask, render_template, request, redirect, session, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'melyyyyaaasdwwd'

API_URL = 'https://api.spoonacular.com/recipes/complexSearch'
API_KEY = '923b514b2c604404954302eaebfea6fd'


usuarios = {}

@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':   
        nombre = request.form.get('nombre')
        apeido = request.form.get('apeido')
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        anio = request.form.get('anio')
        genero = request.form.get('genero')
        email = request.form.get('exampleInputEmail1')
        password = request.form.get('exampleInputPassword1')
        actividad = request.form.get('nivelactividad')
        peso = request.form.get('peso')
        altura = request.form.get('altura')

        if email in usuarios:
            flash("El correo ya está registrado, intenta iniciar sesión.")
            return redirect("/iniciar_sesion")

        usuarios[email] = {
            "nombre": nombre,
            "apeido": apeido,
            "fecha": f"{dia}/{mes}/{anio}",
            "genero": genero,
            "password": password,
            "actividad": actividad,
            "peso": peso,
            "altura": altura
        }

        session["usuario"] = email
        session["nombre"] = nombre

        flash(f"Registro exitoso ¡Bienvenido a Sabores y Saberes {nombre}!")
        return redirect("/perfil")

    return render_template('formulario.html')


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificamos que el usuario exista y la contraseña coincida
        if email in usuarios and usuarios[email]["password"] == password:
            session['usuario'] = email
            session['nombre'] = usuarios[email]["nombre"]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
            return redirect(url_for('iniciar_sesion'))

    return render_template("iniciar_sesion.html")


@app.route('/perfil')
def perfil():
    if not session.get("usuario"):
        flash("Debes iniciar sesión para acceder a tu perfil.")
        return redirect("/iniciar_sesion")
    
    email = session["usuario"]
    usuario = usuarios[email]

    return render_template('perfil.html', usuario=usuario)

@app.route('/buscar', methods=['POST'])
def buscar():
    consulta = request.form.get('consulta')  # nombre del input en tu formulario

    params = {
        'apiKey': API_KEY,
        'query': consulta,
        'number': 16, 
        'addRecipeInformation': True
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    recetas = data.get("results", [])

    return render_template('recetas.html', recetas=recetas)



from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'melyyyyaaasdwwd'

API_URL = 'https://api.spoonacular.com/recipes/complexSearch'
API_KEY = '923b514b2c604404954302eaebfea6fd'

usuarios = {}


@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':

        nombre = request.form.get('nombre')
        apeido = request.form.get('apeido')
        dia = request.form.get('dia')
        mes = request.form.get('mes')
        anio = request.form.get('anio')
        genero = request.form.get('genero')
        email = request.form.get('exampleInputEmail1')
        password = request.form.get('exampleInputPassword1')
        actividad = request.form.get('nivelactividad')
        peso = request.form.get('peso')
        altura = request.form.get('altura')

        if email in usuarios:
            flash("El correo ya está registrado, intenta iniciar sesión.")
            return redirect("/login")

        usuarios[email] = {
            "nombre": nombre,
            "apeido": apeido,
            "fecha": f"{dia}/{mes}/{anio}",
            "genero": genero,
            "password": password,
            "actividad": actividad,
            "peso": peso,
            "altura": altura
        }

        session["usuario"] = email
        session["nombre"] = nombre

        flash(f"Registro exitoso ¡Bienvenido a Sabores y Saberes {nombre}!")
        return redirect("/perfil")

    return render_template('formulario.html')


@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    return render_template("iniciar_sesion.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if email not in usuarios:
            flash("El usuario no existe")
            return redirect("/iniciar_sesion")

        if usuarios[email]["password"] != password:
            flash("Contraseña incorrecta")
            return redirect("/iniciar_sesion")

        session["usuario"] = email
        session["nombre"] = usuarios[email]["nombre"]

        flash("Inicio de sesión exitoso")
        return redirect("/")

    return render_template("iniciar_sesion.html")


@app.route('/alergias', methods=['GET', 'POST'])
def alergias():

    if request.method == 'POST':

        alergias_u = request.form.get('alergias')
        preferencias = request.form.get('preferencias')
        termino = request.form.get('termino')

        if not termino:
            flash("Debes escribir una búsqueda específica.", "error")
            return redirect(url_for('alergias'))

        dietas = {
            "Vegetariana": "vegetarian",
            "Vegana": "vegan",
            "Alta en proteína": "high-protein",
            "Baja en carbohidratos": "low-carb",
            "Sin azúcar": "low-sugar"
        }
        dieta_api = dietas.get(preferencias)

        params = {
            "apiKey": API_KEY,
            "query": termino,
            "intolerances": alergias_u,
            "diet": dieta_api,
            "number": 16
        }

        respuesta = requests.get(API_URL, params=params)
        data = respuesta.json()
        recetas = data.get("results", [])

        return render_template(
            'alergias.html',
            mensaje="Búsqueda realizada exitosamente",
            recetas=recetas
        )

    return render_template('alergias.html')


@app.route('/recet1', methods=['POST', 'GET'])
def recet1():
    return render_template('recet1.html')


@app.route('/perfil')
def perfil():
    if not session.get("usuario"):
        flash("Debes iniciar sesión para acceder a tu perfil.")
        return redirect("/login")

    email = session["usuario"]
    usuario = usuarios[email]

    return render_template('perfil.html', usuario=usuario)


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        ingrediente = request.form.get('ingrediente')

        params = {
            'apiKey': API_KEY,
            'query': ingrediente,
            'number': 10
        }

        respuesta = requests.get(API_URL, params=params)
        datos = respuesta.json()
        recetas = datos.get("results", [])

        return render_template("buscar.html", recetas=recetas)

    return render_template("buscar.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("nombre", None)
    flash("Has cerrado sesión correctamente")
    return redirect(url_for("inicio"))


if __name__ == '__main__':
    app.run(debug=True)




@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("nombre", None)
    flash("Has cerrado sesión correctamente")
    return redirect(url_for("inicio"))


if __name__ == '__main__':
    app.run(debug=True)

