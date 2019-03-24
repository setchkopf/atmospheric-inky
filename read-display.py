# -*- coding: utf-8 -*-

#!/usr/bin/env python
import bme680
import time

#set up previous reading for comparison
previous_t = 0
previous_p = 0
previous_h = 0
previous_q = 0

current_t
current_p
current_h
current_q

print("""Display Temperature, Pressure, Humidity and Gas

Press Ctrl+C to exit

""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)

print('\n\nPolling:')
#set refresh rate
t_refresh = 6 
#standard air quality (Ohms)
gas_baseline = 150000
hum_weighting = 0.25
hum_baseline = 40
try:
    while True:
        if sensor.get_sensor_data():
            current_t = round(sensor.data.temperature)
            current_p = round(sensor.data.pressure)
            current_h = round(sensor.data.humidity)

            output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                current_t,
                current_p,
                current_h)

            if sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                gas_offset = gas_baseline - gas
                hum_offset = current_h - hum_baseline

                if hum_offset > 0:
                    hum_score = (100 - hum_baseline - hum_offset)
                
                else:
                    hum_score = (hum_baseline + hum_offset)

                hum_score /= (100 - hum_baseline)
                hum_score *= (hum_weighting * 100)

                if gas_offset > 0:
                    gas_score = (gas/gas_baseline)
                    gas_score *= (100 - (hum_weighting * 100))

                else:
                    gas_score = 100 - (hum_weighting *100)

                current_q = round(hum_score + gas_score)

                print('{0},{1} Ohms'.format(
                    output,
                    current_q))

            else:
                print(output)

            parse_data()

        time.sleep(t_refresh)

except KeyboardInterrupt:
    pass

degree_sign = u'\N{DEGREE SIGN}'
def parse_data()
   if (current_t != previous_t) or (current_p != previous_p) or (current_h != previous_h) or (current_q != previous_q)
       previous_t = current_t
       previous_p = current_p
       previous_h = current_h
       previous_q = current_q

       #display readings 
       #degree_signC
       #hPa
       #%
       #IAQ

       #display time

       #TODO - construct image


