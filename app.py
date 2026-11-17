# CASO 02 | Estimación de costo de transporte agrícola - SENATI
# Flask + HTML + CSS (sin JavaScript). Usa el modelo guardado en modelo_transporte.pkl.

from pathlib import Path
import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
carpeta = Path(__file__).resolve().parent

# Cargamos el modelo entrenado con entrenar_modelo.py (una sola vez).
paquete = joblib.load(carpeta / 'modelo_transporte.pkl')
modelo = paquete['modelo']
columnas = paquete['columnas']
rangos = paquete['rangos']
mae = paquete['mae']
r2 = paquete['r2']


def leer_numero(texto):
    """Convierte el texto del formulario en número (acepta coma decimal)."""
    return float(texto.replace(',', '.'))


@app.route('/', methods=['GET', 'POST'])
def inicio():
    resultado = None
    error = ''
    # Valores que el usuario escribió, para no perderlos al recargar.
    escritos = {'distancia_km': '', 'carga_kg': '', 'via_no_asfaltada': '0'}

    if request.method == 'POST':
        for campo in escritos:
            escritos[campo] = request.form.get(campo, '').strip()

        try:
            distancia = leer_numero(escritos['distancia_km'])
            carga = leer_numero(escritos['carga_kg'])
            via = int(escritos['via_no_asfaltada'])

            # Validación de rangos pedida en el caso.
            d_min, d_max = rangos['distancia_km']
            c_min, c_max = rangos['carga_kg']
            if not d_min <= distancia <= d_max:
                error = f'La distancia debe estar entre {d_min} y {d_max} km.'
            elif not c_min <= carga <= c_max:
                error = f'La carga debe estar entre {c_min} y {c_max} kg.'
            elif via not in (0, 1):
                error = 'El tipo de vía solo puede ser 0 (asfaltada) o 1 (no asfaltada).'
            else:
                # DataFrame con los mismos nombres de columna del entrenamiento.
                fila = pd.DataFrame([[distancia, carga, via]], columns=columnas)
                costo = max(modelo.predict(fila)[0], 0)
                resultado = {
                    'costo': f'{costo:,.2f}',
                    'minimo': f'{max(costo - mae, 0):,.0f}',
                    'maximo': f'{costo + mae:,.0f}',
                }
        except ValueError:
            error = 'Escribe valores numéricos válidos en todos los campos.'

    return render_template('index.html', resultado=resultado, error=error,
                           escritos=escritos, rangos=rangos, mae=mae, r2=r2)


if __name__ == '__main__':
    # debug=True solo para practicar en la computadora.
    app.run(debug=True)
