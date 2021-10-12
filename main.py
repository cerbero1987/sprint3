from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import html #agregada por franklin
from utils import isUsernameValid, isEmailValid, isPasswordValid, isNameValid
import yagmail as yagmail
from forms import Formulario_Contacto


app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/index')
def index():    
    return render_template("index.html", titulo='Escuela Colombiana de Ingeniería Julio Garavito')

#Formulario de Contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    try:
        form = Formulario_Contacto(  request.form  )
        error = None
        if request.method == 'POST': #and form.validate():  
            nombre = request.form['nombre']
            correo = request.form['correo']
            mensaje = request.form['mensaje']

            #1. Validar datos de contacto:
            if not isNameValid(nombre):
                # Si está mal.
                error = "Solo debe usar letras en nombre y apellido"
                flash(error)
            if not isEmailValid(correo):
                # Si está mal.
                error = "Correo invalido"
                flash(error)
            if error is not None:
                # Ocurrió un error
                return render_template("contacto.html", form=form, titulo="Formulario de contacto")
            else:
                #2. Enviar un correo.
                # Para crear correo:                                    
                # Modificar la siguiente linea con tu informacion personal            
                yag = yagmail.SMTP('yeffersone@uninorte.edu.co','39VMbtj_2EZ6jZ-')
                yag.send(to='yeffersone@uninorte.edu.co', subject='contacto web, '+nombre, contents=mensaje, headers={"Reply-To":f"{correo}"})
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("contacto.html", form=form, titulo="Formulario de contacto")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("contacto.html", titulo="Formulario de contacto")


@app.route('/ingresar')
def ingresar():    
    return render_template("ingresar.html")

#Decoradores Panel Administrativo
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


@app.route('/gracias', methods=['GET', 'POST'])
def gracias():
    return render_template("gracias.html", titulo='Gracias')

#franklin
@app.route('/infodocente', methods=['GET', 'POST'])
def informacionDocente():
    return render_template("admin/infodocente.html", titulo="Información de Docente")

#Notas Estudiante
@app.route('/notaestudiante', methods=['GET', 'POST'])
def notasEstudiante():
    return render_template("admin/notasestudiante.html", titulo="Calificaciones de Estudiante")

#Notas docente
@app.route('/notadocente', methods=['GET', 'POST'])
def notadocente():
    return render_template("admin/notasdocente.html", titulo="Calificaciones de Estudiante")