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

def open_table(cape, cin, lcl, lfc, el, srh_01, srh_03, srh_06, blk_shr_06, year, month, day, hour, station) -> None:
    table = plt.figure(figsize=(10, 10))
    table.canvas.manager.set_window_title(f'TSLHDPy v0.1.0-alpha ({year}-{month}-{day} {hour} UTC. Station number: {station})')
    ax = table.add_subplot(111)
    ax.axis('off')
    
    text = (
        f'CAPE: {check_for_round(check(cape.m))} J/kg\n'
        f'CIN: {check_for_round(check(cin.m))} J/kg\n'
        f'LCL: {check_for_round(check(lcl.m))} hPa\n'
        f'LFC: {check_for_round(check(lfc.m))} hPa\n'
        f'EL: {check_for_round(check(el.m))} hPa\n'
        f'SRH 0-1 km: {check_for_round(check(srh_01.m))} $m^2/s^2$\n'
        f'SRH 0-3 km: {check_for_round(check(srh_03.m))} $m^2/s^2$\n'
        f'SRH 0-6 km: {check_for_round(check(srh_06.m))} $m^2/s^2$\n'
        f'Bulk Shear 0-6 km:  {check_for_round(check(blk_shr_06.m))} knots\n'
    )
    ax.text(0.05, 0.95, text, fontsize=16, fontfamily='monospace', va='top')
    
