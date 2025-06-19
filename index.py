#Bienvenidos a nuestro Proyecto de Pagina Web
#En este caso trataremos con una web sencilla
from flask import Flask, render_template, redirect, url_for, flash #complemeto para manejos Web de python
from flask import request
app=Flask(__name__)
app.secret_key = 'super_secret_key_para_flash_messages'
import json
import os

DATA_FILE = 'data.json' ##aqui se cargaran los registro de cada persoona
def load_data(): #definicion que nos ayudara a cargar los datos desde el archivo json
    """Carga los registros desde el archivo JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
                print(f"DEBUG: Datos cargados desde {DATA_FILE}: {data}") # DEBUG
                return data
            except json.JSONDecodeError:
                print(f"DEBUG: Error al decodificar JSON en {DATA_FILE}. Inicializando datos vacios.") # DEBUG
                return {"records": [], "next_id": 1}
    print(f"DEBUG: {DATA_FILE} no encontrado. Inicializando datos vacios.") # DEBUG
    return {"records": [], "next_id": 1}

def save_data(data):#definicion que nos ayudara a guardar los datos desde el archivo json
    """Guarda los registros en el archivo JSON."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"DEBUG: Datos guardados en {DATA_FILE}: {data}") # DEBUG

# Cargar datos al iniciar la aplicacion
app_data = load_data()
registros_db = app_data["records"]
next_id = app_data["next_id"]

def get_next_record_id():
    """Genera un ID unico para un nuevo registro."""
    global next_id
    current_id = next_id
    next_id += 1
    app_data["next_id"] = next_id # Actualizar el ID en los datos de la app
    return current_id

def ordenar_registros(registros, criterio_orden='id', orden_desc=False):
    """
    Ordena una lista de registros por el criterio especificado.
    """
    if not registros:
        return []

    try:
        if criterio_orden == 'edad':
            return sorted(registros, key=lambda x: x.get(criterio_orden, 0), reverse=orden_desc)
        elif criterio_orden in ['nombre', 'ciudad']:
            return sorted(registros, key=lambda x: x.get(criterio_orden, '').lower(), reverse=orden_desc)
        else:
            return sorted(registros, key=lambda x: x.get(criterio_orden, float('inf')), reverse=orden_desc)
    except TypeError:
        flash(f"Advertencia: No se pudo ordenar por '{criterio_orden}' debido a tipos de datos inconsistentes.", 'warning')
        return registros

#rutas de las paginas
@app.route('/')
def principal():
    return render_template('index.html')
@app.route('/Registro')
def Registro():
    return render_template('Registro.html')

@app.route('/lista')
def lista():
    """
    Muestra la lista de registros. Permite ordenar.
    """
    criterio_orden = request.args.get('ordenar_por', 'id')
    registros_ordenados = ordenar_registros(registros_db, criterio_orden)
    return render_template('lista.html', registros=registros_ordenados, current_order=criterio_orden)

@app.route('/Registro', methods=['GET', 'POST'])
def agregar_registro():
    """Permite anadir un nuevo registro."""
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        edad_str = request.form['edad'].strip()
        ciudad = request.form['ciudad'].strip()

        if not nombre or not edad_str or not ciudad:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('Registro.html', data=request.form)

        try:
            edad = int(edad_str)
            if edad <= 0:
                flash('La edad debe ser un numero positivo.', 'error')
                return render_template('Registro.html', data=request.form)
        except ValueError:
            flash('La edad debe ser un numero entero valido.', 'error')
            return render_template('Registro.html', data=request.form)

        nuevo_registro = {
            "id": get_next_record_id(),
            "nombre": nombre,
            "edad": edad,
            "ciudad": ciudad
        }
        registros_db.append(nuevo_registro)
        save_data(app_data)
        flash(f"Registro de '{nombre}' anadido exitosamente.", 'success')
        return redirect(url_for('lista'))
    return render_template('Registro.html', data={})
@app.route('/editar/<int:registro_id>', methods=['GET', 'POST'])
def editar_registro(registro_id):
    """
    Permite editar un registro existente por su ID.
    """
    print(f"DEBUG: Intentando editar registro con ID: {registro_id}") # DEBUG
    registro = next((r for r in registros_db if r["id"] == registro_id), None)

    if not registro:
        print(f"DEBUG: Registro con ID {registro_id} NO encontrado. Redirigiendo a index.") # DEBUG
        flash('Registro no encontrado.', 'error')
        return redirect(url_for('index'))

    print(f"DEBUG: Registro encontrado para editar: {registro}") # DEBUG
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        edad_str = request.form['edad'].strip()
        ciudad = request.form['ciudad'].strip()

        if not nombre or not edad_str or not ciudad:
            flash('Todos los campos son obligatorios.', 'error')
            return render_template('editar.html', registro=registro)

        try:
            edad = int(edad_str)
            if edad <= 0:
                flash('La edad debe ser un numero positivo.', 'error')
                return render_template('edit.html', registro=registro)
        except ValueError:
            flash('La edad debe ser un numero entero valido.', 'error')
            return render_template('edit.html', registro=registro)

        registro['nombre'] = nombre
        registro['edad'] = edad
        registro['ciudad'] = ciudad
        save_data(app_data)
        flash(f"Registro de '{nombre}' (ID: {registro_id}) actualizado exitosamente.", 'success')
        return redirect(url_for('lista'))
    return render_template('editar.html', registro=registro)

@app.route('/borrar/<int:registro_id>')
def delete_registro(registro_id):
    """
    Permite eliminar un registro por su ID.
    """
    global registros_db
    registros_db = [r for r in registros_db if r["id"] != registro_id]
    return redirect(url_for('lista'))
@app.route('/Recetas')

def Recetas():
    return render_template('Recetas.html')
if __name__=="__main__":
    app.run(debug=True, port=5017) 

