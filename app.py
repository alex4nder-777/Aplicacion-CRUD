from flask import Flask, render_template,request,redirect,url_for
import os
import database as db

app = Flask(__name__)
@app.route("/")
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    myresult = cursor.fetchall()
    #convertir los datos a diccionario
    inser_object = []
    column_name = [column[0] for column in cursor.description]
    for record in myresult:
        inser_object.append(dict(zip(column_name, record)))
    cursor.close()    
    return render_template('index.html', data = inser_object)

#ruta para guardar usuarios en la base de datos
@app.route('/user', methods=['POST'])
def add_user():
    user_name = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if user_name and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO usuarios (username, name, password) VALUES (%s, %s, %s)"
        data = (user_name, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))    

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuarios WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])

def edit(id):
    user_name = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if user_name and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE usuarios SET username =%s,name=%s, password=%s WHERE id =%s"
        data = (user_name, name, password,id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run("127.0.0.1", port="8080", debug=True)