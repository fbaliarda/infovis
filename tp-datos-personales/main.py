import os

import pandas as pd
from pykml import parser
import re
import dateutil.parser, dateutil.tz

DAY_NAMES = { 'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles', 'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sabado', 'Sunday': 'Domingo'}
if __name__ == '__main__':
    processed_data = {'Día': [], 'Camino': [], 'Comienzo': [], 'Llegada': [], 'Tiempo (min)': [], 'Distancia': []}
    for filename in os.listdir('../raw'):
        with open(os.path.join('../raw', filename), 'r', encoding='utf-8') as f:
            root = parser.parse(f).getroot()
            returning = False
            trip_completed = False
            for placemark in root.Document.Placemark:
                if placemark.name == 'Driving':
                    data = re.search('Driving from (.+?) to (.+?). Distance (.+?)m', placemark.description.text)
                    start, end, distance = \
                        dateutil.parser.isoparse(data.group(1)).astimezone(dateutil.tz.tzlocal()),\
                        dateutil.parser.isoparse(data.group(2)).astimezone(dateutil.tz.tzlocal()),\
                        int(data.group(3))
                    processed_data['Día'].append(DAY_NAMES[start.strftime('%A')])
                    processed_data['Camino'].append('Vuelta' if returning else 'Ida')
                    processed_data['Comienzo'].append(start.strftime("%Y-%m-%dT%H:%M:%S"))
                    processed_data['Llegada'].append(end.strftime("%Y-%m-%dT%H:%M:%S"))
                    processed_data['Tiempo (min)'].append('%.1f' % ((end - start).total_seconds() / 60))
                    processed_data['Distancia'].append(distance)
                    trip_completed = returning
                    returning = True
                if trip_completed:
                    break
    df = pd.DataFrame(data=processed_data)
    df.to_csv('rutas.csv', encoding='utf-8-sig', index=False)
    print(processed_data)

