from astropy.io import fits  
from astropy.table import Table
import matplotlib.pyplot as plt 
import os 


# hdu=fits.open("/mnt/d/ExtractSpec/WHT_140624/reduce_wht_isis_red/1.0/Masters/MasterWaveCalib_A_1_DET01.fits")
#hdu=fits.open("/mnt/d/ExtractSpec/WHT_140624/reduce_wht_isis_red/1.0/Masters/MasterWaveCalib_A_1_DET01.fits")
hdu=fits.open(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Calibrations\WaveCalib_A_0_DET01.fits") 

plt.plot(hdu[2].data['wave_soln'][0],hdu[2].data['spec'][0]) 
plt.show()

# params={0:None,1:{'BINSPEC':1}} 
# datas={0:None,1:{'wave':{'data':hdu[2].data['wave_soln'][0],'fmt':'D','unit':'Angstrom'},\
# 				 'flux':{'data':hdu[2].data['spec'][0]     ,'fmt':'D','unit':None}}}

datas=Table({'wave':hdu[2].data['wave_soln'][0],'flux':hdu[2].data['spec'][0]}, meta={'BINSPEC':1})
#datas.write("/mnt/d/ExtractSpec/J1502_WHT/wht_isis_blue_R300B.fits")
datas.write(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Calibrations\ljt_yfosc_Gr3.fits", overwrite=True)