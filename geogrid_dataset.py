import os
import subprocess
import numpy as np
from global_land_mask import globe
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

env = Environment(loader=FileSystemLoader('/data/for_proj'))
template_wps = env.get_template('template_geo_namelist.wps')

geogrid = {
    'OUTPUT_PATH': '"/data/for_proj/geogrid_runs_test/"',
    'DATA_PATH': '"/data/WPS_GEOG/"'
}
n_domains = 200 #вычисляется доменов каждого вида -> 200
train_dims = [100, 120, 140, 160, 180]
for we in tqdm(train_dims):
    for sn in train_dims:
        for idx in range(30, n_domains + 30):
            while True:
                geogrid['LAT'] = np.random.rand() * 120 - 50
                geogrid['LON'] = np.random.rand() * 360 - 180
                if geogrid['LAT'] > 60 and geogrid['LON'] > -55 and geogrid['LON'] < -25: continue
                if globe.is_land(geogrid['LAT'], geogrid['LON']): break
            geogrid['E_WE'] = we
            geogrid['E_SN'] = sn
            config_wps = template_wps.render(geogrid)
            # with open(os.path.join('namelist.wps'), "w") as file:
            with open(os.path.join('/home/wrfuser/WPS/namelist.wps'), "w") as file:
                file.write(config_wps)
            code = subprocess.call(['/home/wrfuser/WPS/geogrid.exe'], stdout=subprocess.DEVNULL, cwd='/home/wrfuser/WPS/', stderr=subprocess.DEVNULL)
            os.rename(os.path.join(geogrid['OUTPUT_PATH'][1:-1], 'geo_em.d01.nc'), os.path.join(geogrid['OUTPUT_PATH'][1:-1], f'geo_em.{we}x{sn}.{idx}.nc'))
            # os.rename(os.path.join(geogrid['OUTPUT_PATH'][1:-1], 'geo_em.d01.nc'), os.path.join(geogrid['OUTPUT_PATH'][1:-1], 'geo_em.{}x{}.{}.nc'.format(we, sn, idx)))

            if code != 0:
                print(idx, code)