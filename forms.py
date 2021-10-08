from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators

class Formulario_Usuario(Form):
    usuario = StringField('Usuario', 
    [ 
        validators.DataRequired(), 
        validators.Length(min=8,max=25)
    ] )
    password = PasswordField('Contraseña',
    [ 
        validators.DataRequired(), 
        validators.Length(min=8,max=25) 
    ])
    recordar = BooleanField('Recordar usuario')
    enviar = SubmitField('Iniciar sesión')
    

