import matplotlib.pyplot as plt
import math

def check(param):
    if math.isnan(param):
        return '-'
    else:
        return param

def check_for_round(param):
    if param == '-':
        return '-'
    else:
        return round(param)

def open_table(cape, cin, lcl, lfc, el, year, month, day, hour, station) -> None:
    table = plt.figure(figsize=(10, 10))
    table.canvas.manager.set_window_title(f'TSLHDPy v0.1.0-alpha ({year}-{month}-{day} {hour} UTC. Station number: {station})')
    ax = table.add_subplot(111)
    ax.axis('off')
    text = f'CAPE: {check_for_round(check(cape.m))} J/kg\nCIN: {check_for_round(check(cin.m))} J/kg\nLCL: {check_for_round(check(lcl.m))} hPa\nLFC: {check_for_round(check(lfc.m))} hPa\nEL: {check_for_round(check(el.m))} hPa'
    ax.text(0.05, 0.95, text, fontsize=16)
    plt.show()
    plt.close(table)


