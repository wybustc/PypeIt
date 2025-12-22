from astropy.io import fits 
import subprocess 
from pathlib import Path as PathClass
import os 
from pypeit.inputfiles import InputFile, PypeItFile, FluxFile, Coadd1DFile
from pypeit import msgs 
import shutil 
import sys 
import time 
from configobj import ConfigObj as config
import matplotlib.pyplot as  plt 
import numpy as np 
from astropy.coordinates import SkyCoord 
import astropy.units as u 
from astropy.table import Table 

class pypeit_wrapper(): 
    '''
    This class wraps some functions to automatically run the Pypeit; Written by YB 
    '''

    def __init__(self, path_dir, path_work,  instrument, clean=False): 
        self.path_dir   = PathClass(path_dir)  ###The directory containning the raw data 
        self.path_work  = PathClass(path_work) ###The working directory for Pypeit 
        self.path_pre   = self.path_work / 'pre_pypeit'  ###The working directory before primary Pypeit  
        self.instrument = instrument 
        self.file_ret   = []                   ###The list of files to be reduced   
        self.env        = os.environ.copy()
        self.path_setups= None 
        self.path_sens  = {}
        if sys.platform == 'win32': 
            subprocess.run('powershell -Command conda activate pypeitYB')
        if clean: 
            ##NOTE clean all the relvant files for last run 
            for path in self.path_work.glob(f'*{self.instrument}*'): 
                if path.is_dir():
                   shutil.rmtree(path) 
            if  self.path_pre.exists():
                shutil.rmtree(self.path_pre) 
            if  (self.path_work / 'rawfiles').exists(): 
                shutil.rmtree(self.path_work / 'rawfiles') 
        os.chdir(self.path_work)

    @staticmethod
    def input_func(str_info): 
        a= input(str_info)
        if  a in ['', 'yes', 'y','Y', 'Yes']: 
            return True 
        elif a in ['no', 'No', 'N','n']: 
            return False 
        else: 
            self.input_func('Input invalid; Please input again') 

    @staticmethod
    def sensfunc_input(sens_params, uvis_params): 
        pinput=input('Press enter to continue or input the paramters you want to change like: nresln: 10, resolution:1600,... \n') 
        if pinput=='': return 'break' 
        else: 
            pdict={}; dict_up={} 
            for p in pinput.split(','):
                if p.split(':')[0].strip() in ['hydrogen_mask_wid','mask_helium_lines','mask_hydrogen_lines', 'polyorder']: 
                    dict_up[p.split(':')[0].strip()]=p.split(':')[1]  
                else: 
                    pdict[p.split(':')[0].strip()]=p.split(':')[1] 
                    
            uvis_params.update(pdict) 
            sens_params.update(dict_up)

            cf=config()
            cf.filename='sensfunc.par'
            cf['sensfunc']=sens_params 
            cf['sensfunc']['UVIS']={'polycorrect': False} | uvis_params ##NOTE In the default case, we set polycorrect as False 
            cf.write()
            return 'continue'
        
    def config_calib(self): 
        '''
        This function is used to link the different calibration (here only for the arcs) sets to the different science/standards
        '''
        for path in self.path_setups: 
            self.read_setup(path / f'{path.name}.pypeit') 
            
            ###Find arcs 
            ind_arc = np.where(  np.char.find( self.parfile.data['frametype'].astype(str), 'arc') >=0 )[0]

            if len(ind_arc) > 1: 
                msgs.info(f'More than one arc in {path.name}  setup file, try to make a configuration ') 
                
                ###process the bias and flats, this usually should be same   
                ind1= np.char.find(self.parfile.data['frametype'].astype(str), 'bias') ###NOTE char.find will return the index of the wanted str in the found elements, if not found, this will return -1 for that elements 
                ind2= np.char.find(self.parfile.data['frametype'].astype(str), 'pixelflat' ) 
                ind3= np.char.find(self.parfile.data['frametype'].astype(str), 'illumflat') 
                ind4= np.char.find(self.parfile.data['frametype'].astype(str), 'trace')  

                ind = np.where( (ind1 >=0) | (ind2>=0) | (ind3>=0) | (ind4>=0) )[0] 
                self.parfile.data['calib'][ind] = 'all' 

                ###allocate arcfiles to corresponding science/ standard file 
                ind_sci= np.char.find( self.parfile.data['frametype'].astype(str), 'science') 
                ind_std= np.char.find( self.parfile.data['frametype'].astype(str), 'standard') 
                ind_sci= np.where( ( ind_sci>=0) | (ind_std>=0) )[0] 
                for i, index in enumerate(ind_arc): 
                    self.parfile.data['calib'][index]= i+1 
                    arc_name = self.parfile.data['target'][index] 

                    ind_name = self.parfile.data['target'][ind_sci]==arc_name 
                    self.parfile.data['calib'][ind_sci[ind_name]] = i+1 

                ### write to file 
                self.parfile.write( path / f'{path.name}.pypeit' )

                ###sucess or fail?
                ind = self.parfile.data['calib'][ind_sci]==0 
                if len(ind_sci[ind]) >0: 
                    msgs.warn('Arc allocation failed') 
                else: 
                    msgs.info('Arc allocation success')
            


                a= input('Open the pypeit file to check/correct the calib columns; Press enter to continue')
                subprocess.run(f'notepad { path/ f"{path.name}.pypeit"}', shell=True, check=True)  
            


                

    def pypeit_setup(self, pre_pypeit=False): 
        '''
        This functions runs the pypeit_setup command in the terminal, to get the information for the files
        '''
        if pre_pypeit:
            ###'changeing to correpsonding direcotry 
            self.path_pre.mkdir(exist_ok=True) 
            os.chdir(self.path_pre) 
        else: 
            os.chdir(self.path_work) 

        command= f'pypeit_setup -s {self.instrument} -r {self.path_dir} -c all' 
        if sys.platform == 'win32':
            res=subprocess.run(command, check=True)  
        else:
            res=subprocess.run(command, shell=True, check=True)
        self.path_setups= PathClass.cwd().glob(f'*{self.instrument}*')

    @staticmethod
    def run_ds9(path_file,dataext=None): 
        if sys.platform == 'win32':
            #TODO this still can not prevent the procedure to go on when open the ds9 
            if dataext is None:
                process = subprocess.Popen(r'powershell -Command ds9 %s'%path_file, shell=True)
            else: 
                process = subprocess.Popen(r'powershell -Command ds9 %s[%d]'%(path_file,dataext), shell=True)
            # time.sleep(0.1) ###Waiting for DS9 to launch； In fact, this may be not necessary

            # check whether DS9 is closed 
            while True:
                check_process = subprocess.Popen('powershell "Get-Process ds9 -ErrorAction SilentlyContinue"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = check_process.communicate()
                
                if b"ds9" not in output:
                    break  # ds9 already closed 
                time.sleep(0.1) 
        else: 
            if dataext is None:
                subprocess.run(['ds9',  path_file], check=True) 
            else:
                subprocess.run(['ds9', '%s[%d]'%path_file], check=True) 

    def read_setup(self, path): 
        '''
        This function reads the pypeit file generated by pypeit_setup
        '''
        self.parfile = PypeItFile.from_file(path)

    def ljt_yfosc_prePypeit(self, preParams): 
        '''
        This function modifies the datasec and biasec in the header for ljt_yfosc instrument 
        '''
        # print(preParams) 
        # a= input() 
        dispname_changed= [] ###NOTE the datasec should be modified according to dispname 
        for index, path_setup in enumerate(self.path_setups): 
            path_pypeit = path_setup / f'{path_setup.name}.pypeit'
            self.read_setup(path_pypeit) 
            dispname = self.parfile.setup['dispname']

            datasec= preParams.get('datasec',None) 
            biasysec= preParams.get('biasysec',None) 
            if 'datasec' not in preParams:
                if dispname =='grism3': 
                    datasec = '[160:2000, 2080:4250]'
                    # biasysec = ',2080:4250]'
                else: 
                    raise Exception(f'Dispersion name not recognized! {dispname}')
            if 'biasysec' not in preParams: 
                if dispname =='grism3': 
                    # datasec = '[160:2000, 2080:4250]'
                    biasysec = ',2080:4250]'
                else: 
                    raise Exception(f'Dispersion name not recognized! {dispname}')
            
            if dispname  in dispname_changed: continue ###NOTE the dataec should be modified according to dispname 
    
            
            data= self.parfile.data
            for d in data: 
                path_file= self.path_dir / d['filename']
                if (index>0) & (d['frametype']=='bias'): 
                    ###copy bias files for different dispname
                    path_new= path_file.parent/ path_file.name.replace('.fits.fz',f'_{dispname}.fits.fz')
                    shutil.copy(path_file,  path_new ) 
                    path_file=path_new 

                with fits.open(path_file, mode='update') as hdul: 
                    hdul[1].header['DATASEC']= datasec 
                    hdul[1].header['BIASSEC']= hdul[1].header['BIASSEC'].split(',')[0]+biasysec
                    hdul.flush()

            dispname_changed.append(dispname) 

        ###run the pypeit_setup again 
        for path in self.path_setups: 
            shutil.rmtree(path) 
        self.pypeit_setup(pre_pypeit=False) 
            

    def pre_pypeit(self, check_quality=False,copyfile=True, configCalib=True, dataext=None,  **preParams): 
        '''
        This function runs the data preparation scrpt 
        TO   throw unuseful files or configurations  
        TO   modify the datasec and biasec in the header 
        TO   check whether the image is good or not, if demanded

        Args:
            check_quality (bool): Whether to check the quality of the images.
        '''
        path_pre= self.path_work / 'pre_pypeit' 

        ###run the pypeit_setup first; retain files related to standard and science frames 
        self.pypeit_setup(pre_pypeit=True) 
        for path in self.path_setups: 
            self.read_setup(path / f'{path.name}.pypeit')  
            data= self.parfile.data 

            if ('science' in data['frametype'] ) | ('standard' in data['frametype'] ): 
                self.file_ret= self.file_ret + list(data['filename']) 
        
        ###copy the useful files to a new directory (NOTE we use link instead of copy to save space)
        path_new= self.path_work / 'raw_files'
        if path_new.exists():
            shutil.rmtree(path_new) 
        path_new.mkdir()  
        for file in self.file_ret: 
            if not (path_new / file).exists(): 
                if copyfile:
                    shutil.copy(self.path_dir / file, path_new / file) 
                else:
                    os.link(self.path_dir / file, path_new / file) 
        self.path_dir = path_new 

        ###run the pypeit_setup again  
        self.pypeit_setup(pre_pypeit=False) 

        ###check quality if demanded 
        if check_quality: 
            for path_setup in self.path_setups:
                path_pypeit = path_setup / f'{path_setup.name}.pypeit'
                self.read_setup(path_pypeit)
                if self.input_func('Open the pypeit file?(default: yes)'): 
                    subprocess.run(f'notepad { path_setup / f"{path_setup.name}.pypeit"}', shell=True)  
                if self.input_func('Check the images quality one by one?(default: yes)'):
                    data= self.parfile.data
                    for d in data: 
                        path_file= self.path_dir / d['filename']
                        print(f'Opening file: {path_file}') 
                        self.run_ds9(path_file, dataext=dataext) 
                        img_chk= self.input_func('If the %s is good? (default; yes)'%d['frametype']) 
                        if not img_chk: 
                            os.remove(path_file) 
            ###After checking, run pypeit_setup again to update the pypeit file
            self.pypeit_setup(pre_pypeit=False)


        ###modify accordingly for diffrent instruments
        if self.instrument=='ljt_yfosc': 
            self.ljt_yfosc_prePypeit(preParams) 

        if configCalib:
            self.config_calib()


    def run_pypeit(self, path_setup= None,  configs={}): 
        '''
        This is used to run pypeit, 
        args: 
            path_pypeit, the path to the pypeit file, if None , we will use that from self.path_setups 
            configs, the configuration that will be written to the pypeit file 
        '''
        if path_setup  is not None: 
            if isinstance(path_setup): 
                self.path_setups= [path_setup] 
        if (path_setup is None) and (self.path_setups is None): 
            msgs.info('attempt to find setups from the work dir') 
            self.path_setups= self.path_work.glob(f'*{self.instrument}*')

        
        for path_setup in self.path_setups: 
            os.chdir(path_setup) 
            path_pypeit = path_setup / f'{path_setup.name}.pypeit'
            if configs != {}: 
                self.read_setup(path_pypeit) 
                self.parfile.config.update(configs) 
                self.parfile.write(path_pypeit) 
            
            subprocess.run(['run_pypeit', str(path_pypeit),  '-o'], check=True)

    @staticmethod
    def get_median_index(lst):
        if not lst:
            return None  # return None for empty list 
        n = len(lst)
        # 创建(索引, 值)的元组列表
        indexed = [(index, value) for index, value in enumerate(lst)]
        # 按值排序元组列表
        sorted_indexed = sorted(indexed, key=lambda x: x[1])
        # 计算中位数位置（取上中位数位置）
        median_pos = n // 2
        # 返回原始索引
        return sorted_indexed[median_pos][0]


    def compare_std(self, path_sens, savefig= True): 
        ''' 
        This is used to compare the different sensfunc from different stds 
        '''
        path_sens = PathClass(path_sens) 
        ylim = [1e55, -1]; sensfunc_amplitude =[] ; std_sign= [] 
        for path in  path_sens.glob('*.fits'):  
            ###plot each sensfunc 
            hdu=fits.open(path) 
            wave, sensfunc = hdu[1].data['sens_wave'][0], hdu[1].data['sens_zeropoint_fit'][0] 
            plt.plot(wave, sensfunc, label = path.name.replace('.fits',''))
            hdu.close() 

            ## acquire the ylim, we only consider the primary region 
            wave_cover = wave[-1] - wave[0] 
            ind    =  (wave >  (wave[0]+ wave_cover /3))  & (wave< (wave[0]+wave_cover*2/3)) 
            ylim[0]=  min(np.min(sensfunc[ind]), ylim[0]) 
            ylim[1]=  max(np.max(sensfunc[ind]), ylim[1]) 
            sensfunc_amplitude.append(sum(sensfunc[ind]) / len(sensfunc[ind])) 
            std_sign.append(path.name.replace('.fits','')) 
        
        plt.ylim( ylim[0] - (ylim[1]-ylim[0])/2. , ylim[1]+ (ylim[1]-ylim[0])/2.)
        plt.legend() 
        if savefig: 
            plt.savefig(path_sens / 'std_comparison.png')
        plt.show() 

        ind= self.get_median_index(sensfunc_amplitude) 

        return std_sign[ind]




    def produce_sensfunc(self, debug=True, sens_params={}, uvis_params={}, tell_params={},clean=True): 
        '''
        This is used to do the flux calibration for 1d-spectra 
        Input: 
            sens_params; commmon params for pypeit_sensfunc (for diffent setups), like {'ljt_yfosc_A': {}} 
            uvis_params: params for UVIS algrithom of pypeit_sensfunc, like {'ljt_yfosc_A':{'resolution': 1000}}
        Output: 
            path_sens: dict, like {'ljt_yfosc_A': path_to_sens}, contains the path to sensfile for different configuration 
            
        '''
        if self.path_setups is None: 
            print('No setups directory assigned; Finding in the workdir') 
            self.path_setups= self.path_work.glob(f'*{self.instrument}*')

        for path_setup in self.path_setups: 
            setup = path_setup.name 
            path_pypeit= path_setup / f'{setup}.pypeit'

            par= PypeItFile.from_file(path_pypeit) 

            ind = par.data['frametype']=='standard'
            if len(par.data[ind])==0: 
                msgs.warn('No standrd object in the pypeit file') 
                continue 
        
            path_sens= path_setup / 'sensfunc'
            if path_sens.exists() & clean: 
                shutil.rmtree(path_sens) 

            path_sens.mkdir(exist_ok=True) 
            os.chdir(path_sens) 


            msgs.info('Find %s standards: %s'%(len(par.data[ind]), list( par.data['target'][ind] ) ) )
            filenames= list(par.data['filename'][ind])
            for filename in filenames: 
                path_1d = list( (path_setup / 'Science').glob('spec1d*%s*fits'%filename.split('.')[0] ))[0] 
                std_sign= "".join(path_1d.name.split('_')[1:-2])

                ###first produce the par file for sensfunc 
                cf=config()
                cf.filename='sensfunc.par'
                cf['sensfunc'] = sens_params.get(setup, {}) 
                cf['sensfunc']['UVIS']={'polycorrect': False} ##NOTE if True it will use the polyfit results to correct the Bspline fit at the mask region (It seems not all mask regions but only for narrow mask region?).
                                                              ##Hence if it's true, it can lead results that the masked region (e.g. emission line mask) has results jump at above or below the predicted results 
                                                              ##NOTE but the polyfit results can be improved by increase the polyorder parameter, hence maybe  in some case, this can be set to True to in combination with bspline 
                                                              ##fit when bspline fit can not fit all region well.
                if setup in uvis_params:
                    cf['sensfunc']['UVIS'].update(uvis_params[setup])   
                cf.write() 

                while True:
                    if debug:
                        ret=subprocess.run(f'pypeit_sensfunc {path_1d} -o {std_sign}.fits -s {cf.filename} --debug', shell=True)  
                    else:
                        ret=subprocess.run(f'pypeit_sensfunc {path_1d} -o {std_sign}.fits -s {cf.filename}', shell=True) 
                    res= self.sensfunc_input(sens_params, uvis_params) 
                    if res=='break': break 
                
                if not ret.returncode==0:
                    msgs.warn('warning : pypeit_senfunc ERROR for {std_sign}')
                    continue

            #### Put the path information for sensfunc into the self 
            self.path_sens[setup]= {'all':  path_sens, 'prefer': self.compare_std(path_sens)}  


    def flux_calib(self, path_sens={}): 
        '''
        This function is used to do the flux calibration 
        Input: 
             path_sens, the path to the directory of sensfunc file, like {'setup': path\to\direcotry,'prefer': filename of the preferred sensfunc if more than one }
        '''
        if self.path_setups is None:
            msgs.info('No setups provied; Finding them in the work dir....') 
            self.path_setups= self.path_work.glob(f'*{self.instrument}*')
        
        for path_setup in self.path_setups: 
            os.chdir(path_setup) 

            setup = path_setup.name 
            if setup not in self.path_sens: 
                msgs.info('Finding the sensfunc dir in the setup direcotry') 
                if (path_setup / 'sensfunc').exists(): 
                    path_sensDir = path_setup / 'sensfunc' 
                    std_prefer   = self.compare_std(path_sensDir) ##prefer the std with  median scale   
                elif setup in path_sens: 
                    path_sensDir = PathClass( path_sens[setup]['all'] )
                    if 'prefer' not in path_sens[setup]: 
                        std_prefer= self.compare_std(path_sensDir) 
                else: 
                    raise Exception('Please run the produce sensfunc first, or directly provied the path to the direcotry containing the std files') 
            else: 
                path_sensDir=self.path_sens[setup] ['all'] 
                if 'prefer' not in self.path_sens[setup]['prefer']: 
                    std_prefer= self.compare_std(path_sensDir) 
            
            self.path_sens={'all': path_sensDir, 'prefer': std_prefer}

            
            for path_sensfunc in  path_sensDir.glob('*.fits'): #NOTE The direcotry should only contain the std 
                std_sign = path_sensfunc.name.replace('.fits', '') 
                msgs.info(f'Start the flux calibration with the std: std_sign') 

                path_science= path_setup / 'Science' 
                path_science_std= path_setup / f'Science_{std_sign}' 
                if path_science_std.exists():
                    msgs.info(f'Detected old directory: Science_{std_sign}; Deleteing it') 
                    shutil.rmtree(path_science_std) 

                msgs.info('Copying the science file to the new directory.....') #For save space, we only copy spec1d file....
                shutil.copytree(path_science, path_science_std,ignore=lambda dir, names: [name for name in names if name.startswith('spec2d')])

                msgs.info('Initializing the flux setup') 
                subprocess.run('pypeit_flux_setup %s'%path_science_std, shell=True) 
                msgs.info('Correct the extinct from False to True') 
                path_par = path_setup / f'{self.instrument}.flux' 
                par= FluxFile.from_file(path_par)
                par.config['fluxcalib']['extinct_correct']=True 
                par.data['sensfile'][0] = str(path_sensfunc) 
                path_par = path_par.parent / path_par.name.replace('.flux', f'_{std_sign}.flux')
                par.write(path_par) 

                msgs.info('Do the flux calibration') 
                subprocess.run('pypeit_flux_calib %s'%path_par, shell=True)


            ####save name of preferred std into a file 
            with open(path_setup / 'std_prefer.txt', 'w') as fp: 
                fp.write('%s'%std_prefer) 

    
    def match_target(self, path_setup, target_method='coord', sep=None): 
        '''
        match exposures for the same targets
        '''
        self.target_exp= {} ###This formats liek {'target_name': [filename1, filename2, filenam3]}
        path_science= path_setup / 'Science' 

        if target_method=='name': 
            for path_spec in path_science.glob('spec1d*.fits'): 
                name = hdu[0].header['target'] 
                self.target_exp[name]= self.target_exp.get(name, []).append(path_spec.name) #NOTE we record the file name not the file path 
        elif target_method=='coord':
            if sep is None: 
                if self.instrument in ['ljt_yfosc']: 
                    sep = 0.2 
                elif self.instrument in ['p200_ngps_r','p200_ngps_i']: #NOTE the pipeline for p200_ngps used telescope coord not requested one , hence it may have large offset 
                    sep = 2 
                    
            for path_spec in path_science.glob('spec1d*.fits'): 
                # print(path_spec) 
                hdu =fits.open(path_spec) 
                c1  =SkyCoord(ra=hdu[0].header['RA'], dec=hdu[0].header['dec'], unit='deg') 
                # hdu.close() 

                foundsame=False
                for key in self.target_exp: 
                    hdu2 = fits.open( path_setup / 'Science' / self.target_exp[key][0]) ##we only use one file to see if the coords are within wanted separation 
                    c2  = SkyCoord(ra= hdu2[0].header['RA'], dec=hdu2[0].header['dec'], unit='deg') 
                    hdu2.close()
                    if c1.separation(c2).to(u.arcsec).value< sep: 
                        self.target_exp[key].append(path_spec.name) 
                        foundsame =True
                        break 
                if foundsame==False: 
                    namekey = hdu[0].header['target']
                    if namekey in self.target_exp: ##In some case, hdu[0].header['target'] may be same as old one, even when foundsame=False. This could be due to smae object with offset> sep or different object but one of them has wrong name 
                        for i in  range(10):
                            if (namekey+f'_{i}') in self.target_exp: continue 
                            else: 
                                self.target_exp[namekey+f'_{i}'] = [path_spec.name] 
                                break 
                    else:
                        self.target_exp[namekey] = [path_spec.name] 

    @staticmethod
    def get_allspat(path_spec):
        '''
        This function is used to get all the spec extracted at different spatial positions
        Input: 
             path_spec, the path to the spec1d file 
        Output: 
             the spat name, and the corresponding spatial position 
        ''' 
        hdu=fits.open(path_spec) 
        spat_name= []
        spat_posi= [] 
        for i in range(10): #In default, we think there is only can up to 10 spectrum 
            extname = f'EXT000{i}'
            if extname in hdu[0].header: 
                spat_name.append(hdu[0].header[extname]) 
                spat_posi.append(int( hdu[0].header[extname].split('-')[0].replace('SPAT','')) )
            else: 
                break 
        return np.array(spat_name), np.array( spat_posi) 
    

    def get_closestSpat(self, spat, path_spec): 
        '''
        This function is used to get the closest spatial position to the provied spat of extracted spectra
        '''
        spat_name, spat_posi= self.get_allspat(path_spec) 
        ind = np.argmin( np.abs( spat_posi- spat) )

        return spat_name[ind], spat_posi[ind], abs( spat_posi[ind]- spat) 


    def determin_spat(self, path_setup, method='all', max_spat_gap=2, user_provided={} ): 
        '''
        NOTE this function is used to get the spat pixel position for the target 
        Input args:
              method, the method used to calculated the position of the target 
                 if method=='all', we will retain all the spectrum found 
                 if method=='S/N', we will use    the spectrum with the best S/N 
                 if method=='WCS', we will use the coordinates to find the position
              max_spat_gap, the maximum gap, to thought spatial extractions as same spectrum 
              use_provided, this will provided the expecetd spatial position for a target  
        '''   
        self.useful_spat={} 

        msgs.info('Find all useful spectrum.....') ###We only consider the spectrum that were extracted in all the exposures of 1 target as useful 
        for target in self.target_exp: 
            spat_name, spat_posi= self.get_allspat( path_setup / 'Science' / self.target_exp[target][0]) 
            for i in range(1, len(self.target_exp[target])): 
                spat_name_i, spat_posi_i = self.get_allspat( path_setup / 'Science' / self.target_exp[target][i]) 
                
                seps= np.array( [ np.min(  np.abs( spat - spat_posi_i) ) for spat in  spat_posi] ) 
                ind = seps <=  max_spat_gap 
                spat_name = spat_name[ind] 
                spat_posi = spat_posi[ind]

            self.useful_spat[target] = spat_posi 
        
        if method=='all': 
            pass 
        elif method=='S/N':
            for target in self.target_exp: 
                path_spec1d=path_setup / 'Science' / self.target_exp[target][0] ###NOTE we use one expousre to get the position with best SNR 
                spat_name, spat_posi= self.get_allspat( path_spec1d ) 
                hdu= fits.open(path_spec1d) 

                snr_max = -9999
                spat_used= None 
                for spat in spat_name: 
                    snr = np.nanmedian( hdu[ int(spat[-1]) ].data['opt_counts'] * hdu[ int(spat[-1]) ].data['opt_counts_ivar']**0.5 ) 
                    if snr > snr_max: 
                        snr_max= snr 
                        spat_used = spat 

                self.useful_spat[target]= np.array( [ spat_used  ]) 
    
        elif method=='wcs': 
            ###It seems there is some error in the wcs for ljt 
            msgs.warn('The WCS method is still not completed, and we here use the all method')

        
        ###process the special case, where user_provied position is not None
        for target in user_provided: 
            if target not in self.target_exp: 
                msgs.warn(f'Provided {target} is not found')
            path_spec1d=path_setup / 'Science' / self.target_exp[target][0] ###NOTE we use one expousre to get the position with best SNR 
            spatName, spat, sep= self.get_closestSpat(user_provided[target], path_spec1d)
            if sep > 5: 
                raise Exception('The cloest spat to the provied is more than 5 pixel') 
            self.useful_spat[target]= np.array([spat] ) 


                    
    def codd1d_spec(self, target_method='coord', spat_method=None, max_spat_gap= 2, user_provided={}): 
        '''
        This function is used to coaddd multiple exposure, or convert only 1-exposure to the 1d-spec format, 
        Input: 
            target_method, the way used to find all exposures for a same target 
                           there are two method supported, i.e., 'name':treat sources with same name as same target 
                                                                'coord': treat sources with coords within separation of 0.5 arcsec 
                           the default is to use the coordinates to match the target      
            spat_method  , the way used to find the spatial pixel position for the wanted target                                   
        ''' 
        
        assert target_method in ['name', 'coord'], 'the target method only support coord or name'
        
        if self.path_setups is None: 
            msgs.info('No setup in the self variable, finding them in the work dir') 
            self.path_setups= self.path_work.glob(f'*{self.instrument}*') 
        
        for path_setup in  self.path_setups: 
            msgs.info('Finding all Science dir calibrated with different std') 
            path_sciences = path_setup.glob(f'Science_*')
            # print(list(path_sciences))

            msgs.info('Mkdir for coadded 1d spec')
            for path_science in path_sciences: 
                path_coadd = path_setup / path_science.name.replace('Science', 'coadd1d') 
                if path_coadd.exists(): 
                    shutil.rmtree(path_coadd) 
                os.mkdir(path_coadd) 

            msgs.info('Matching targets with exposures')
            self.match_target(path_setup, target_method= target_method) 
            print(self.target_exp) 

            msgs.info('Determing the spatial pixel position for each target') 
            self.determin_spat(path_setup, method= spat_method, max_spat_gap=max_spat_gap, user_provided= user_provided)  


            msgs.info('Beginning to the coadd the 1d spec') 
            path_sciences = path_setup.glob(f'Science_*')
            for path_science in path_sciences: 
                # print('hello')
                path_coadd = path_setup / path_science.name.replace('Science', 'coadd1d') 
                
                os.chdir(path_coadd) 
                subprocess.run(['pypeit_flux_setup', str(path_science)]) 

                par = Coadd1DFile.from_file(f'{self.instrument}.coadd1d')

                ###coadd1d for each target 
                for target in self.target_exp: 
                    ###coadd1d for each spat
                    # print(self.useful_spat[target])
                    # print(self.target_exp[target])
                    for spat in self.useful_spat[target]: 
                        print('hello %s'%spat)
                        filenames= [] ; spat_names= [] 
                        print(spat, self.target_exp[target]) 
                        for filename in self.target_exp[target]: 
                            filenames.append(filename) 
                            spat_name, spat_posi, sep = self.get_closestSpat(spat, path_science / filename) 
                            spat_names.append(spat_name) 

                        par.config['coadd1d']['coaddfile']= '%s_spat%04d.fits'%(target, spat) 
                        # par.data['filename']=filenames
                        # par.data['obj_id']  =spat_names 
                        par.data=Table({'filename': filenames, 'obj_id': spat_names})
                        path_coadd1dfile= path_coadd / ( '%s_spat%04d.coadd1d'%(target, spat) )
                        # print(path_coadd1dfile)
                        par.write(path_coadd1dfile ) 
                
                        subprocess.run(['pypeit_coadd_1dspec', str(path_coadd1dfile)],check=True)


    def telluric_correction(self, tellgrid=None, path_res=None):
        '''
        This function is used to do the telluric correction for each coadded 1dspec
        Input: 
             tellgrid, if you want use a specific tellgrid file, you can refer to this variable, the default is None, the it will use the default tellgrid file determined by the pypeit
             If path_res is not None, it will do the telluric correction for fits file in the path_res 
        '''
        if path_res is not None: 
            path_res  = PathClass( path_res) 
            path_tell = path_res  / 'telluric' 
            if path_tell.exists(): 
                shutil.rmtree(path_tell) 

            os.mkdir(path_tell) 
            for path_1d in path_res.glob('*.fits'): 
                shutil.copy(path_1d, path_tell / path_1d.name)
            
            os.chdir(path_tell) 
            for path_1d in path_tell.glob('*.fits'): 
                command= ['pypeit_tellfit', str(path_1d),  '--objmodel',  'poly'] 
                # command = 'pypeit_tellfit %s --objmodel poly'%path_1d
                if tellgrid is not None: 
                    command  = command + ['-g', str(tellgrid)]
                    # command = command +'  -g %s'%tellgrid
                subprocess.run(command, check=True)
            
            return ':)'
 

        if self.path_setups is None: 
            msgs.info('No setup in the self variable, finding them in the work dir') 
            self.path_setups= self.path_work.glob(f'*{self.instrument}*') 
        
        for path_setup in self.path_setups: 
            ###find the coadd1d directory  
            path_coadds= path_setup.glob('coadd1d_*')
            
            for path_coadd in  path_coadds: 
                path_tell = path_setup / path_coadd.name.replace('coadd1d', 'telluric')
                msgs.info('Copying the spec1d file to the telluric directory')
                if path_tell.exists(): 
                    shutil.rmtree(path_tell) 
                shutil.copytree(path_coadd, path_tell, ignore=lambda dir, names: [name for name in names if not name.endswith('.fits')]) 

                os.chdir(path_tell) 
                for path_1d in path_tell.glob('*.fits'): 
                    command= ['pypeit_tellfit', str(path_1d),  '--objmodel',  'poly'] 
                    # command = 'pypeit_tellfit %s --objmodel poly'%path_1d
                    if tellgrid is not None: 
                        command  = command + ['-g', str(tellgrid)]
                        # command = command +'  -g %s'%tellgrid
                    subprocess.run(command, check=True)

                    
                    


        

            

            



    

        
    
        
        

