from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators, TextAreaField, SelectField,PasswordField, DateField

class Formulario_Contacto(Form):
    nombre = StringField('Nombre y Apellido', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25)
    ] )
    correo = StringField('E-mail',
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25) 
    ])
    mensaje = TextAreaField('Mensaje',
    [
        validators.DataRequired('Campo Requerido para contacto')
    ])
    enviar = SubmitField('Enviar')
    

class Crear_Comentario(Form):
    mensaje = TextAreaField('Comentario')
    enviar = SubmitField('Enviar')

#Franklin
class info_Docente(Form):
    nombre = StringField('Nombres y Apellidos', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    correo = StringField('E-mail',
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25) 
    ])
    cedula = StringField('Número de Cedula',
    [
        validators.DataRequired('Ingrese su nùmero de cedula')
    ])
    pregrado = StringField('Pregrado', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    postgrado = StringField('Postgrado', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    language = SelectField(u'Asignatura', choices=[('a1', 'Asignatura 1'), ('a2', 'Asignatura 2'), ('a3', 'Asignatura 3')])
    guardar = SubmitField('Guardar')

#Gabriel
class Formulario_Ingresar(Form):
    usuario = StringField('Usuario', 
    [ 
        validators.DataRequired('Campo Requerido para ingresar'), 
        validators.Length(min=8,max=10)
    ] )
    contrasena = PasswordField('Contraseña',
    [ 
        validators.DataRequired('Campo Requerido para ingresar'), 
        validators.Length(min=8,max=25) 
    ])
    recordar = BooleanField('Recordar Usuario')
    
    login = SubmitField('Login')

class info_Estudiante(Form):
    nombre = StringField('Nombre completo', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    facultad = StringField('Facultad', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    carrera = StringField('Carrera', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    correo = StringField('Correo Electrónico',
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25) 
    ])
    cedula = StringField('Número de Cedula',
    [
        validators.DataRequired('Ingrese su nùmero de cedula')
    ])
    telefono = StringField('Telefono/Celular', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    codigo = StringField('ID Estudiante', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    fechaNac = DateField('Fecha de Nacimiento', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
    ] )
    language = SelectField(u'Asignatura', choices=[('a1', 'Asignatura 1'), ('a2', 'Asignatura 2'), ('a3', 'Asignatura 3')])
    guardar = SubmitField('Guardar')

#Claudio
class crear_Actividad(Form):
    nombreActividad = StringField('Nombre de la actividad', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25)
    ] )
    fechaEntrega = StringField('Fecha de Entrega',
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25) 
    ])
    descripcion = TextAreaField('Descripción de la actividad',
    [
        validators.DataRequired('Campo Requerido para contacto')
    ])
    tipoActividad = SelectField(u'Tipo de Actividad', choices=[('tp1', 'Taller'), ('tp2', 'Quiz'), ('tp3', 'Parcial'), ('tp4', 'ensayo'), ('tp5', 'otros')])
    asignatura = SelectField(u'Asignatura', choices=[('a1', 'Asignatura 1'), ('a2', 'Asignatura 2'), ('a3', 'Asignatura 3')])
    curso = SelectField(u'Curso', choices=[('c1', 'Curso 1'), ('c2', 'Curso 2'), ('c3', 'Curso 3')])
    enviar = SubmitField('Crear Actividad')

#Lennin
class registrar_Estudiante(Form):
    nombre = StringField('Nombre completo', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    apellidos = StringField('Apellidos', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    codigo = StringField('ID Estudiante', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    correo = StringField('Correo Electrónico',
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25) 
    ])
    programa = SelectField(u'Programa', choices=[('p1', 'Programa 1'), ('p2', 'Programa 2'), ('p3', 'Programa 3')])
    guardar = SubmitField('Guardar')

class registrar_Docente(Form):
    nombre = StringField('Nombre completo', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    apellidos = StringField('Apellidos', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    codigo = StringField('ID Estudiante', 
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=40)
    ] )
    correo = StringField('Correo Electrónico',
    [ 
        validators.DataRequired('Campo Requerido para contacto'), 
        validators.Length(min=8,max=25) 
    ])
    materia = SelectField(u'Materia', choices=[('m1', 'Materia 1'), ('m2', 'Materia 2'), ('m3', 'Materia 3')])
    guardar = SubmitField('Guardar')