from pypeit_wrapper import pypeit_wrapper 

if True: 
    path_files= r"D:\ExtractSpec\2M4\251026\251026"  ###path to dir with raw files 
    path_work = r"D:\ExtractSpec\2M4\251026"  ###path to working dir 

    ljt= pypeit_wrapper(path_dir = path_files, path_work=path_work , instrument='ljt_yfosc',clean=False) ###clean = True, it will clean working dir before running pypeit 
    ljt.pre_pypeit(check_quality=False, copyfile=True) ###Do some preparation work, copyfile=True, it will copy useful raw files to working dir, but this would take more space on disk. If False, it will create links to original files, but in this case, the original files will also be modified by the procedure 
    ljt.run_pypeit( ) #run the pypeit , You can set some configs allowed for pypeit, like configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    ljt.produce_sensfunc() ##produce the sensfunc file for flux calibaration 
    ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}}) ###path_sens, path to dir containing a sensfunc file, it will be used , if no std was found  in this observation set 
    ljt.codd1d_spec(target_method='coord') ###coadd1d extracted 1d spectra 
    ljt.telluric_correction() ###Do the telluric correction 

if False:
    ###still one error, about for cycle 
    ljt= pypeit_wrapper(path_dir = r"D:\ExtractSpec\2M4\251013\251013_test\251013", path_work=r"D:\ExtractSpec\2M4\251013\251013_test2", instrument='ljt_yfosc',clean=False)
    # ljt.pre_pypeit(check_quality=False) 
    # ljt.run_pypeit( ) #configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    # ljt.produce_sensfunc()
    # ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}})
    ljt.codd1d_spec(target_method='coord') 
    ljt.telluric_correction()

if False: 
    ljt= pypeit_wrapper(path_dir = r"D:\ExtractSpec\2M4\251129\251129", path_work=r"D:\ExtractSpec\2M4\251129", instrument='ljt_yfosc',clean=False)
    ljt.pre_pypeit(check_quality=False) 
    ljt.run_pypeit( ) #configs={'calibrations':{'wavelengths':{'method': 'holy-grail'}}}
    ljt.produce_sensfunc()
    ljt.flux_calib(path_sens= {'ljt_yfosc_A': {'all': r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\sensfunc"}})
    ljt.codd1d_spec(target_method='coord') 
    ljt.telluric_correction()


if False: 
    from astropy.io import fits 
    import matplotlib.pyplot as plt 
    from astropy.table import Table 

    hdu=fits.open(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Calibrations\WaveCalib_A_0_DET01.fits")

    plt.plot( hdu[2].data['spec'][0])


    data= Table.read(r"D:\ExtractSpec\2M4\ds92.dat",format='ascii') 
    plt.plot(data['col1'][::-1]+7, data['col2'])
    plt.show() 

if False: 
    import subprocess
    import os 
    print(os.getcwd() )
    subprocess.run(['ls','-l'])