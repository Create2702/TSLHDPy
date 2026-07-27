import matplotlib.pyplot as plt
from metpy.plots import SkewT, Hodograph
from metpy.units import units
from datetime import datetime
from siphon.simplewebservice.wyoming import WyomingUpperAir
import metpy.calc as calc
import requests
from table import open_table
import numpy as np

print('----- TSLHDPy v0.2.2-alpha -----')

while True:
    try:
        year = int(input('>> Year: '))
        month = int(input('>> Month (int): '))
        day = int(input('>> Day: '))
        hour = int(input('>> Hour (UTC): '))
        station = int(input('>> Station number: '))
        print('--------------------------------')
    except ValueError:
        print('Value error. Please try again.')
        continue
    
    while True:
        approval = input(f'Do you want to get data for {year}-{month}-{day} {hour} UTC, station number: {station}? (y/n): ').lower()
        if approval == 'y' or approval == 'n':
            break
        else:
            print('Please enter only "y" or "n".')
    if approval == 'n':
        print('--------------------------------')
        continue
    else:
        print('--------------------------------')
        try:
            date = datetime(year, month, day, hour)
        except ValueError:
            print('Incorrect format.')
            continue

        df = None
        try:
            df = WyomingUpperAir.request_data(date, station)
        except requests.exceptions.ConnectionError:
            print('Connection error. Check your internet and try again.')
            continue
        except ValueError:
            print(f'No data available in {year}-{month}-{day} {hour} UTC or wrong station number. Try again.')
            continue
        except requests.exceptions.HTTPError:
            print('HTTP error. Please try again or download the lastest version of TSLHDPy.')
            continue

        if df is not None:
            pressure = df['pressure'].values * units.hPa
            temperature = df['temperature'].values * units.degC
            dewpoint = df['dewpoint'].values * units.degC
            u_wind = df['u_wind'].values * units.knot
            v_wind = df['v_wind'].values * units.knot
            height = df['height'].values * units.meters
            scale_pressure = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100] * units.hPa
            clean_pressure = pressure >= 150 * units.hPa
            u_h = u_wind[clean_pressure]
            v_h = v_wind[clean_pressure]

            temperature_surface = temperature[0]
            dewpoint_surface = dewpoint[0]
            pressure_surface = pressure[0]
            parcel_line = calc.parcel_profile(pressure, temperature_surface, dewpoint_surface)
            lcl_p, lcl_t = calc.lcl(pressure_surface, temperature_surface, dewpoint_surface)
            lfc_p, lfc_t = calc.lfc(pressure, temperature, dewpoint, parcel_line)
            el_p, el_t = calc.el(pressure, temperature, dewpoint, parcel_line)
            cape, cin = calc.cape_cin(pressure, temperature, dewpoint, parcel_line)
            scale_height = calc.pressure_to_height_std(scale_pressure)
            srh_pos_01, srh_neg_01, srh_01 = calc.storm_relative_helicity(height, u_wind, v_wind, 1 * units.km)
            srh_pos_03, srh_neg_03, srh_03 = calc.storm_relative_helicity(height, u_wind, v_wind, 3 * units.km)
            srh_pos_06, srh_neg_06, srh_06 = calc.storm_relative_helicity(height, u_wind, v_wind, 6 * units.km)
            u_shear, v_shear = calc.bulk_shear(pressure, u_wind, v_wind, height=height, depth=6 * units.km)
            bulk_shear_06 = calc.wind_speed(u_shear, v_shear)
            
            fig = plt.figure(figsize=(10, 10))
            fig.canvas.manager.set_window_title('TSLHDPy - v0.2.2-alpha')
            skew_t = SkewT(fig)

            skew_t.shade_cape(pressure, temperature, parcel_line)
            skew_t.shade_cin(pressure, temperature, parcel_line, dewpoint)
            skew_t.plot(pressure, parcel_line, 'black')
            skew_t.plot(pressure, temperature, 'red')
            skew_t.plot(pressure, dewpoint, 'green')
            if lcl_p == lfc_p and lcl_t == lfc_t:
                skew_t.plot(lcl_p, lcl_t, marker='_', color='yellow', markersize=25, markeredgewidth=3.5, label='The same level of LCL and LFC')
            else:
                skew_t.plot(lcl_p, lcl_t, marker='_', color='pink', markersize=25, markeredgewidth=3.5, label='LCL')
                skew_t.plot(lfc_p, lfc_t, marker='_', color='blue', markersize=25, markeredgewidth=3.5, label='LFC')
            skew_t.plot(el_p, el_t, marker='_', color=(1.0, 0.0784, 0.5765), markersize=25, markeredgewidth=3.5, label='EL')
            skew_t.plot_barbs(pressure[::2], u_wind[::2], v_wind[::2])
            skew_t.ax.set_title(f'Plots powered by TSLHDPy {year}-{month}-{day} {hour} UTC. Station number: {station}')
            skew_t.ax.set_xlabel('Temperature | °C')
            skew_t.ax.set_ylabel('Pressure | hPa')
            skew_t.ax.set_xlim(-50, 40)
            plt.legend()

            height_scale = skew_t.ax.secondary_yaxis(-0.13)
            height_scale.set_yticks(scale_pressure.m, np.round(scale_height.m, 2))
            height_scale.set_ylabel('Height | km')

            fig_h = plt.figure(figsize=(10, 10))
            fig_h.canvas.manager.set_window_title(f'TSLHDPy v0.2.2-alpha')
            ax = plt.subplot(1, 1, 1)
            ax.set_title(f'Plots powered by TSLHDPy {year}-{month}-{day} {hour} UTC. Station number: {station}')
            hodograph = Hodograph(ax, component_range=80)
            hodograph.add_grid()

            hodograph.plot(u_h, v_h, color='red')

            open_table(cape, cin, lcl_p, lfc_p, el_p, srh_01, srh_03, srh_06, bulk_shear_06, year, month, day, hour, station)

            plt.show()
            plt.clf()
            plt.close('all')