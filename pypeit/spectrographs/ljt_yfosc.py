"""
Module for NTT EFOSC2

.. include:: ../include/links.rst
"""
import numpy as np

from pypeit import msgs
from pypeit import telescopes
from pypeit.core import parse
from pypeit.core import framematch
from pypeit.spectrographs import spectrograph
from pypeit.images import detector_container

from IPython import embed

class LJTYFOSCSpectrograph(spectrograph.Spectrograph):
    """
    Child of Spectrograph to handle LJT/YFOSC specific code
    """
    ndet = 1  # Because each detector is written to a separate FITS file
    telescope = telescopes.LJTTelescopePar()
    name = 'ljt_yfosc'
    header_name = 'yf01'
    camera = 'yf01'
    url = 'https://www.raa-journal.org/issues/all/2019/v19n10/202203/P020220324625354383216.pdf'
    supported = True
    comment = 'The YFOSC instrument mounted on the Lijiang 2.4m telescope at Yunnan Observatories, China.'
    allowed_extensions = [".fz"]

    def init_meta(self):
        """
        Define how metadata are derived from the spectrograph files.

        That is, this associates the PypeIt-specific metadata keywords
        with the instrument-specific header cards using :attr:`meta`.
        """
        self.meta = {}
        # Required (core)
        self.meta['ra']        = dict(ext=1, card='CAT-RA' , required_ftypes=['science', 'standard'])
        self.meta['dec']       = dict(ext=1, card='CAT-DEC', required_ftypes=['science', 'standard'])
        self.meta['target']    = dict(ext=1, card='OBJECT')
        self.meta['binning']   = dict(card=None, compound=True ) #TODO check whether the first is binspectral and second is binspatial 
        self.meta['mjd']       = dict(ext=1, card='MJD-OBS')
        
        self.meta['datasec']   = dict(ext=1, card='DATASEC')
        self.meta['oscansec']  = dict(ext=1, card='BIASSEC')
        self.meta['exptime']   = dict(ext=1, card='EXPTIME')
        self.meta['airmass']   = dict(ext=1, card='AIRMASS', required_ftypes=['science', 'standard']) #TODO here is effective airmass, do we need to use airmass at start or at end? 
        self.meta['decker']    = dict(ext=1, card='FILTER1', required_ftypes=['science', 'standard'])
        
        # Extras for config and frametyping
        self.meta['dispname']  = dict(ext=1, card='FILTER3', required_ftypes=['science', 'standard'])
        self.meta['idname']    = dict(ext=1, card='OBSTYPE')
        self.meta['instrument']= dict(ext=1, card='INSTRUME')
        self.meta['filter2']   = dict(ext=1, card='FILTER2') #TODO is this name in meta legal ? 

        self.meta['lampstat01']= dict(ext=1, card='FILTER7') # open or closed

    
    def compound_meta(self, headarr, meta_key):
        """
        Methods to generate metadata requiring interpretation of the header
        data, instead of simply reading the value of a header card.

        Args:
            headarr (:obj:`list`):
                List of `astropy.io.fits.Header`_ objects.
            meta_key (:obj:`str`):
                Metadata keyword to construct.

        Returns:
            object: Metadata value read from the header(s).
        """
        if meta_key == 'binning': 
            binspatial = headarr[1]['CCDSUM'].split()[0] 
            binspec = headarr[1]['CCDSUM'].split()[1] 
            binning = parse.binning2string(int(binspec), int(binspatial))
            return binning 

    def config_independent_frames(self):
        """
        Define frame types that are independent of the fully defined
        instrument configuration.

        This method returns a dictionary where the keys of the dictionary are
        the list of configuration-independent frame types. The value of each
        dictionary element can be set to one or more metadata keys that can
        be used to assign each frame type to a given configuration group. See
        :func:`~pypeit.metadata.PypeItMetaData.set_configurations` and how it
        interprets the dictionary values, which can be None.

        Returns:
            :obj:`dict`: Dictionary where the keys are the frame types that
            are configuration-independent and the values are the metadata
            keywords that can be used to assign the frames to a configuration
            group.
        """
        return {'bias': ['binning', 'datasec'], 'dark': ['binning', 'datasec']} #TODO check this 

    def configuration_keys(self):
        """
        Return the metadata keys that define a unique instrument
        configuration.

        This list is used by :class:`~pypeit.metadata.PypeItMetaData` to
        identify the unique configurations among the list of frames read
        for a given reduction.

        Returns:
            :obj:`list`: List of keywords of data pulled from file headers
            and used to constuct the :class:`~pypeit.metadata.PypeItMetaData`
            object.
        """
        return ['dispname', 'decker', 'filter2',  'binning', 'datasec']

    def raw_header_cards(self):
        """
        Return additional raw header cards to be propagated in
        downstream output files for configuration identification.

        The list of raw data FITS keywords should be those used to populate
        the :meth:`~pypeit.spectrographs.spectrograph.Spectrograph.configuration_keys`
        or are used in :meth:`~pypeit.spectrographs.spectrograph.Spectrograph.config_specific_par`
        for a particular spectrograph, if different from the name of the
        PypeIt metadata keyword.

        This list is used by :meth:`~pypeit.spectrographs.spectrograph.Spectrograph.subheader_for_spec`
        to include additional FITS keywords in downstream output files.

        Returns:
            :obj:`list`: List of keywords from the raw data files that should
            be propagated in output files.
        """
        return ['FILTER1', 'FILTER3']

    def get_detector_par(self, det, hdu=None):
        """
        Return metadata for the selected detector.

        .. warning::

            Many of the necessary detector parameters are read from the file
            header, meaning the ``hdu`` argument is effectively **required** for
            LJT/YFOSC.  The optional use of ``hdu`` is only viable for
            automatically generated documentation.

        Args:
            det (:obj:`int`):
                1-indexed detector number.
            hdu (`astropy.io.fits.HDUList`_, optional):
                The open fits file with the raw image of interest.  If not
                provided, frame-dependent parameters are set to a default.

        Returns:
            :class:`~pypeit.images.detector_container.DetectorContainer`:
            Object with the detector metadata.
        """
        if hdu is None:
            binning  = '1,1'
            datasec  = None
            oscansec = None
            gain     = np.atleast_1d(1.2)
            rdnoise  = np.atleast_1d(2.2)
            saturate = 63000
            nonlinear= 0.52 
            darkcurr = 36
            platesca =0.286 
        else:
            binning  = self.get_meta_value(self.get_headarr(hdu), 'binning')
            datasec  = np.atleast_1d( parse.flip_fits_slice( hdu[1].header['datasec']) ) #NOTE flip is must 
            oscansec = np.atleast_1d( parse.flip_fits_slice( hdu[1].header['biassec'] ) )
            gain     = np.atleast_1d(hdu[1].header['GAIN'])  # e-/ADU
            rdnoise  = np.atleast_1d(hdu[1].header['RDNOISE'])  # e-/pixel
            saturate = hdu[1].header['SATURATE']*100  # ADU
            nonlinear= round(hdu[1].header['MAXLIN']/saturate*100,2) #TODO It seems that the satpix par in the process is not useful, and here we just set a large stauration value to aviod mask in the luminous arc lines 
            darkcurr = hdu[1].header['DARKCURR']*3600  # e-/pixel/hour
            platesca = hdu[1].header['PIXSCALE']  # arcsec/pixel
        
        # Instrument paper: https://www.raa-journal.org/issues/all/2019/v19n10/202203/P020220324625354383216.pdf
        detector_dict = dict(
            binning         = binning,
            det             = 1, # only one detector
            dataext         = 1,
            specaxis        = 0,
            specflip        = False, #TODO check 
            spatflip        = False, #TODO check 
            platescale      = platesca, #TODO, the meaning ? here use the PIXSCALE
            darkcurr        = darkcurr,  # e-/pixel/hour
            saturation      = saturate, 
            nonlinear       = nonlinear,
            mincounts       = -1e10, #TODO check; I didn't find relevant info 
            numamplifiers   = 1,     #TODO check; I didn't find relevant info. In the header, there is only amplifier name ('default'), and only 1 gain 
            gain            = gain,  
            ronoise         = rdnoise, 
            datasec         = datasec,
            oscansec        = oscansec,
            #suffix          = '_Thor',
        )
        return detector_container.DetectorContainer(**detector_dict)

    @classmethod
    def default_pypeit_par(cls):
        """
        Return the default parameters to use for this instrument.
        
        Returns:
            :class:`~pypeit.par.pypeitpar.PypeItPar`: Parameters required by
            all of PypeIt methods.
        """
        par = super().default_pypeit_par()

        
        # Ignore PCA
        par['calibrations']['slitedges']['sync_predict'] = 'nearest'
        par['calibrations']['slitedges']['bound_detector']= True 

        # Ignore satureated pixels for arcframe; NOTE the stapix parameters below seems not useful? (I haven't checked the code yet)
        par['calibrations']['arcframe']['process']['satpix']='force'
        par['calibrations']['pixelflatframe']['process']['satpix']='nothing'
        par['calibrations']['illumflatframe']['process']['satpix']='nothing'
        par['calibrations']['alignframe']['process']['satpix'] ='nothing'
        par['calibrations']['lampoffflatsframe']['process']['satpix']='nothing'
        par['calibrations']['tiltframe']['process']['satpix'] ='nothing'

        # par['calibrations']['arcframe']['process']['subtract_continuum']=True

        # 1D wavelength solution
        par['calibrations']['wavelengths']['method'] = 'full_template'
        par['calibrations']['wavelengths']['lamps'] = ['HeI','NeI']

        # Set the default exposure time ranges for the frame typing
        par['calibrations']['biasframe']['exprng']     = [None, 0.001]
        par['calibrations']['darkframe']['exprng']     = [999999, None]     # No dark frames
        par['calibrations']['pinholeframe']['exprng']  = [999999, None]     # No pinhole frames
        par['calibrations']['arcframe']['exprng']      = [None, 120]
        par['calibrations']['standardframe']['exprng'] = [None, 300]
        par['scienceframe']['exprng']                  = [60, None]

        return par

    def config_specific_par(self, scifile, inp_par=None):
        """
        Modify the PypeIt parameters to hard-wired values used for
        specific instrument configurations.

        Args:
            scifile (:obj:`str`):
                File to use when determining the configuration and how
                to adjust the input parameters.
            inp_par (:class:`~pypeit.par.parset.ParSet`, optional):
                Parameter set used for the full run of PypeIt.  If None,
                use :func:`default_pypeit_par`.

        Returns:
            :class:`~pypeit.par.parset.ParSet`: The PypeIt parameter set
            adjusted for configuration specific parameter values.
        """
        # Start with instrument wide
        par = super().config_specific_par(scifile, inp_par=inp_par)

        # Wavelength calibrations
        if   self.get_meta_value(scifile, 'dispname') == 'grism3':
            par['calibrations']['wavelengths']['reid_arxiv'] = 'ljt_yfosc_Gr3.fits'
            par['sensfunc']['UVIS']['resolution']     =  2000 #TODO check 
        elif self.get_meta_value(scifile, 'dispname') == 'grism14':
            par['calibrations']['wavelengths']['reid_arxiv'] = 'ljt_yfosc_Gr14.fits' 
            par['sensfunc']['UVIS']['resolution']     =  3500 #TODO check 
        elif self.get_meta_value(scifile, 'dispname') == 'grism8':
            par['calibrations']['wavelengths']['reid_arxiv'] = 'ljt_yfosc_Gr8.fits'
            par['sensfunc']['UVIS']['resolution']     =  4000 #TODO check 
        return par

    def check_frame_type(self, ftype, fitstbl, exprng=None):
        """
        Check for frames of the provided type.

        Args:
            ftype (:obj:`str`):
                Type of frame to check. Must be a valid frame type; see
                frame-type :ref:`frame_type_defs`.
            fitstbl (`astropy.table.Table`_):
                The table with the metadata for one or more frames to check.
            exprng (:obj:`list`, optional):
                Range in the allowed exposure time for a frame of type
                ``ftype``. See
                :func:`pypeit.core.framematch.check_frame_exptime`.

        Returns:
            `numpy.ndarray`_: Boolean array with the flags selecting the
            exposures in ``fitstbl`` that are ``ftype`` type frames.
        """
        good_exp = framematch.check_frame_exptime(fitstbl['exptime'], exprng)
        # TODO: Allow for 'sky' frame type, for now include sky in
        # 'science' category
        if ftype in ['science', 'standard']:
            return good_exp & (fitstbl['lampstat01'] == 'lamp_off') & (fitstbl['idname'] == 'EXPOSE') & (fitstbl['dispname'] != 'open')
        if ftype == 'bias':
            return good_exp & (fitstbl['idname'] =='BIAS')   
        if ftype in ['pixelflat', 'trace', 'illumflat']:
            # Flats and trace frames are typed together
            return good_exp & (fitstbl['idname'] == 'LAMPFLAT')
        if ftype == 'pinhole':
            # Don't type pinhole
            return np.zeros(len(fitstbl), dtype=bool)
        if ftype in ['arc', 'tilt']:
            return good_exp & (fitstbl['idname'] == 'EXPOSE') & (fitstbl['lampstat01'] != 'lamp_off') & (fitstbl['dispname'] != 'open')

        msgs.warn('Cannot determine if frames are of type {0}.'.format(ftype))
        return np.zeros(len(fitstbl), dtype=bool)
    
    def bpm(self, filename, det, shape=None, msbias=None):
        """
        Generate a default bad-pixel mask.

        Even though they are both optional, either the precise shape for
        the image (``shape``) or an example file that can be read to get
        the shape (``filename`` using :func:`get_image_shape`) *must* be
        provided.

        Args:
            filename (:obj:`str` or None):
                An example file to use to get the image shape.
            det (:obj:`int`):
                1-indexed detector number to use when getting the image
                shape from the example file.
            shape (tuple, optional):
                Processed image shape
                Required if filename is None
                Ignored if filename is not None
            msbias (`numpy.ndarray`_, optional):
                Processed bias frame used to identify bad pixels

        Returns:
            `numpy.ndarray`_: An integer array with a masked value set
            to 1 and an unmasked value set to 0.  All values are set to
            0.
        """

        # Call the base-class method to generate the empty bpm
        bpm_img = super().bpm(filename, det, shape=shape, msbias=msbias)

        return bpm_img
