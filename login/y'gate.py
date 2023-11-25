from flask import Flask, render_template, request, redirect , url_for, session, flash
from flask_mysqldb import MySQL
import secrets
import os
import base64
from werkzeug.utils import secure_filename

app= Flask(__name__)

IMG_FOLDER= os.path.join('static', 'IMG')

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= '32358570'
app.config['MYSQL_DB']= 'ygate'
app.static_url_path = '/static'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER']= IMG_FOLDER
app.config['UPLOAD_FOLDER'] = 'static'


ygatelogo= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
ygate= os.path.join(app.config['UPLOAD_FOLDER'], "ygate.png")
ygate1= os.path.join(app.config['UPLOAD_FOLDER'], "ygate1.png")
carrusel1= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.pgn")
carrusel2= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
carrusel3= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
carrusel4= os.path.join(app.config['UPLOAD_FOLDER'], "Y'GATE logo.png")
menu= os.path.join(app.config['UPLOAD_FOLDER'], "menu.svg")
pan= os.path.join(app.config['UPLOAD_FOLDER'], "pan.jpg")
gatos= os.path.join(app.config['UPLOAD_FOLDER'], "gatos.jpg")
postre= os.path.join(app.config['UPLOAD_FOLDER'], "postre.jpg")
ropa= os.path.join(app.config['UPLOAD_FOLDER'], "ropa.jpg")
hambur= os.path.join(app.config['UPLOAD_FOLDER'], "hambur.jpg")
grani= os.path.join(app.config['UPLOAD_FOLDER'], "grani.jpg")
ara= os.path.join(app.config['UPLOAD_FOLDER'], "ara.jpg")
jumbo= os.path.join(app.config['UPLOAD_FOLDER'], "jumbo.jpg")
exito= os.path.join(app.config['UPLOAD_FOLDER'], "exito.jpg")
olimpica= os.path.join(app.config['UPLOAD_FOLDER'], "olimpica.jpg")
colanta= os.path.join(app.config['UPLOAD_FOLDER'], "colanta.jpg")
d1= os.path.join(app.config['UPLOAD_FOLDER'], "d1.jpg")
caru= os.path.join(app.config['UPLOAD_FOLDER'], "caru.jpg")
user= os.path.join(app.config['UPLOAD_FOLDER'], "user.jpg")
add= os.path.join(app.config['UPLOAD_FOLDER'], "boton-mas.png")
delete= os.path.join(app.config['UPLOAD_FOLDER'], "borrar.png")
edit= os.path.join(app.config['UPLOAD_FOLDER'], "editar.png")


mysql=MySQL(app)


@app.route('/')
def principal():
    return render_template('principal.html', logo_image= ygatelogo , carrusel1= carrusel1 ,carrusel2= carrusel2 ,carrusel3= carrusel3,carrusel4= carrusel4  )

@app.route('/suscribirse')
def suscribirse():
    return render_template('suscribirse.html',logo_imag= ygatelogo)

@app.route('/registro_cliente')
def re_cliente():
    return render_template('registro-cliente.html', logo_image= ygatelogo)

@app.route('/registrop', methods=['POST'])
def cliente():
    if request.method == 'POST':
        nombre = request.form['name']
        nombreUsu = request.form['nameuser']
        contraseña = request.form['password']
        email= request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO usuarios (user_name, nombre, correo, contraseña, direccion) VALUES (%s, %s, %s, %s, %s)',(nombreUsu, nombre, email, contraseña, ""))
        mysql.connection.commit()
        return redirect(url_for('interfaz'))

    
@app.route('/interfaz')
def interfaz():
    nombre_usuario = session.get('nombre_usuario', 'Invitado') 
    return render_template('interfaz-usuario.html',nombre_usuario= nombre_usuario ,logo_image= ygatelogo ,user=user,menu= menu, ropa= ropa , gatos= gatos , pan= pan , postre=postre ,hambur= hambur, grani= grani, ara=ara, olimpica=olimpica,exito=exito,colanta=colanta, jumbo=jumbo , d1=d1, caru=caru)


@app.route('/iniciar_sesion')
def iniciar_sesion():
    return render_template('iniciar_sesion.html', logo_image= ygate1)

@app.route('/sesion', methods=['POST'])
def iniciarsesion():
    if request.method == 'POST':
        email = request.form['correo']
        contraseña = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT user_name FROM usuarios WHERE correo = %s  AND contraseña = %s', (email, contraseña))
        user = cursor.fetchone()
        
        if user:
            session['nombre_usuario'] = user[0]  
            return redirect(url_for('interfaz'))
        else:
            return 'Inicio de sesión no válido'
    
    return render_template('iniciar_sesion.html')


@app.route('/sesion_empresa')
def sesion_empresa():
    return render_template('login_empresa.html', logo_image= ygate1)

@app.route('/loginempresa', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        contraseña = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id_empresa, user_name FROM empresas WHERE correo = %s AND contraseña = %s', (email, contraseña))
        company = cursor.fetchone()

        if company:
            session['nombre_empresa'] = company[1]
            session['id_empresa'] = company[0]
            return redirect(url_for('interfaz_empresa'))
        else:
            return 'Inicio de sesión no válido'


@app.route('/planes')
def planes():
    return render_template('planes.html' ,logo_imag= ygatelogo)


@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    if 'user_name' in session:
        session.pop('user_name', None)
    return redirect(url_for('principal'))

@app.route('/registro_empresa')
def empresa():
    return render_template('registro-empresa.html', logo_imag= ygatelogo)

@app.route('/rempresa', methods= ['POST'])
def rempresa():
    if request.method == 'POST' :
        logo=request.files['logo']
        nombre_empresa=request.form['nombre_empresa']
        correo= request.form['correo']
        contraseña= request.form['contraseña']
        contraseñar= request.form['contraseñar']
        direccion= request.form['direccion']
        filename = secure_filename(logo.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if contraseña == contraseñar:
            cursor= mysql.connection.cursor()
            cursor.execute('INSERT INTO empresas(user_name,correo ,contraseña, direccion, logo ) VALUES (%s,%s,%s,%s, %s)',(nombre_empresa,correo,contraseña, direccion,ruta ))
            mysql.connection.commit()
            return redirect(url_for('interfaz_empresa'))
        else:
            flash('las contraseñas no coinciden. vuelve a intentar')
            return redirect(url_for('empresa'))

@app.route('/add_producto')
def add_producto():
    empresa_id = session.get('id_empresa', None)
    company_name = session.get('nombre_empresa', 'Invitado').upper()
    return render_template('agregar_producto.html', llgate=ygate,empresa_id= empresa_id, company_name= company_name, ygate= ygate )

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    global empresa_id
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        foto = request.files["foto"]
        tipo = request.form['tipo']
        tiempo = request.form["tiempo"]
        filename = secure_filename(foto.filename)
        ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        empresa_id = session.get('id_empresa', None) 
        company_name = session.get('nombre_empresa', 'Invitado').upper()
        print(empresa_id)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (nombre_producto, precio, cantidad, tipo,id_empresa,imagen,nombre_empresa,tiempo) VALUES (%s, %s, %s, %s, %s,%s,%s,%s)", (nombre, precio, cantidad, tipo, empresa_id,ruta,company_name,tiempo))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('interfaz_empresa'))
    else:
        return redirect(url_for('add_producto'))




@app.route('/interfaz_empresa')
def interfaz_empresa():
    company_name = session.get('nombre_empresa', 'Invitado').upper()
    empresa_id = session.get('id_empresa', None)  # Change to 'id_empresa'

    if empresa_id is not None:

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM productos WHERE id_empresa = %s', (empresa_id,))
        datos = cursor.fetchall()
        cur= mysql.connection.cursor()
        cur.execute('SELECT logo FROM empresas where id_empresa= {}'.format(empresa_id))
        ruta= cur.fetchall()
        if ruta:
            ruta = [rutas[0] for rutas in ruta]
        
    else:
        flash('No has iniciado sesión como empresa')

    return render_template('interfaz-empresa.html', productos=datos, ygate=ygate, company_name=company_name, id=empresa_id, add=add, delete=delete, edit=edit ,ruta=ruta)



@app.route('/editar_producto')
def editar_producto():
    company_name = session.get('nombre_empresa', 'Invitado').upper()
    empresa_id = session.get('id_empresa', None)
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM productos where id_empresa= {}'.format(empresa_id))
    datos= cur.fetchall()
    cur= mysql.connection.cursor()
    cur.execute('SELECT logo FROM empresas where id_empresa= {}'.format(empresa_id))
    ruta= cur.fetchall()
    if ruta:
        ruta = [rutas[0] for rutas in ruta]
    return render_template('editar_producto.html', productos= datos, company_name= company_name,ruta=ruta)

@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id_producto = {0} '.format(id))
    data = cur.fetchall()

    if request.method == 'POST':
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        tipo = request.form["tipo"]
        precio = request.form["precio"]
        cur.execute('UPDATE productos SET nombre_producto = %s, tipo = %s, precio = %s, cantidad = %s WHERE id_producto = %s', (nombre, tipo, precio, cantidad, id))
        mysql.connection.commit()
        return redirect(url_for('interfaz_empresa'))

    return render_template('editar.html', producto=data[0])


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        tipo = request.form["tipo"]
        precio = request.form["precio"]
        cur = mysql.connection.cursor()
        cur.execute('UPDATE productos SET nombre_producto = %s, tipo = %s, precio = %s, cantidad = %s WHERE id_producto = %s', (nombre, tipo, precio, cantidad, id))
        mysql.connection.commit()

        return redirect(url_for('interfaz_empresa'))

    

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur= mysql.connection.cursor()
    cur.execute('DELETE  FROM productos where id_producto= {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('interfaz_empresa'))

@app.route('/eliminar')
def eliminar1():
    empresa_id = session.get('id_empresa', None)
    cur= mysql.connection.cursor()
    cur.execute('SELECT * FROM productos where id_empresa= {}'.format(empresa_id))
    datos= cur.fetchall()
    return render_template('eliminar.html', productos= datos, id=empresa_id)
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    global empresa_id
    if request.method == "POST":
        id_empresa = session.get('id_empresa', None)
        nombre = request.form.get("buscado")
        cur= mysql.connection.cursor()
        cur.execute("SELECT imagen FROM productos WHERE nombre_empresa = %s", (nombre,))
        rutas = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute("SELECT nombre_producto FROM productos WHERE nombre_empresa = %s", (nombre,))
        nombres = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute("SELECT tiempo FROM productos WHERE nombre_empresa = %s ", (nombre,))
        tiempo = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute("SELECT logo FROM empresas WHERE user_name = %s ", (nombre,))
        logos = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute("SELECT direccion FROM empresas WHERE user_name = %s ", (nombre,))
        direccion = cur.fetchall()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute("SELECT precio FROM productos WHERE nombre_empresa = %s ", (nombre,))
        precio = cur.fetchall()
        cur.close()
        if rutas:
            rutas = [ruta[0] for ruta in rutas]
            logos = [logo[0] for logo in logos]
            precio = [precios[0] for precios in precio]
            direccion = [direcciones[0] for direcciones in direccion]
            
            rutas_nombres = list(zip(rutas, nombres , tiempo,precio))

            return render_template("subidos.html", rutas_nombres=rutas_nombres, nombre=nombre.upper(),logo=logos,direccion=direccion)

        else:
            return "No se encontró"

    return render_template("interfaz-usuario.html")
        
if __name__ == '__main__':
    app.run(debug=True)
