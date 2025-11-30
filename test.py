from pypeit.inputfiles import InputFile, PypeItFile,FluxFile, Coadd1DFile
import subprocess 
import numpy as np 

if False: 
    # InputFile.data_block='data'
    cls= PypeItFile.from_file(r"D:\ExtractSpec\2M4\251026\ljt_yfosc_A\ljt_yfosc_A.pypeit")
    # print(cls.data) 
    # print(cls.setup) 
    # print(cls.config, cls.config.__class__) 
    # print(cls.file_paths)
    # cls.setup['Setup B']=' '

    # print(cls.data['frametype']=='standard') 
    print(np.where( np.char.find( cls.data['frametype'].astype(str), 'arc') >=0)[0]  ) 

    # cls.write(r"D:\ExtractSpec\2M4\251013\ljt_yfosc_B\ljt_yfosc_B_test.pypeit")

if False: 
    subprocess.run(['notepad', r"D:\ExtractSpec\2M4\251013\ljt_yfosc_B\ljt_yfosc_B.pypeit"], shell=True)

if False: 
    import os 
    dst = r"D:\ExtractSpec\2M4\251013\ljg2m401-yf01-20251013-0002-b00.fits.fz"
    src = r"D:\ExtractSpec\2M4\251013\251013\ljg2m401-yf01-20251013-0002-b00.fits.fz"
    # subprocess.run(f'mklink "{dst}" "{src}"', shell=True, check=True)
    os.link(src, dst) 
    # os.symlink(, , target_is_directory=False)

if False: 
    # process= subprocess.run(r'powershell -Command ds9 -wait D:\ExtractSpec\2M4\251013\hdu\bias_2.fits', shell=True, )
    # # process.wait() 
    # # process= subprocess.Popen(r'powershell -Command ds9 D:\ExtractSpec\2M4\251013\hdu\bias_3.fits', shell=True, )
    # print('hello')

    import time 
    def run_ds9(path_file): 
        process = subprocess.Popen(r'powershell -Command ds9 %s'%path_file, shell=True)

        # 等待 DS9 窗口出现（给一些启动时间）
        # time.sleep(2)

        # 轮询检查 DS9 是否还在运行
        while True:
            # 检查是否有 ds9 进程在运行
            check_process = subprocess.Popen('powershell "Get-Process ds9 -ErrorAction SilentlyContinue"', 
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = check_process.communicate()
            
            if b"ds9" not in output:
                break  # DS9 已关闭
            time.sleep(0.1)

    run_ds9(r'D:\ExtractSpec\2M4\251013\hdu\bias_2.fits')
    print('DS9 closed, continuing execution...')

if False: 
    for i,j in  enumerate(['a','b', 'c', 'd','e','f','g']): 
        print(i,j) 


if False: 
    from astropy.io import fits 
    path_file = r"D:\ExtractSpec\2M4\251013\rename\lslit2_51-open-grism3\bias_2.fits.fz"
    with fits.open(path_file, mode='update') as hdul: 
        print(hdul[1].header['datasec'], hdul[1].header['datasec'].split(',')[0]+',2080:4250]') 
        print(hdul[1].header['biassec'])



if False: 
    import subprocess
    import sys

    subprocess.run('pypeit_setup -h ', shell=False, check=True)

if False: 
    import os
    from pathlib import Path as PathClass 
    path = PathClass(r"D:\ExtractSpec\2M4\251013")
    os.chdir(path) 
    path= PathClass(r"D:\ExtractSpec\2M4\251013\251013_test\raw_files") 
    for path in path.glob('*'):
        print(path.parent) 

if False: 
    from astropy.io import fits 
    path_new= r"D:\ExtractSpec\2M4\251013\251013_test\raw_files\ljg2m401-yf01-20251013-0142-e00.fits.fz" 
    path_old= r"D:\ExtractSpec\2M4\251013\251013\ljg2m401-yf01-20251013-0142-e00.fits.fz" 

    hdu1= fits.open(path_new) 
    hdu2= fits.open(path_old) 

    keys = set( list(hdu1[1].header.keys()) + list(hdu2[1].header.keys()) ) 
    for key in  keys: 
        if key not in hdu1[1].header.keys(): 
            print(f'{key} not in file new') 
            continue 
        if key not in hdu2[1].header.keys(): 
            print(f'{key} not in file old') 
            continue 

        if hdu1[1].header[key] != hdu2[1].header[key]: 
            print(f'{key}, new {hdu1[1].header[key]}, old {hdu2[1].header[key]}') 
    
if False: 
    from pathlib import Path as PathClass
    path =PathClass(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Science") 
    print(list( path.glob('spec1d*ljg2m401-yf01-20251018-0186-e00-BD+28d4211_yf01_20251018T154144.373*fits')))

if False: 
    from astropy.io import fits 
    hdu=fits.open(r"D:\ExtractSpec\2M4\251018_STD\ljt_yfosc_A\Science\spec1d_ljg2m401-yf01-20251018-0186-e00-BD+28d4211_yf01_20251018T154144.373.fits")
    import matplotlib.pyplot as plt 
    i =4
    plt.plot(hdu[i].data['opt_wave'], hdu[i].data['opt_counts']) 
    plt.show() 

if False: 
    cls= FluxFile.from_file(r"D:\ExtractSpec\Magellan_EP1020a\reduce_magellan_mage_A\magellan_mage.flux") 
    print(cls.config) 
    print(cls.data) 
    cls.config['fluxcalib']['extinct_correct']=False 
    cls.data['sensfile'][0] = r"D:\ExtractSpec\Magellan_EP1020a\reduce_magellan_mage_A\feige110.fits" 
    cls.write(r"D:\ExtractSpec\Magellan_EP1020a\reduce_magellan_mage_A\feige110_test.flux")

if False: 
    ###test the WCS 
    from astropy.io import fits 
    hdul=fits.open(r"D:\ExtractSpec\2M4\251018_STD\251018_STD\ljg2m401-yf01-20251018-0179-e00.fits.fz")
    # hdul=fits.open(r"D:\ExtractSpec\2M4\251013\251013\ljg2m401-yf01-20251013-0142-e00.fits.fz")

    from astropy.wcs import WCS
    import numpy as np
    from astropy.coordinates import SkyCoord 

    header = hdul[1].header  # 通常WCS信息在第一个HDU的头文件中
    data = hdul[1].data      # 图像数据（可选，用于验证坐标范围）

    header['CD1_2'] = -header['CD1_2'] 
    header['CD2_1'] = -header['CD2_1'] 
    header.update() 

    # 2. 创建WCS对象
    wcs = WCS(header)

    # 3. 定义天球坐标（赤经/赤纬，单位为度）
    ra = header['tpt-ra']   # 替换为你的目标赤经（单位：度）
    dec= header['tpt-dec']   # 替换为你的目标赤纬（单位：度）
    ra =ra.split(':') 
    dec=dec.split(':') 
    ra = ra[0]+'h'+ra[1]+'m'+ra[2]+'s' 
    dec=dec[0]+'d'+dec[1]+'m'+dec[2]+'s' 
    c1=SkyCoord(ra+' '+dec) 
    ra_deg= c1.ra.value 
    dec_deg= c1.dec.value 
    print(ra_deg, dec_deg) 

    ra = header['tpt-ra']   # 替换为你的目标赤经（单位：度）
    dec= header['tpt-dec']   # 替换为你的目标赤纬（单位：度）
    ra =ra.split(':') 
    dec=dec.split(':') 
    ra = ra[0]+'h'+ra[1]+'m'+ra[2]+'s' 
    dec=dec[0]+'d'+dec[1]+'m'+dec[2]+'s' 
    c1=SkyCoord(ra+' '+dec) 
    ra_ref= c1.ra.value 
    dec_ref= c1.dec.value 
    print(ra_ref, dec_ref) 
    print(header['CRVAL1'], header['CRVAL2'])

    header['CRVAL1']=ra_ref ###为什么修改前后没有用？
    header['CRVAL2']=dec_ref
    header.update() 

    # 4. 转换为像素坐标
    # 使用wcs_world2pix方法，origin=0表示返回0-indexed坐标（Python数组索引）
    pixel_coords = wcs.wcs_world2pix([[ra_deg, dec_deg]], 1)[0]  # 返回格式: [x, y]
    x_pix, y_pix = pixel_coords

    print(f"物理像素坐标 (0-indexed): x = {x_pix:.2f}, y = {y_pix:.2f}")

    # 5. （可选）验证坐标是否在图像范围内
    if (0 <= x_pix < data.shape[1]) and (0 <= y_pix < data.shape[0]):
        print("坐标位于图像内部")
    else:
        print("警告：坐标超出图像边界！")

    # 6. （可选）获取整数像素位置（用于索引）
    x_int = int(round(x_pix))
    y_int = int(round(y_pix))
    print(f"整数像素索引: x_index = {x_int}, y_index = {y_int}")

    hdul.close()  # 关闭文件

if False: 
    ###f
    from astropy.io import fits 
    from astropy.table import Table 
    par= Coadd1DFile.from_file(r"D:\ExtractSpec\2M4\251013\251013_test\ljt_yfosc_A\ljt_yfosc.coadd1d")

    print(par.data.__class__) 
    par.data = Table({'filename': ['1','2'], 'obj_id': ['1','2']})
    # par.data['filename']=['1', '2'] 
    # par.data['obj_id']  =['1', '2']
    print(par.data.__class__) 
    print(par.data)

if  True: 
    data = ['a', 'b', 'c', 'd', 'e', 'f'] 
    for i , j in enumerate(data): 
        print(i, j) 
        