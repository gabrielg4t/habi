from flask import Flask, jsonify,render_template, abort
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = "pruebas"
app.config['MYSQL_PASSWORD'] = "VGbt3Day5R"
app.config['MYSQL_HOST'] = "3.130.126.210"
app.config['MYSQL_PORT'] = 3309
app.config['MYSQL_DB'] = "habi_db"

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def listar_propiedades_disponibles():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT status_history.status_id, " \
              "status.name," \
              "property.address," \
              "property.city," \
              "property.price," \
              "property.description," \
              "property.year " \
              "FROM status_history " \
              "inner join status on status.id = status_history.status_id " \
              "inner join property on status_history.property_id = property.id WHERE name='pre_venta' OR name='en_venta' OR name = 'vendido'"
        cursor.execute(sql)
        datos = cursor.fetchall()
        propiedades=[]
        for fila in datos:
            curso={'Dirección':fila[2],'Ciudad':fila[3], 'Precio de Venta':fila[4], 'Descripcion':fila[5]}
            propiedades.append(curso)
        return jsonify({'propiedades':propiedades})

    except Exception as ex:
        return jsonify({'mensaje':"error"})


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == '__main__':
    app.run(Debug=True)