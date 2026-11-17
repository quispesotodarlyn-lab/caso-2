# Caso 02 — Costo de transporte agrícola (SENATI)

## Archivos
- `datos.csv`: 130 viajes simulados.
- `entrenar_modelo.py`: entrena `LinearRegression` (80/20) y genera `modelo_transporte.pkl` y `modelo.json`.
- `app.py`, `templates/index.html`, `static/estilos.css`: web en Flask + HTML + CSS (sin JavaScript).

## Pasos
```powershell
pip install -r requirements.txt
python entrenar_modelo.py   # vuelve a crear el .pkl con TU versión de scikit-learn
python app.py               # abre http://127.0.0.1:5000
```

## Resultados (prueba, 26 filas)
- Ecuación: costo = 21.52 + 2.774·km + 0.1073·kg + 26.44·vía_no_asfaltada
- MAE = S/ 17.79 | R² = 0.977
- Prueba 1 (25 km, 400 kg, asfaltada): S/ 133.79
- Prueba 2 (100 km, 1200 kg, no asfaltada): S/ 454.13
