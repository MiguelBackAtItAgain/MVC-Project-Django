# MVC-Project-Django

## **Created by:** Miguel Brito

### Instalación de Django en ordenador local

Se recomienda seguir los pasos del siguiente [video] https://www.youtube.com/watch?v=eJdfsrvnhTE&list=PLgxHOcP9p_XzR0hc0i3crV4hneFprmReO&index=1&t=154s

### Servicios requeridos

SQLite

### Dependencias

Ejecutar `pip install -r requirements.txt`

### Base de datos

Usar `python manage.py migrate` dentro de la carpeta de 'mvc' más externa para crear la base de datos.

Usar `python manage.py makemigrations` dentro de la carpeta de 'mvc' más externa para agregar las tablas a la base.

### Correr el proyecto

De querer acceder al panel de administrador, correr los siguientes comandos:

    python manage.py shell
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_superuser(name='su nombre', username='su nombre de usuario', password='su contraseña', idnumber='su cédula', gender='su género', birthdate='su fecha de nacimiento (YYYY-MM'DD)', email='su email', phonenum='su numero de teléfono', address='su dirección') 


Usar `python manage.py runserver` dentro de la carpeta "mvc" más externa para iniciar el programa.










