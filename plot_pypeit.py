from astropy.io import fits 
import matplotlib.pyplot as plt 
import sys 
import numpy as np 
from astropy.table import Table 

if False: 
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
    # data= Table.read(r"D:\ExtractSpec\cwobject.txt")
    # plt.plot(data['wave'])
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

    hdu=fits.open(r"D:\ExtractSpec\2M4\251013\251013_test2\ljt_yfosc_A\telluric_ljg2m401-yf01-20251018-0186-e00-BD+28d4211\AT2025zow_spat0709_tellcorr.fits") 
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

if False: 
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r\p200_ngps_r_B\coadd1d_ngps2512130022-BD28d4211NGPS\TDE2025aarm_spat0242.fits") 
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r_SNR100\p200_ngps_r_B\coadd1d_ngps2512130022-BD28d4211NGPS\TW2236_spat0239.fits")
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r\p200_ngps_r_B\coadd1d_ngps2512130022-BD28d4211NGPS\AT2025zwi_spat0240.fits")
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r\p200_ngps_r_B\coadd1d_ngps2512130022-BD28d4211NGPS\AT2023uqm_spat0239.fits")
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r_SNR100\p200_ngps_r_B\coadd1d_ngps2512130022-BD28d4211NGPS\AT2025afyo_spat0240.fits")
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r\p200_ngps_r_B\coadd1d_ngps2512130023-BD28d4211NGPS\AT2025afvr_spat0240.fits")
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r\p200_ngps_r_B\coadd1d_ngps2512130023-BD28d4211NGPS\AT2025chm_spat0244.fits")

    # ind= hdu[1].data['wave']> 0 
    # plt.plot(hdu[1].data['wave'][ind], hdu[1].data['flux'][ind]) 

    data = Table.read(r"D:\ExtractSpec\NGPS_251213\quick_look\AT2025chm_NGPS_2025-12-13.txt", format='ascii') 
    plt.plot(data['col1'], data['col2'])
    plt.show() 

if False: 
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_u\p200_ngps_u_A\Science\spec1d_ngps_251213_0020-BD28d4211_NGPS_u_20251213T022657.660.fits") 
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_u\p200_ngps_u_A\Science\spec1d_ngps_251213_0059-Feige34_NGPS_u_20251213T130026.923.fits")
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_u\p200_ngps_u_A\Science\spec1d_ngps_251213_0043-J0755+1923_NGPS_u_20251213T082907.421.fits")
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251214\reduce_r\p200_ngps_r_A\Science\spec1d_ngps_251214_0050-AT_2025agra_NGPS_r_20251214T102913.919.fits")
    plt.plot(hdu[1].data['opt_wave'], hdu[1].data['opt_counts'])
    plt.plot(hdu[1].data['box_wave'], hdu[1].data['box_counts'])
    print(hdu[1].header['extname'])
    plt.show() 

if False: 
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r_SNR100\p200_ngps_r_B\coadd1d_ngps2512130023-BD28d4211NGPS\AT2021mde_spat0240.fits") 
    ind= hdu[1].data['wave'] > 0 
    plt.plot(hdu[1].data['wave'][ind], hdu[1].data['flux'][ind]*1.1, label='23') 

    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_r_SNR100\p200_ngps_r_B\coadd1d_ngps2512130022-BD28d4211NGPS\AT2021mde_spat0240.fits") 
    ind= hdu[1].data['wave'] > 0 
    plt.plot(hdu[1].data['wave'][ind], hdu[1].data['flux'][ind], label='22') 

    plt.legend() 
    plt.show() 


if False: 
    from astropy.coordinates import SkyCoord 
    import astropy.units as u 
    c1= SkyCoord(ra=339.0573333333333, dec=39.67666666666666, unit='deg')
    c2= SkyCoord(ra=339.05724999999995, dec= 39.67666666666666, unit='deg')
    print(c1.separation(c2).to(u.arcsec).value) 




if False: 
    # hdu=fits.open(r"D:\ExtractSpec \NGPS_251213\reduce_old_without spectral flexure\reduce_i_SNR100\p200_ngps_i_B\Science\spec1d_ngps_251213_0023-BD28d4211_NGPS_i_20251213T023626.161.fits") 
    # # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_i_SNR100_new\p200_ngps_i_B\Science\spec1d_ngps_251213_0028-AT2023uqm_NGPS_i_20251213T041703.666.fits")
    # plt.plot(hdu[1].data['opt_wave'], hdu[1].data['opt_counts'])
    # print(hdu[1].header['flex'])

    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_i_SNR100\p200_ngps_i_B\Science\spec1d_ngps_251213_0023-BD28d4211_NGPS_i_20251213T023626.161.fits") 
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_i_SNR100\p200_ngps_i_B\Science\spec1d_ngps_251213_0028-AT2023uqm_NGPS_i_20251213T041703.666.fits")
    plt.plot(hdu[1].data['opt_wave'], hdu[1].data['opt_counts']) 

    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_i\p200_ngps_i_B\Science\spec1d_ngps_251213_0023-BD28d4211_NGPS_i_20251213T023626.161.fits") 
    plt.plot(hdu[1].data['opt_wave'], hdu[1].data['opt_counts']) 

    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_i\p200_ngps_i_B\Science\spec1d_ngps_251213_0028-AT2023uqm_NGPS_i_20251213T041703.666.fits") 
    # plt.plot(hdu[1].data['opt_wave'], hdu[1].data['opt_counts']) 
    plt.show() 
     

if False: 
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\results_r\J0755+1923_spat0241_slit1.5.fits") 
    hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\results_i\J0755+1923_spat0338_slit1.5.fits")
    ind= hdu[1].data['wave'] > 0 

    redshift= 0.10826947 
    plt.plot(hdu[1].data['wave'][ind]/(1+redshift) , hdu[1].data['flux'][ind]*(1+redshift)) 
    plt.show() 



if False: 
    ###print the flexure offset 
    from pathlib import Path  as PathClass 
    path_dir= PathClass(r"D:\ExtractSpec\NGPS_251213\reduce_r_SNR100_new\p200_ngps_r_B\Science")
    
    for path  in path_dir.glob('spec1d*.fits'): 
        hdu=fits.open(path) 
        print(path.name.split('_')[0], hdu[1].header['FLEX_SHIFT_Total'])


if False: 
    # hdu=fits.open(r"D:\ExtractSpec\NGPS_251213\reduce_i_SNR100\p200_ngps_i_B\Calibrations\WaveCalib_B_1_DET01.fits")
    # plt.plot(hdu[2].data['wave_soln'][0], hdu[2].data['spec'][0])

    hdu=fits.open(r"D:\YBcode\PypeIt\pypeit\data\arc_lines\reid_arxiv\wvarxiv_p200_ngps_20250131T1354.fits") 
    plt.plot(hdu[1].data['wave'], hdu[1].data['flux'])

    hdu=fits.open(r"C:\Users\user\Downloads\wvarxiv_p200_ngps_20250131T1354.fits")
    plt.plot(hdu[1].data['wave'], hdu[1].data['flux'])

    plt.show() 


if False: 
    hdu =fits.open(r"E:\P200\P200_241031\results\telluric_red0069-G19B2B\AT2020afhd_tellcorr.fits") 
    plt.plot(hdu[1].data['wave'], hdu[1].data['telluric']) 
    plt.show() 
    

if False: 
    hdu=fits.open(r"D:\ExtractSpec\ljg2m401-yf01-20251220-0217-e00-Hilt600.fits") 
    plt.plot(hdu[1].data['sens_wave'][0], hdu[1].data['sens_zeropoint'][0]) 
    plt.plot(hdu[1].data['sens_wave'][0], hdu[1].data['sens_zeropoint_fit'][0])
    plt.show()

