from astropy.io import fits 
import matplotlib.pyplot as plt 
import sys 
import numpy as np 
from astropy.table import Table 

if True: 
    hdu=fits.open(r"D:\ExtractSpec\wNeon.fits") 
    flux = hdu[0].data 
    wave = hdu[0].header['CRVAL1'] + hdu[0].header['CD1_1']*(np.arange(len(flux))-1) 
    plt.plot(wave, flux) 

    hdu=fits.open(r"D:\ExtractSpec\2M4\251013\251013_test\ljt_yfosc_A\Calibrations\WaveCalib_A_0_DET01.fits") 
    wave = hdu[2].data['wave_soln'][0] 
    flux = hdu[2].data['spec'][0]*10
    plt.plot(wave, flux) 
    plt.show() 
    

if False: 
    data= Table.read(r"D:\ExtractSpec\cwobject.txt")
    plt.plot(data['wave'])
    hdu=fits.open(r"D:\ExtractSpec\WFST0742frfr_1d.fits") 
    flux = hdu[0].data*1e17
    wave = hdu[0].header['CRVAL1'] + hdu[0].header['CD1_1']*(np.arange(len(flux))-1)
    print(hdu[0].data) 

    plt.plot(wave, flux) 
    plt.show()  


    hdu=fits.open(r"D:\ExtractSpec\2M4\251013\251013_test\ljt_yfosc_A\coadd1d_ljg2m401-yf01-20251018-0186-e00-BD+28d4211\AT2025zow_spat0709.fits") 
    redshift= 6779/6563-1
    # redshift= 0 

    wave, flux =hdu[1].data['wave'], hdu[1].data['flux'] 
    ind= wave> 0 
    wave, flux = wave[ind], flux[ind]
    plt.plot(wave/(1+redshift), flux) 

    hdu=fits.open(r"D:\ExtractSpec\AT2025zow_1d.fits") 
    flux = hdu[0].data*1e17
    wave = hdu[0].header['CRVAL1'] + hdu[0].header['CD1_1']*(np.arange(len(flux))-1)
    print(flux) 

    plt.plot(wave/(1+redshift) , flux) 
    plt.show() 