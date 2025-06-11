#Bienvenidos a nuestro Proyecto de Pagina Web
#En este caso trataremos con una web sencilla
from flask import Flask, render_template #complemeto para manejos Web de python
app=Flask(__name__)

"""
@app.route('/')  #con este codigo podemos darle una ruta de vista
                 #previa a nuestra pagina
def principal ():
    return "Bienvenidos Unexpo Empresa Auto 2" #Aqui visualizamos el nombre
@app.route('/Registro')
def Registro():
    return "Registro de Usuario"
"""
@app.route('/')
def principal():
    return render_template('index.html')
@app.route('/Registro')
def Registro():
    return render_template('Registro.html')
if __name__=="__main__":
    app.run(debug=True, port=5017) 

