from flask import Flask, flash, redirect, render_template, request, sessions, url_for, g, session
from werkzeug.utils import html #agregada por franklin
from utils import isUsernameValid, isEmailValid, isPasswordValid, isNameValid, isUsernameValidFacil, isPasswordValidFacil
import yagmail as yagmail
from forms import Formulario_Contacto, info_Docente, Formulario_Ingresar, info_Estudiante, crear_Actividad,registrar_Estudiante, registrar_Docente
from db import get_db, close_db
import functools


app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('ingresar'))
        return view(**kwargs)
    return wrapped_view

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
                yag = yagmail.SMTP('yeffersone@uninorte.edu.co','NN')
                yag.send(to='yeffersone@uninorte.edu.co', subject='contacto web, '+nombre, contents=mensaje, headers={"Reply-To":f"{correo}"})
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("contacto.html", form=form, titulo="Formulario de contacto")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("contacto.html", titulo="Formulario de contacto")

#Decoradores Panel Administrativo
#Accesiones Generales
@app.route('/consultaractividades', methods=['GET', 'POST'])#lista las actividades 
def consultaractividades():
    db = get_db()
    actividades =  db.execute('SELECT * FROM actividades INNER JOIN tipo_actividad ON actividades.id_tipo_actividad = tipo_actividad.id_tipo_actividad').fetchall()
    if actividades is None:
        error = "No se han creado actividades"
        flash(error)
        return render_template("admin/actividades/consultaractividades.html", titulo="Listado de Actividades")
    else:
        for i in range(len(actividades)):
            for j in range(len(actividades[i])):
                print(actividades[i][j], end=' ')
            print()
        
        session['actividades'] = actividades
    return render_template("admin/actividades/consultaractividades.html")

@app.route('/comentariosactividad', methods=['GET', 'POST'])
def comentariosactividad():    
    return render_template("admin/comentariosactividad.html")

@app.route('/gracias', methods=['GET', 'POST'])
def gracias():
    return render_template("gracias.html", titulo='Gracias')

#franklin
@app.route('/infodocente', methods=['GET', 'POST'])
def infodocente():
    try:
        form = info_Docente(request.form)
        error = None
        if request.method == 'POST': #and form.validate():  
            nombre = request.form['nombre']
            correo = request.form['correo']
            cedula = request.form['cedula']

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
                return render_template("admin/infodocente.html", form=form, titulo="Información de Docente")
            else:
                #2. Enviar un correo.
                # Para crear correo:                                    
                # Modificar la siguiente linea con tu informacion personal            
                
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("admin/infodocente.html", form=form, titulo="Información de Docente")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/infodocente.html", form=form,titulo="Información de Docente")

#Notas Estudiante
@app.route('/notasestudiante', methods=['GET', 'POST'])
def notasestudiante():
    return render_template("admin/notasestudiante.html", titulo="Calificaciones de Estudiante")

#Notas docente
@app.route('/notasdocente', methods=['GET', 'POST'])
def notasdocente():
    return render_template("admin/notasdocente.html", titulo="Calificaciones de Estudiante")

#Gabriel
#Formulario de Ingreso
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    #try:
        form = Formulario_Ingresar(request.form)    
        if request.method == 'POST': #and form.validate():  
            usuario = request.form['usuario']
            contrasena = request.form['contrasena'] 
            error = None

           #1. Validar datos de ingreso:
            if not isUsernameValidFacil(usuario):
                # Si está mal.
                error = "Solo debe usar letras en Usuario"
                flash(error)
            if not isPasswordValidFacil(contrasena):
                # Si está mal.
                error = "contraseña invalida"
                flash(error)
            if error is not None:
                # Ocurrió un error
                form = Formulario_Ingresar( )
                return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")
            else:
                db = get_db()
                user =  db.execute('SELECT * FROM usuario WHERE user_usuario = ? AND password_usuario = ?',(usuario, contrasena)).fetchone()
                
                if user is None:
                    error = "Usuario no Existe en la Base de Datos"
                    flash(error)
                    form = Formulario_Ingresar( )
                    return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")
                else:
                    rol =  db.execute('SELECT * FROM rol WHERE id_rol = ?',(user[1],)).fetchone()
                    
                    session['user_logueado'] = user[0]
                    session['rol_logueado'] = user[1]
                    session['nombre_logueado'] = user[4]
                    session['apellido_logueado'] = user[5]
                    session['nombre_rol'] = rol[1]
                    if user[1] == 1:
                        return render_template("admin/paneladmin.html", titulo='Panel de Administración')
                    if user[1] == 2:
                        return render_template("admin/paneladmin.html", titulo='Panel de Docente')
                    if user[1] == 3:
                        return render_template("admin/paneladmin.html", titulo='Panel de Alumno')
                    else:
                        return render_template("admin/paneladmin.html", titulo='Panel de Error')


        else:
            #flash("No entro if POST")
            form = Formulario_Ingresar( )
            return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")
    #except:
     #   flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
      #  form = Formulario_Ingresar( )
       # return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")

#Decorador buscador de cursos
@app.route('/busquedacursos', methods=['GET', 'POST'])
def busqueda_cursos():
    return render_template("admin/busquedacursos.html", titulo="Buscador de cursos")

#Decoradores informacion estudiante
@app.route('/infoestudiante', methods=['GET', 'POST'])
def infoestudiante():
    try:
        form = info_Estudiante(request.form)
        error = None
        if request.method == 'POST': #and form.validate():  
            nombre = request.form['nombre']
            correo = request.form['correo']
            cedula = request.form['cedula']

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
                return render_template("admin/infoestudiante.html", form=form, titulo="Información del Estudiante")
            else:
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("admin/infoestudiante.html", form=form, titulo="Información del Estudiante")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/infoestudiante.html", form=form,titulo="Información del Estudiante")

#Claudio
@app.route('/creacionactividaddocente', methods=['GET', 'POST'])
def creacionactividaddocente():
    try:
        form = crear_Actividad(request.form)
        error = None
        if request.method == 'POST': #and form.validate():  
            nombreActividad = request.form['nombreActividad']
            descripcion = request.form['descripcion']
            fechaEntrega = request.form['fechaEntrega']
            tipoActividad = request.form['tipoActividad']
            asignatura = request.form['asignatura']
            curso = request.form['curso']

            #1. Validar datos de contacto:
            if not isNameValid(nombreActividad):
                # Si está mal.
                error = "Solo debe usar letras en nombre y apellido"
                flash(error)
            if not isNameValid(descripcion):
                # Si está mal.
                error = "Correo invalido"
                flash(error)
            if error is not None:
                # Ocurrió un error
                return render_template("admin/creacionactividaddocente.html", form=form, titulo="Crear Actividad")
            else:
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("admin/creacionactividaddocente.html", form=form, titulo="Crear Actividad")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/creacionactividaddocente.html", form=form,titulo="Crear Actividad")


@app.route('/detalleactividadestudiante', methods=['GET', 'POST'])
def detalleactividadestudiante():
    return render_template("admin/detalleactividadestudiante.html", titulo="Detalles de la actividad")

#Lennin
@app.route('/registrodeusurioEstudiante', methods=['GET', 'POST'])
def registrodeusurioEstudiante():
    try:
        form = registrar_Estudiante(request.form)
        error = None
        if request.method == 'POST': #and form.validate():  
            nombre = request.form['nombre']
            codigo = request.form['codigo']
            correo = request.form['correo']
            programa = request.form['programa']
            apellidos = request.form['apellidos']
  
            #1. Validar datos de contacto:
            if not isNameValid(nombre):
                # Si está mal.
                error = "Solo debe usar letras en nombre y apellido"
                flash(error)
            if not isNameValid(apellidos):
                # Si está mal.
                error = "Correo invalido"
                flash(error)
            if error is not None:
                # Ocurrió un error
                return render_template("admin/registrodeusurioEstudiante.html", form=form, titulo="Registrar Estudiante")
            else:
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("admin/registrodeusurioEstudiante.html", form=form, titulo="Registrar Estudiante")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/registrodeusurioEstudiante.html", form=form,titulo="Registrar Estudiante")

@app.route('/registrousuariodocente', methods=['GET', 'POST'])
def registrousuariodocente():
    try:
        form = registrar_Docente(request.form)
        error = None
        if request.method == 'POST': #and form.validate():  
            nombre = request.form['nombre']
            codigo = request.form['codigo']
            correo = request.form['correo']
            programa = request.form['programa']
            apellidos = request.form['apellidos']
  
            #1. Validar datos de contacto:
            if not isNameValid(nombre):
                # Si está mal.
                error = "Solo debe usar letras en nombre y apellido"
                flash(error)
            if not isNameValid(apellidos):
                # Si está mal.
                error = "Correo invalido"
                flash(error)
            if error is not None:
                # Ocurrió un error
                return render_template("admin/registrousuariodocente.html", form=form, titulo="Registrar Docente")
            else:
                return render_template("gracias.html", titulo='Gracias por escribirnos')

        return render_template("admin/registrousuariodocente.html", form=form, titulo="Registrar Docente")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/registrousuariodocente.html", form=form,titulo="Registrar Docente")

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("admin/dashboard.html", titulo="Dashboard")
