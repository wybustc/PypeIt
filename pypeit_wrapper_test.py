from pypeit_wrapper import pypeit_wrapper 


if True:
    ljt= pypeit_wrapper(path_dir = r"D:\ExtractSpec\2M4\251013\251013_test\251013", path_work=r"D:\ExtractSpec\2M4\251013\251013_test", instrument='ljt_yfosc',clean=False)
    # ljt.pre_pypeit(check_quality=False) 
    # ljt.run_pypeit( ) #configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    # ljt.produce_sensfunc()
    # ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}})
    ljt.codd1d_spec() 


if False: 
    from astropy.io import fits 
    import matplotlib.pyplot as plt 
    from astropy.table import Table 

    hdu=fits.open(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Calibrations\WaveCalib_A_0_DET01.fits")

    plt.plot( hdu[2].data['spec'][0])


    data= Table.read(r"D:\ExtractSpec\2M4\ds92.dat",format='ascii') 
    plt.plot(data['col1'][::-1]+7, data['col2'])
    plt.show() 

