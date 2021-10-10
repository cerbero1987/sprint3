from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from utils import isUsernameValid, isEmailValid, isPasswordValid
import yagmail as yagmail
from forms import Formulario_Usuario

app = Flask(__name__)
app.secret_key = "Equipo8"

@app.route('/')
@app.route('/index')
def index():    
    return render_template("index.html", titulo='Escuela Colombiana de Ingeniería Julio Garavito')

@app.route('/contacto')
def contacto():    
    return render_template("contacto.html")

@app.route('/ingresar')
def ingresar():    
    return render_template("ingresar.html")

@app.route('/comentariosactividad', methods=['GET', 'POST'])
def comentariosactividad():    
    return render_template("admin/comentariosactividad.html")

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    try:
        if request.method == 'POST':       
            usuario = request.form['usuario']
            email = request.form['email']
            password = request.form['password']

            error = None
            
            #1. Validar usuario, email y contraseña:
            if not isUsernameValid(usuario):
                # Si está mal.
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash(error)
            if not isEmailValid(email):
                # Si está mal.
                error = "Correo invalido"
                flash(error)
            if not isPasswordValid(password):
                # Si está mal.
                error = "La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"
                flash(error)

            if error is not None:
                # Ocurrió un error
                return render_template("registro.html")
            else:
                #2. Enviar un correo.
                # Para crear correo:                                    
                # Modificar la siguiente linea con tu informacion personal            
                yag = yagmail.SMTP('pehernaldo2@gmail.com', 'Hernaldo12345678*') 
                yag.send(to=email, subject='Activa tu cuenta',
                    contents='Bienvenido, usa este link para activar tu cuenta ')
                flash('Revisa tu correo para activar tu cuenta')

                #3. redirect para ir a otra URL
                return redirect( url_for( 'login' ) )

        return render_template("registro.html")

    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("registro.html")



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Formulario_Usuario(  request.form  )
    if request.method == 'POST' and form.validate():            
        flash('Inicio de sesión solicitado por el usuario {}, recordar={}'.format(form.usuario.data, form.recordar.data))
        return redirect(url_for('gracias'))

    return render_template("login.html", form=form, titulo='Inicio de sesión')


@app.route('/gracias', methods=['GET', 'POST'])
def gracias():
    return render_template("gracias.html", titulo='Gracias')