from flask import Flask, jsonify,render_template, abort
from flask_mysqldb import MySQL

app = Flask(__name__)

####### Variables de Conexion Mysql #######

app.config['MYSQL_USER'] = "pruebas"
app.config['MYSQL_PASSWORD'] = "VGbt3Day5R"
app.config['MYSQL_HOST'] = "3.130.126.210"
app.config['MYSQL_PORT'] = 3309
app.config['MYSQL_DB'] = "habi_db"

mysql = MySQL(app)

####### Funcion que sólo lista todas las propiedades Disponibles con el estatus "pre_venta", "en_venta", "vendido" #######
####### Se imprimen via REST en formato JSON entrando al directorio raiz #######

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
              "inner join property on status_history.property_id = property.id where name NOT LIKE ('comp%')"
        cursor.execute(sql)
        datos = cursor.fetchall()
        propiedades=[]
        for fila in datos:
            propiedad={'Dirección':fila[2],'Ciudad':fila[3], 'Precio de Venta':fila[4], 'Descripcion':fila[5]}
            propiedades.append(propiedad)
        return jsonify({'Propiedades Disponibles':propiedades})

    except Exception as ex:
        return jsonify({'Error': "No existen resultados que coincidan con esa busqueda"})



####### Esta funcion lista todas las propiedades disponibles con el filtro anterior y añade 3 parametros más #######
####### los cuales corresponden a los filtros de ciudad, fecha de construccion y estado de venta en el que se encuentra el inmueble #######
####### para obtener estos resusltados tendremos que pasar los parametros seguidos de '/' ej. http://127.0.0.1:5000/bogota/2000/pre_venta
####### de existir algun error o no existir coincidencias con la busqueda se mostrara el mensaje de "Error"

@app.route('/<ciudad>/<fecha_construccion>/<estado>', methods=['GET'])
def listar_por_cuidad_fecha_estado(ciudad, fecha_construccion, estado):
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
              "inner join property on status_history.property_id = property.id where name NOT LIKE ('comp%') AND (city='{}') AND (year = '{}' AND (name = '{}'))".format(ciudad, fecha_construccion, estado)
        cursor.execute(sql)
        datos = cursor.fetchall()
        propiedades = []
        for fila in datos:
            propiedad = {'Dirección': fila[2], 'Ciudad': fila[3], 'Precio de Venta': fila[4], 'Descripcion': fila[5]}
            propiedades.append(propiedad)

        if propiedades == []:
            return jsonify({'No existen resultados que coincidan con esa busqueda'})
        else:
            return jsonify({'Propiedades Disponibles': propiedades})

    except Exception as ex:
        return jsonify({'Error': "No existen resultados que coincidan con esa busqueda"})


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == '__main__':
    app.run(debug=True)