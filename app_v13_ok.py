from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from flask import send_from_directory

from datetime import datetime
import os

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS # Guardamos la ruta como un valor en la app

#explicado en el pdf clase 33-35 desarrollando aplicacion web
app.secret_key="programacodoacodo"

# Creo ruta /uploads , con esto de aca vamos a poder  mostrar la foto dice, osea no solo con el codigo del html
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['UPLOADS'], nombreFoto)


# CARGAMOS LOS DATOS DE LA TABLA EMPLEADOS DE LA BD Y LA ENVIAMOS PARA CREAR LA TABLA PARA MOSTRAR
@app.route('/')
def index():
    sql = "SELECT * FROM empleados;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    empleados = cursor.fetchall()

    conn.commit()

    return render_template('empleados/index_v13.html', empleados=empleados)


@app.route('/create')
def create():
    return render_template('empleados/create_v13.html')


# ESTE ES EL CODIGO DEL BOTON BORRAR DE LA TABLA
@app.route('/delete/<int:id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()#ES EL INTERMEDIARIO

    sql = "SELECT foto FROM empleados WHERE id=%s"
    cursor.execute(sql, id)

    nombreFoto = cursor.fetchone()[0]
    os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))

    sql = "DELETE FROM empleados WHERE id=%s"
    cursor.execute(sql, id)

    conn.commit()

    return redirect('/')

# CODIGO DEL BOTON Modificar
@app.route('/modify/<int:id>')
def modify(id):
    sql = "SELECT * FROM empleados WHERE id=%s"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)

    empleado = cursor.fetchone()#INVESTIGAR QUE HACE FETCHONE ???????????????????????????????

    conn.commit()

    return render_template('empleados/edit_v13.html', empleado=empleado)

#CODIGO CUANDO HAGO EL UPDATE, APRIETO EL BOTON MODIFICAR
@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtID']

    datos = (_nombre, _correo, id)

    conn = mysql.connect()
    cursor = conn.cursor()

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

        sql = "SELECT foto FROM empleados WHERE id=%s"
        cursor.execute(sql, id)

        nombreFoto = cursor.fetchone()[0]

        os.remove(os.path.join(app.config['UPLOADS'], nombreFoto))
        sql = "UPDATE empleados SET foto=%s WHERE id=%s"
        cursor.execute(sql, (nuevoNombreFoto, id))
        conn.commit()

    sql = "UPDATE empleados SET nombre=%s, correo=%s WHERE id=%s;"
    cursor.execute(sql, datos)

    conn.commit()

    return redirect('/')


#CODIGO PARA CUANDO CREAMOS E INSERTAMOS UN REGISTRO EN LA BASE DE DATOS.
@app.route('/store', methods=['POST'])
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    print(_foto)

    # COMPROBACION DE INGRESAR DATOS EN EL FORMULARIO
    if _nombre == '' or _correo == '' or _foto == '':
        flash('Faltan datos del Empleado.') #CARTEL FALTAN DATOS DEL EMPLEADO
        return redirect(url_for('create'))

    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + '_' + _foto.filename
        _foto.save("uploads/" + nuevoNombreFoto)

    sql = "INSERT INTO empleados (nombre, correo, foto) values (%s, %s, %s);"

    datos = (_nombre, _correo, nuevoNombreFoto)

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
