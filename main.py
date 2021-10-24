import sqlite3
from flask import Flask, flash, redirect, render_template, request, sessions, url_for, g, session
from werkzeug.utils import html #agregada por franklin
from utils import isCedulaValid, isUsernameValid, isEmailValid, isPasswordValid, isNameValid, isUsernameValidFacil, isPasswordValidFacil
#import yagmail as yagmail
from forms import Crear_Comentario, Formulario_Contacto, info_Docente, Formulario_Ingresar, info_Estudiante, crear_Actividad,registrar_Estudiante, registrar_Docente
from db import get_db, close_db
import functools
from werkzeug.security import generate_password_hash, check_password_hash #para el cifrado


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
                #yag = yagmail.SMTP('yeffersone@uninorte.edu.co','NN')
                #yag.send(to='yeffersone@uninorte.edu.co', subject='contacto web, '+nombre, contents=mensaje, headers={"Reply-To":f"{correo}"})
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
    #se que usario esta logueado para poder hacer el filtrado de actividades si es root lista todas las actividades, si es docente solo muestra sus actividades y si es alumno solo los del curso inscrito
    session['user_logueado']#id
    session['rol_logueado']#rol 1 admin - 2 docente - 3 estudiante
    if session['rol_logueado'] == 1:
        actividades =  db.execute('SELECT * FROM actividades INNER JOIN tipo_actividad ON actividades.id_tipo_actividad = tipo_actividad.id_tipo_actividad INNER JOIN asignaturas ON actividades.id_asignatura = asignaturas.id_asignatura').fetchall()
    elif session['rol_logueado'] !=1 and session['rol_logueado'] !=2: #Alumnos
        actividades =  db.execute('SELECT * FROM curso_alumnos INNER JOIN rel_curso_actividad_usuario ON rel_curso_actividad_usuario.id_curso = curso_alumnos.id_curso INNER JOIN actividades ON actividades.id_actividad = rel_curso_actividad_usuario.id_actividad INNER JOIN tipo_actividad ON tipo_actividad.id_tipo_actividad = actividades.id_tipo_actividad INNER JOIN asignaturas ON asignaturas.id_asignatura = actividades.id_asignatura WHERE curso_alumnos.id_usuario = ?',(session['user_logueado'],)).fetchall()
        print(actividades) 
    else:
        actividades =  db.execute('SELECT * FROM rel_curso_actividad_usuario INNER JOIN actividades ON rel_curso_actividad_usuario.id_actividad = actividades.id_actividad INNER JOIN tipo_actividad ON tipo_actividad.id_tipo_actividad = actividades.id_tipo_actividad INNER JOIN asignaturas ON asignaturas.id_asignatura = actividades.id_asignatura WHERE rel_curso_actividad_usuario.id_usuario = ?',(session['user_logueado'],)).fetchall()

    if actividades is None:
        error = "No se han creado actividades"
        flash(error)
        return render_template("admin/actividades/consultaractividades.html", titulo="Listado de Actividades")
    else:
        session['gps'] = "Actividades"
        #session['link'] = ""
        session['actividades'] = actividades

    return render_template("admin/actividades/consultaractividades.html")


@app.route('/comentariosactividad/<int:n1>', methods=['GET', 'POST'])
def comentariosactividad(n1):  
    session['gps'] = "Actividades"
    session['link'] = "consultaractividades"
    form = Crear_Comentario(  request.form  )  
    id_actividad = n1
    db = get_db()
    mensajesfull =  db.execute('SELECT mensaje,nombre_usuario,Apellido_usuario FROM rel_mensajes_actividades_usuario INNER JOIN usuario ON usuario.id_usuario = rel_mensajes_actividades_usuario.id_usuario WHERE rel_mensajes_actividades_usuario.id_actividad = ? AND eliminado = 0 ',(id_actividad,)).fetchall()
    actividad =  db.execute('SELECT * FROM actividades WHERE id_actividad = ?',(id_actividad,)).fetchone()
    if mensajesfull is None:
        error = "La actividad solicitada no tiene comentarios"
        flash(error)
        return redirect(url_for('consultaractividades'))
    else:
        session['mensajesfull'] = mensajesfull
        session['actividad'] = actividad
        redirect(url_for('consultaractividades'))
    return render_template("admin/comentariosactividad.html", form=form)

@app.route('/guardarcomentario', methods=['GET', 'POST'])
def guardarcomentario():
    try:
        form = Crear_Comentario(request.form)
        n1 = request.form['actividad'] 
        logueadouser = request.form['userlogueado'] 
        error = None
        if request.method == 'POST': 
            mensaje = request.form['mensaje']
            
            print("===", n1)
            print("===", logueadouser)
            print("===", mensaje)
            if error is not None:
                # Ocurrió un error
                return render_template("admin/comentariosactividad.html", form=form, n1=n1, titulo="Comentario Actividad")
            else:
                form = Crear_Comentario()
                db = get_db()
                db.execute('INSERT INTO rel_mensajes_actividades_usuario (id_actividad, id_usuario, mensaje, eliminado) VALUES (?, ?, ?, ?)',(n1, logueadouser, mensaje, 0))
                db.commit()
                flash("Mensaje asignado a la tarea")
                return render_template("admin/actividades/consultaractividades.html")

        return render_template("admin/comentariosactividad.html", form=form, n1=n1, titulo="Comentario Actividad")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/comentariosactividad.html", n1=n1, titulo="Comentario Actividad")

@app.route('/listarcomentariosEliminar', methods=['GET', 'POST'])
def listarcomentariosEliminar():
    
    session['listarcomentariosEliminar'] = "listarcomentarios"
    session['gps'] = "Lista de actividades"   
    return render_template("admin/listarcomentarios.html", titulo="Lista de actividades")


@app.route('/listarcomentariosEliminar/<int:lista>', methods=['GET', 'POST'])
def vercomentarios(lista):
    id_actividad = lista
    session['link'] = "consultaractividades"
    session['gps'] = "Lista de Comentarios a eliminar" 
    db = get_db()
    mensajesfull =  db.execute('SELECT id, mensaje,nombre_usuario,Apellido_usuario FROM rel_mensajes_actividades_usuario INNER JOIN usuario ON usuario.id_usuario = rel_mensajes_actividades_usuario.id_usuario WHERE rel_mensajes_actividades_usuario.id_actividad = ? AND eliminado = 0 AND rel_mensajes_actividades_usuario.id_usuario = ?',(id_actividad,session['user_logueado'])).fetchall()
    actividad =  db.execute('SELECT * FROM actividades WHERE id_actividad = ?',(id_actividad,)).fetchone()
    if mensajesfull is None or len(mensajesfull)==0:
        error = "La actividad solicitada no tiene comentarios"
        flash(error)
        return redirect(url_for('consultaractividades'))
    else:
        session['mensajesfull'] = mensajesfull
        session['actividad'] = actividad[0]
        session['opcion'] = 'Eliminar'
    return render_template("admin/listarcomentarios.html")
    
@app.route('/eliminarcomentario/<int:idActividad>/<int:idComentario>', methods=['GET', 'POST'])
def eliminarcomentario(idActividad,idComentario):
    error = None
    idComentario = idComentario
    idActividad = idActividad
    if request.method == 'GET': 
        if error is not None:
            # Ocurrió un error
            error = "Error"
            flash(error)
            return render_template("admin/comentariosactividad.html",titulo="Comentario Actividad")
        else:
            db = get_db()
            db.execute('UPDATE rel_mensajes_actividades_usuario SET eliminado = 1 WHERE id = ?',(idComentario,))
            db.commit()
            error = "Comentario eliminado en la actividad"
            flash(error)
            return redirect(url_for('consultaractividades'))

    return redirect(url_for('consultaractividades'))

@app.route('/editarcomentario/<int:idActividad>/<int:idComentario>', methods=['GET', 'POST'])
def editarcomentario(idActividad,idComentario):
    form = Crear_Comentario(request.form)
    error = None
    idComentario = idComentario
    idActividad = idActividad
    if request.method == 'GET': 
        if error is not None:
            # Ocurrió un error
            error = "Error"
            flash(error)
            return render_template("admin/comentariosactividad.html",titulo="Comentario Actividad")
        else:
            db = get_db()
            consulta = db.execute('SELECT mensaje FROM rel_mensajes_actividades_usuario WHERE id = ? AND eliminado = 0',(idComentario,)).fetchone()
            session['mesaje'] = consulta
            session['id'] = idComentario
            session['link'] = "consultaractividades"
            session['gps'] = "Editar Comentario" 
            
            return render_template("admin/Editarcomentarios.html", form = form, titulo="Comentario Actividad")

    return redirect(url_for('consultaractividades'))
    

@app.route('/listarcomentariosEditar/<int:lista>', methods=['GET', 'POST'])
def listarcomentariosEditar(lista):
    id_actividad = lista
    session['link'] = "consultaractividades"
    session['gps'] = "Lista de Comentarios a Editar" 
    db = get_db()
    mensajesfull =  db.execute('SELECT id, mensaje,nombre_usuario,Apellido_usuario FROM rel_mensajes_actividades_usuario INNER JOIN usuario ON usuario.id_usuario = rel_mensajes_actividades_usuario.id_usuario WHERE rel_mensajes_actividades_usuario.id_actividad = ? AND eliminado = 0 AND rel_mensajes_actividades_usuario.id_usuario = ?',(id_actividad,session['user_logueado'])).fetchall()
    actividad =  db.execute('SELECT * FROM actividades WHERE id_actividad = ?',(id_actividad,)).fetchone()
    if mensajesfull is None or len(mensajesfull)==0:
        error = "La actividad solicitada no tiene comentarios"
        flash(error)
        return redirect(url_for('consultaractividades'))
    else:
        session['mensajesfull'] = mensajesfull
        session['actividad'] = actividad[0]
        session['opcion'] = 'Editar'
    return render_template("admin/listarcomentarios.html")

@app.route('/actualizarcomentario', methods=['GET', 'POST'])
def actualizarcomentario():
    try:
        form = Crear_Comentario(request.form)
        idcomentarioeditar = request.form['actividad'] 
        error = None
        if request.method == 'POST': 
            mensajeeditado = request.form['mensaje'] 
            if error is not None:
                # Ocurrió un error
                return render_template("admin/comentariosactividad.html", form=form, titulo="Comentario Actividad")
            else:
                form = Crear_Comentario()
                db = get_db()
                db.execute('UPDATE rel_mensajes_actividades_usuario SET mensaje = ? WHERE id = ?',(mensajeeditado,idcomentarioeditar))
                db.commit()
                flash("Mensaje editado con exito")
                return render_template("admin/actividades/consultaractividades.html")

        return render_template("admin/comentariosactividad.html", form=form, titulo="Comentario Actividad")
    except:
        flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
        return render_template("admin/comentariosactividad.html", titulo="Comentario Actividad")

#MODULO CALIFICACIONES
#calificaciones publicadas docente
@app.route('/calificacionespublicadas', methods=['GET', 'POST'])
def calificacionespublicadas():
    session.pop('nameprog', None)
    session.pop('actividad', None)
    session.pop('cursofull', None)
    session.pop('actividadSeleccionada', None)
    session['gps']="Calificaciones publicadas" #breadcrumb
    db = get_db()
    programasfull =  db.execute('SELECT id_programa, nombre_programa FROM programas').fetchall()
    if programasfull is None or len(programasfull)==0:
        error = "No existen programas academicos en la Base de Datos"
        flash(error)
        return redirect(url_for('sindatos'))
    else:
        session['programasfull'] = programasfull
    return render_template("admin/calificacionespublicadas.html", titulo="Ver Calificaciones")

@app.route('/calificacionespublicadas/<int:programa>', methods=['GET', 'POST'])
def calificacionespublicadasPrograma(programa):
    if programa != 0:
        db = get_db()
        cursofull =  db.execute('SELECT id_cursos, nombre_curso FROM cursos WHERE id_programa = ?',(programa,)).fetchall()
        if cursofull is None or len(cursofull)==0:
            session.pop('namecurso', None)
            session.pop('cursofull', None)
            session.pop('actividad', None)
            error = "No existen Cursos asociados al programa academico seleccionado"
            flash(error)
            return redirect(url_for('calificacionespublicadas'))
        else:
            nameprog =  db.execute('SELECT id_programa,nombre_programa FROM programas WHERE id_programa = ?',(programa,)).fetchone()
            session.pop('namecurso', None)
            session.pop('cursofull', None)
            session.pop('actividad', None)
            session.pop('actividadSeleccionada', None)
            session['cursofull'] = cursofull
            session['nameprog'] = nameprog[1]
            session['id_programa'] = nameprog[0]
    return render_template("admin/calificacionespublicadas.html", titulo="Ver Calificaciones")

@app.route('/calificacionespublicadas/<int:programa>/<int:curso>', methods=['GET', 'POST'])
def calificacionespublicadascurso(programa,curso):
    
    if programa != 0 and curso !=0: 
        db = get_db()
        actividad =  db.execute('SELECT DISTINCT actividades.id_actividad, actividades.descripcion FROM rel_curso_actividad_usuario INNER JOIN actividades ON actividades.id_actividad = rel_curso_actividad_usuario.id_actividad WHERE rel_curso_actividad_usuario.id_curso=?',(curso,)).fetchall()
        
        if actividad is None or len(actividad)==0:
            session.pop('desc', None)
            session.pop('namecurso', None)
            session.pop('actividad', None)
            session.pop('actividadSeleccionada', None)
            error = "No existen Actividades asociadas al Curso seleccionado"
            flash(error)
            return render_template("admin/calificacionespublicadas.html", programa = programa, titulo="Ver Calificaciones")
        else:
            nameprog =  db.execute('SELECT nombre_programa FROM programas WHERE id_programa = ?',(programa,)).fetchone()
            namecurso =  db.execute('SELECT nombre_curso FROM cursos WHERE id_cursos = ?',(curso,)).fetchone()
            if namecurso is None or len(namecurso)==0:
                session['namecurso'] = "seleccione el programa"

            else:
                session['namecurso'] = namecurso
                session['desc'] = "seleccione la actividad"
            
            session['actividad'] = actividad
            session['nameprog'] = nameprog[0]
            session['id_curso'] = curso
            
    return render_template("admin/calificacionespublicadas.html", programa = programa, titulo="Ver Calificaciones")

@app.route('/calificacionespublicadas/<int:programa>/<int:curso>/<int:actividad>', methods=['GET', 'POST'])
def calificacionespublicadascursoactividad(programa,curso,actividad):
    
    if programa != 0 and curso !=0 and actividad != 0: 
        db = get_db()
        actividadSeleccionada =  db.execute('SELECT rel_curso_actividad_usuario.id_actividad, actividades.descripcion, rel_curso_actividad_usuario.calificacion, usuario.nombre_usuario, usuario.Apellido_usuario FROM rel_curso_actividad_usuario INNER JOIN actividades ON actividades.id_actividad = rel_curso_actividad_usuario.id_actividad INNER JOIN usuario ON usuario.id_usuario = rel_curso_actividad_usuario.id_usuario INNER JOIN rol ON usuario.id_rol = rol.id_rol WHERE rel_curso_actividad_usuario.id_actividad = ? AND rol.id_rol = 3',(actividad,)).fetchall()
        
        if actividadSeleccionada is None or len(actividadSeleccionada)==0:
            session.pop('desc', None)
            session.pop('namecurso', None)
            session.pop('actividad', None)
            session.pop('actividadSeleccionada', None)
            error = "No existen Actividades asociadas al Curso seleccionado"
            flash(error)
            return render_template("admin/calificacionespublicadas.html", programa = programa, titulo="Ver Calificaciones")
        else:
            nameprog =  db.execute('SELECT nombre_programa FROM programas WHERE id_programa = ?',(programa,)).fetchone()
            namecurso =  db.execute('SELECT nombre_curso FROM cursos WHERE id_cursos = ?',(curso,)).fetchone()
            nameactividad =  db.execute('SELECT descripcion FROM actividades WHERE id_actividad = ?',(actividad,)).fetchone()
            if namecurso is None or len(namecurso)==0:
                session['namecurso'] = "seleccione el programa"
                session['desc'] = "seleccione la actividad"
                
            else:
                session['namecurso'] = namecurso

            if nameactividad is None or len(nameactividad)==0:
                session['desc'] = "seleccione la actividad"
                
            else:
                session['desc'] = nameactividad[0]
                
            
            session['actividadSeleccionada'] = actividadSeleccionada
            session['nameprog'] = nameprog[0]
            session['id_curso'] = curso
            
    return render_template("admin/calificacionespublicadas.html", programa = programa, titulo="Ver Calificaciones")

#Calificaciones Alumno  solo Ver
@app.route('/calificacionalumno', methods=['GET', 'POST'])
def calificacionalumno():
    session['gps']="Mis Calificaciones" #breadcrumb
    db = get_db()
    cursoalumno =  db.execute('SELECT DISTINCT cursos.id_cursos, cursos.nombre_curso FROM rel_curso_actividad_usuario INNER JOIN cursos ON cursos.id_cursos = rel_curso_actividad_usuario.id_curso WHERE rel_curso_actividad_usuario.id_usuario=?',(session['user_logueado'],)).fetchall()
    if cursoalumno is None or len(cursoalumno)==0:
        session.pop('cursoalumno', None)
        session.pop('calificacion', None)
        error = "El alumno no tiene matriculado ningun curso"
        flash(error)
        return redirect(url_for('sindatos'))
    else:
        session.pop('cursoalumno', None)
        session.pop('calificacion', None)
        session['cursoalumno'] = cursoalumno
    return render_template("admin/calificacionalumno.html", titulo="Ver Tus Calificaciones")

@app.route('/calificacionalumno/<int:curso>', methods=['GET', 'POST'])
def calificacionalumnocurso(curso):
    if curso != 0:
        db = get_db()
        calificacion =  db.execute('SELECT DISTINCT actividades.descripcion, rel_curso_actividad_usuario.calificacion FROM rel_curso_actividad_usuario INNER JOIN actividades ON actividades.id_actividad = rel_curso_actividad_usuario.id_actividad WHERE rel_curso_actividad_usuario.id_usuario = ? AND rel_curso_actividad_usuario.id_curso = ?',(session['user_logueado'], curso)).fetchall()
        if calificacion is None or len(calificacion)==0:
            session.pop('cursoalumno', None)
            session.pop('calificacion', None)
            error = "El curso no tiene notas disponibles"
            flash(error)
            return redirect(url_for('calificacionalumno'))
        else:
            namecurso =  db.execute('SELECT nombre_curso FROM cursos WHERE id_cursos = ?',(curso,)).fetchone()
            if namecurso is None or len(namecurso)==0:
                session['namecurso'] = "seleccione el programa"
                
            else:
                session['namecurso'] = namecurso
            session['calificacion'] = calificacion
    return render_template("admin/calificacionalumno.html", titulo="Ver Tus Calificaciones")

@app.route('/sindatos', methods=['GET', 'POST'])
def sindatos():
    return render_template("admin/sindatos.html", titulo='Error 404')

@app.route('/gracias', methods=['GET', 'POST'])
def gracias():
    return render_template("gracias.html", titulo='Gracias')

#franklin
@app.route('/home', methods=['GET', 'POST'])
def home(): #----------------------------------------------------------->home
   
    session['gps']="Inicio" #breadcrumb
    if session['rol_logueado']==2:   #dependiendo el usuario se modifican aqui las direcciones url a donde deben ir,
        session['perfil']="infodocente" 
        session['cursos']="cursosdocente" 
        session['buscacursos']="busquedacursos" 
        session['mensajes']="consultaractividades"
        session['creacionactividad']="creacionactividaddocente"
        session['veractividad']="consultaractividades"
        session['notas']="notasdocente"
        session['calificacionespublicadas']="calificacionespublicadas"
    elif session['rol_logueado']==3:
        session['perfil']="infoestudiante"
        session['mensajes']="consultaractividades"
        session['buscacursos']="busquedacursos" 
        session['veractividad']="consultaractividades"
        session['notas']="notasestudiante"
    else:
        session['perfil']="infodocente"      # a falta de ventanas coloco las mismas para que no se cuelgue. ya el menu divide todo
        session['cursos']="cursosdocente" 
        session['buscacursos']="busquedacursos" 
        session['mensajes']="consultaractividades"
        session['creacionactividad']="creacionactividaddocente"
        session['veractividad']="consultaractividades"
        session['notas']="notasdocente"
        session['calificacionespublicadas']="calificacionespublicadas"
       
    return render_template("admin/home.html", titulo=session['nombre_rol'])


@app.route('/infodocente', methods=['GET', 'POST'])
def infodocente():
    try:
        error = None
        if request.method == 'POST': #and form.validate():  
            #print("ya presionaron guardar, ENTRANDO CON EL POST")
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            correo = request.form['correo']
            cedula = request.form['cedula']
            pregrado = request.form['pregrado']
            postgrado = request.form['postgrado']
            
            #1. Validar datos de contacto:
            if not( isNameValid(nombre) or isNameValid(apellido) ):
                # Si está mal.
                error = "Solo debe usar letras en los campos Nombres y apellidos"
                flash(error)
            if not isEmailValid(correo):
                # Si está mal.
                error = "Correo invalido"
                flash(error)
            if not isCedulaValid(cedula): 
            #  Si está mal.
               error = "Numero de cedula invalido"
               flash(error)
            if error is not None:
                # Ocurrió un error
                form = info_Docente(request.form)
                return render_template("admin/infodocente.html", form=form, titulo="Información de Docente")
                
            else:
                db = get_db() 
                consulta=db.execute("UPDATE usuario SET nombre_usuario=? , Apellido_usuario=?, correo=?, cedula=?, pregrado=?, postgrado=?  WHERE id_usuario =?",(nombre, apellido, correo, cedula, pregrado, postgrado, session['user_logueado']))
                db.commit() # si no se hace comit, no se confirmara ninguna modificacion en la bd
               # print("ya ejecute el SQL y debi actualizar")
                flash("Valores actualizados con éxito")
                consulta_inicio=db.execute("SELECT * FROM usuario WHERE id_usuario = ?", (session['user_logueado'],)).fetchone()
                #flash("la consulta de select "+ str(consulta_inicio))
                #print("confirmé que si actualicé")
                close_db()
                #print("cerré la base de datos")
                session['datos_form'] = consulta_inicio
                form = info_Docente(request.form)
                return render_template("admin/infodocente.html", form=form, titulo="Información de Docente")
        else:
            #recien entra al link infodocente.html....   
            print("entro con GET")
            session['gps']="Perfil" #breadcrumb
            
            db = get_db() 
            consulta_inicio=db.execute("SELECT * FROM usuario WHERE id_usuario = ?", (session['user_logueado'],)).fetchone()
            session['datos_form'] = consulta_inicio
            print("ya hice el formulario, y le puse los valores de la consulta")
            form = info_Docente(request.form)
            close_db()
            return render_template("admin/infodocente.html", form=form, titulo="Información de Docente")
    
    except:
       flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
       return render_template("admin/infodocente.html", form=form,titulo="Información de Docente")


#Decoradores informacion estudiante
@app.route('/infoestudiante', methods=['GET', 'POST'])
def infoestudiante():
    error = None
    if request.method == 'POST': #and form.validate(): 
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fechaNac = request.form['fechaNac']
        correo = request.form['correo']
        telefono = request.form['telefono']
        cedula = request.form['cedula']
        #codigo = request.form['codigo']    ---->no deben ser modificables por el estudiante
        #facultad = request.form['facultad'] ---->no
        #programa = request.form['carrera']---->no
        
        #1. Validar datos de contacto:
        if not( isNameValid(nombre) or isNameValid(apellido) ):
            # Si está mal.
            error = "Solo debe usar letras en los campos Nombres y apellidos"
            flash(error)
        if not isEmailValid(correo):
            # Si está mal.
            error = "Correo invalido"
            flash(error)
        if not(isCedulaValid(cedula) or isCedulaValid(telefono)): 
        #  Si está mal.
            error = "Numero de cedula invalido"
            flash(error)
        if error is not None:
            # Ocurrió un error
            form = info_Estudiante(request.form)
            return render_template("admin/infoestudiante.html", form=form, titulo="Información de Estudiante")
            
        else:
            db = get_db() 
            consulta=db.execute("UPDATE usuario SET nombre_usuario=? , Apellido_usuario=?, correo=?, cedula=?, telefono=?, fecha_nacimiento=?  WHERE id_usuario =?",(nombre, apellido, correo, cedula, telefono, fechaNac, session['user_logueado']))
            db.commit() # si no se hace comit, no se confirmara ninguna modificacion en la bd
            # print("ya ejecute el SQL y debi actualizar")
            flash("Valores actualizados con éxito")
            consulta_inicio=db.execute("SELECT * FROM usuario WHERE id_usuario = ?", (session['user_logueado'],)).fetchone()

            close_db()
          
            session['datos_form'] = consulta_inicio
            form = info_Estudiante(request.form)
            return render_template("admin/infoestudiante.html", form=form, titulo="Información de Estudiante")
    else:
        #recien entra al link infoestudiante.html....   
        print("entro con GET")
        session['gps']="Perfil" #breadcrumb
        
        db = get_db() 
        consulta_inicio=db.execute("SELECT * FROM usuario WHERE id_usuario = ?", (session['user_logueado'],)).fetchone()
        session['datos_form'] = consulta_inicio
        form = info_Estudiante(request.form)
        close_db()
        return render_template("admin/infoestudiante.html", form=form, titulo="Información de Estudiante")

#Notas Estudiante
@app.route('/notasestudiante', methods=['GET', 'POST'])
def notasestudiante():
    session['gps']="Calificaciones" #breadcrumb
    return render_template("admin/notasestudiante.html", titulo="Calificaciones de Estudiante")



#Notas docente
@app.route('/notasdocente', methods=['GET', 'POST'])
def notasdocente():
    session['gps']="Cursos" #breadcrumb
    
    return render_template("admin/notasdocente.html", titulo="Calificaciones de Estudiante")

@app.route('/logout')
def  cerrarsesion():
    session.clear()
    
    return redirect(url_for("ingresar"))

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
                #user =  db.execute('SELECT * FROM usuario WHERE user_usuario = ? AND password_usuario = ?',(usuario, contrasena)).fetchone()
                user =  db.execute('SELECT id_usuario, id_rol, user_usuario, password_usuario, nombre_usuario, apellido_usuario FROM usuario WHERE user_usuario = ?',(usuario,)).fetchone() 
                print(user) 
                if user is None:
                    error = "Usuario no Existe en la Base de Datos"
                    flash(error)
                else:                
                    usuario_valido = check_password_hash(user[3],contrasena)
                    if not usuario_valido:
                        error = "Usuario y/o contraseña no son correctos."
                        flash( error )  
                        form = Formulario_Ingresar( )
                        return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")
                    else:
                        rol =  db.execute('SELECT * FROM rol WHERE id_rol = ?',(user[1],)).fetchone()
                        
                        session['user_logueado'] = user[0] #id
                        session['rol_logueado'] = user[1]
                        session['nombre_logueado'] = user[4]
                        session['apellido_logueado'] = user[5]
                        session['nombre_rol'] = rol[1]
                        
                    return redirect( url_for( 'home' ) )
        
        else:
        
            form = Formulario_Ingresar( )
            return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")
    #except:
     #   flash("¡Ups! Ha ocurrido un error, intentelo de nuevo.")
      #  form = Formulario_Ingresar( )
       # return render_template("ingresar.html", form=form, titulo="Iniciar Sesión")

#Decorador buscador de cursos
@app.route('/busquedacursos', methods=['GET', 'POST'])
def busqueda_cursos():
    session['gps']="Buscar cursos" #breadcrumb
    return render_template("admin/busquedacursos.html", titulo="Buscador de cursos")

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
    session['gps']="Actividades" #breadcrumb
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


#registro de contraseñas-------------------------------21-10-21
@app.route('/registrocontrasenas', methods=['GET', 'POST'])
def registrocontrasenas():
    #try:
        if request.method == 'POST':   
            
            password = request.form['password']
            password2 = request.form['password2']
            flash(password)
            flash(password2)
            
            db = get_db()
             #cambiar a id de usuario logeado
            id =  session['user_logueado'] 
            flash(id)
            error = None
            
            
            if not password:
                error = "Contraseña requerida."
                flash(error)
            if not password2:
                error = "Contraseña requerida."
                flash(error)
            #1. Validar usuario, email y contraseña:
            #if not isUsernameValid(usuario):
                # Si está mal.
            #    error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
            #    flash(error)
            #if not isEmailValid(email):
                # Si está mal.
            #    error = "Correo invalido"
            #    flash(error)
            #if not isPasswordValid(password):
                # Si está mal.
            #    error = "La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres"
            #    flash(error)
                      
            if password2 != password:
                error = "Las contraseñas no coinciden"
                flash(error)

            if error is not None:
                # Ocurrió un error
                return render_template("registrocontrasenas.html")
            else:
                # Seguro:
                password_cifrado = generate_password_hash(password)
                db.execute(
                    
                    "UPDATE usuario SET password_usuario = ? WHERE id_usuario = ?",(password_cifrado,id)
                )
                db.commit()
                #2. Enviar un correo.
                # Para crear correo:                                    
                # Modificar la siguiente linea con tu informacion personal            
                 #yag = yagmail.SMTP('yeffersone@uninorte.edu.co','NN')
                #yag.send(to='yeffersone@uninorte.edu.co', subject='contacto web, '+nombre, contents=mensaje, headers={"Reply-To":f"{correo}"})
                #    contents='Bienvenido, usa este link para activar tu cuenta ')
                flash('Contraseña Modificada con exito')

                #3. redirect para ir a otra URL
                return redirect( url_for( 'ingresar' ) )

        return render_template("admin/registrocontrasenas.html")