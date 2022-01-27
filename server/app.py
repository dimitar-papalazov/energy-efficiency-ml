from flask import Flask, render_template, request
from model import predict_cooling, predict_heating, get_heating_score, get_cooling_score

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
  heating_load_accuracy = round(get_heating_score(), 2)
  cooling_load_accuracy = round(get_cooling_score(), 2)
  if request.method == 'GET':
    return render_template('index.html', heating_load_accuracy = int(heating_load_accuracy * 100), cooling_load_accuracy = int(cooling_load_accuracy * 100))
  else:
    if len(request.form) and request.form['relative_compactness'] != '' and request.form['surface_area'] != '' and request.form['wall_area'] != '' and request.form['roof_area'] != '' and request.form['height'] != '':
      arguments = [float(request.form['relative_compactness']), float(request.form['surface_area']), float(request.form['wall_area']), float(request.form['roof_area']), float(request.form['height']), float(request.form['orientation']), float(request.form['glazing_area']), float(request.form['glazing_variation'])]

      heating_load = predict_heating(arguments)
      heating_load_mistake = heating_load * (1 - heating_load_accuracy)
      heating_load_range = str(round(heating_load - heating_load_mistake, 2)) + '-' + str(round(heating_load + heating_load_mistake, 2)) + ' kWh/m²' 
      heating_load = str(round(heating_load, 2)) + ' kWh/m²'      

      cooling_load = predict_cooling(arguments)
      cooling_load_mistake = cooling_load * (1 - cooling_load_accuracy)
      cooling_load_range = str(round(cooling_load - cooling_load_mistake, 2)) + '-' + str(round(cooling_load + cooling_load_mistake, 2)) + ' kWh/m²' 
      cooling_load = str(round(cooling_load, 2)) + ' kWh/m²'      

      return render_template('index.html', heating_load_accuracy = int(heating_load_accuracy * 100), cooling_load_accuracy = int(cooling_load_accuracy * 100), heating_load=heating_load, cooling_load=cooling_load, heating_load_range=heating_load_range, cooling_load_range=cooling_load_range)
    return render_template('index.html', heating_load_accuracy = int(heating_load_accuracy * 100), cooling_load_accuracy = int(cooling_load_accuracy * 100), bad_input=True)


if __name__ == '__main__':
  app.run('0.0.0.0', 8000, True)