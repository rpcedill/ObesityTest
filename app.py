import pickle
from flask import Flask, request, render_template
#import joblib
import array as ar
import pandas as pd
import numpy as np


app = Flask(__name__)
#model = joblib.load('model_jlib')
model = pickle.load(open('model2.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')
  

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == "POST":
        arrayPred = ar.array("f", range(20))
        for i in range(0, 20):
            arrayPred[i] = 0
        genero = int(request.form.get("genero"))
        arrayPred[genero] = 1
        edad = int(request.form.get('edad'))
        arrayPred[15] = edad
        famSobre = int(request.form.get('pre3'))
        arrayPred[16] = famSobre
        altoCalo = int(request.form.get('pre4'))
        arrayPred[17] = altoCalo
        snack = int(request.form.get('pre7'))
        arrayPred[snack] = 1
        monitoreo = int(request.form.get('pre10'))
        arrayPred[18] = monitoreo
        actividad = int(request.form.get('pre11'))
        arrayPred[19] = actividad
        alcohol = int(request.form.get('pre13'))
        arrayPred[alcohol] = 1
        transpo = int(request.form.get('pre14'))
        arrayPred[transpo] = 1

        d2 = {'MTRANS_Automobile': [arrayPred[0]], 'MTRANS_Bike': [arrayPred[1]], 'MTRANS_Motorbike': [arrayPred[2]],
            'MTRANS_Public_Transportation': [arrayPred[3]],
            'MTRANS_Walking': [arrayPred[4]],
            'Gender_Female': [arrayPred[5]], 'Gender_Male': [arrayPred[6]],
            'CALC_Always': [arrayPred[7]], 'CALC_Frequently': [arrayPred[8]], 'CALC_Sometimes': [arrayPred[9]],
            'CALC_no': [arrayPred[10]],
            'CAEC_Always': [arrayPred[11]], 'CAEC_Frequently': [arrayPred[12]], 'CAEC_Sometimes': [arrayPred[13]],
            'CAEC_no': [arrayPred[14]],
            'Age': [arrayPred[15]], 'FHWO': [arrayPred[16]], 'FAVC': [arrayPred[17]], 'SCC': [arrayPred[18]],
            'FAF': [arrayPred[19]]} 

        
        df2 = pd.DataFrame(data=d2)


        prediction = model.predict(df2[:1])
        prediction = str(np.argmax(prediction))
        match prediction:
            case "0":
                return render_template('recomendaciones.html', prediction_text='Insuficiente Peso', 
                recomendacion1="Consumir alimentos ricos en calorías y nutrientes, como frutas, verduras, proteínas y carbohidratos complejos.", 
                recomendacion2="Consumir alimentos ricos en grasas saludables, como aguacate, nueces y semillas.", 
                recomendacion3="Hacer ejercicios de resistencia para aumentar la masa muscular.")
            case "1":
                return render_template('recomendaciones.html', prediction_text='Peso Normal', 
                recomendacion1="Mantener la dieta balanceadaa en nutrientes.", 
                recomendacion2="Evitar consumir alcohol y tabaco.", 
                recomendacion3="Beber suficiente agua y limitar el consumo de bebidas con alto contenido calórico.")
            case "2":
                return render_template('recomendaciones.html', prediction_text='Sobrepeso Nivel I', 
                recomendacion1="Aumentar la actividad física, como ir por una caminata o natación. Apuntar al menos a hacer 150 minutos moderado de actividad aerobica.", 
                recomendacion2="Monitorear las porciones de comida.", 
                recomendacion3="Apuntar a dormir 8 horas, ya que puede afectar al peso y a la salud en general.")
            case "3":
                return render_template('recomendaciones.html', prediction_text='Sobrepreso Nivel II', 
                recomendacion1="Implementar metas mesurables sobre pérdida de peso.", 
                recomendacion2="Incorporar ejercicios de fuerza entre 2-3 veces a la semana.", 
                recomendacion3="Evitar consumir comidas altas en azúcar.")
            case "4":
                return render_template('recomendaciones.html', prediction_text='Obesidad Tipo I', 
                recomendacion1="Fijar metas realistas sobre la pérdidad de peso, como perder entre 5-10% del peso corporal en los primeros 6 meses.", 
                recomendacion2="Seguir una dieta basada en tus necesidades y preferencias.", 
                recomendacion3="Buscar apoyo de un profesional de la salud.")
            case "5":
                return render_template('recomendaciones.html', prediction_text='Obesidad Tipo II', 
                recomendacion1="Incorporar entrenamiento de fuerza entre 2-3 días a la semana.", 
                recomendacion2="Incorporar terapia conductual, terapia cognitiva u otra forma de terapia para manejar los aspectos psicológicos de la obesidad.", 
                recomendacion3="Buscar apoyo médico multidisciplinario.")
            case "6":
                return render_template('recomendaciones.html', prediction_text='Obesidad Tipo III', 
                recomendacion1="Consultar con un equipo multidisciplinario de médicos para desarrollar un plan de pérdida de peso personalizado.", 
                recomendacion2="Revisar otro tipo de enfermedades provenientes de la obesidad como diabetes, hipertensión o apnea del sueño.", 
                recomendacion3="Considerar una cirugía bariátrica.")

if __name__ == "__main__":
    app.run()