from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, DateField, IntegerField, PasswordField, SubmitField, SelectField, validators, ValidationError
import email_validator

class LoginForm(FlaskForm):
    login = StringField('Логин', [validators.InputRequired()])
    password = PasswordField('Пароль', [validators.InputRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    names = []
    logins = []
    
    nickname = StringField('Ник в системе', [validators.Length(min=4, max=32), validators.NoneOf( names, message='Пользователь с таким именем уже существует')])
    system_role = SelectField('Доступ в системе', [validators.InputRequired()], id='select_system_role')
    '''
    secondname = StringField('Фамилия', [validators.Length(min=2, max=20)])
    firstname = StringField('Имя', [validators.Length(min=2, max=20)])
    surname = StringField('Отчество', [validators.Length(min=2, max=20)])
    '''
    email = StringField('E-mail', [validators.Length(min=6, max=64), validators.Email()])
    login = StringField('Логин', [validators.Length(min=4, max=25), validators.NoneOf( logins, message='Пользователь с таким логином уже существует! Пожалуйста, выберите другой')])
    password = PasswordField('Пароль', [validators.InputRequired(), 
                                        validators.Length(min=6, max=64), 
                                        validators.EqualTo('confirm', message='Пароли должны совпадать')])
    confirm  = PasswordField('Повторите пароль')
    submit = SubmitField('Создать новую учетную запись')

class TaskAddForm(FlaskForm):
    name = StringField('Название', [validators.Length(min=0, max=64)])
    descr = StringField('Описание', [validators.Length(min=0,max=600)])
    stage = SelectField('Этап выполнения', [validators.InputRequired()], id='select_stage')
    priority = SelectField('Приоритет', [validators.InputRequired()], id='select_priority')
    tasktype = StringField('Тип задачи', [validators.Length(min=0,max=32)])
    taskfield = StringField('Вид работ', [validators.Length(min=0,max=32)])
    user = SelectField('Ответственное лицо', [validators.InputRequired()], id='select_user')
    
    submit = SubmitField('Создать')
    
'''
class EditUserForm(FlaskForm):
    
    submit = SubmitField('Сохранить')
    
class TaskEditForm(FlaskForm):
    
    submit = SubmitField('Сохранить')
    
class CommentAddForm(FlaskForm):
    
    submit = SubmitField('Отправить')
    
class CommentEditForm(FlaskForm):
    
    submit = SubmitField('Сохранить')
    
class ProjectAddForm(FlaskForm):
    submit = SubmitField('Создать')
    
class ProjectEditForm(FlaskForm):
    
    submit = SubmitField('Сохранить')
'''
