#                                                            _
# S3 Push ds app
#
# (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os

# import the Chris app superclass
from chrisapp.base import ChrisApp
from med2image import med2image


class Med2ImgApp(ChrisApp):
    """
    Converts medical image data files in input directory to png, jpg, etc ...
    """
    AUTHORS         = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH        = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC        = os.path.basename(__file__)
    EXECSHELL       = 'python3'
    TITLE           = 'Med2Img'
    CATEGORY        = ''
    TYPE            = 'ds'
    DESCRIPTION     = 'An app to convert from medical image data files to png, jpg, etc ...'
    DOCUMENTATION   = 'http://wiki'
    LICENSE         = 'Opensource (MIT)'
    VERSION         = '0.1'
    MAX_NUMBER_OF_WORKERS = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS = 1  # Override with integer value
    MAX_CPU_LIMIT = ''  # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT = ''  # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT = ''  # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT = ''  # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """
        self.add_argument('--outputFileType', dest='outputFileType', type=str,
                          default='jpg', optional=True, help='output image file format')
        self.add_argument('--sliceToConvert', dest='sliceToConvert', type=int,
                          default=-1, optional=True, help='slice to convert (for 3D data)')
        self.add_argument('--func', dest='func', type=str, default='', optional=True,
                          help='apply the specified transformation function before saving')

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        for (dirpath, dirnames, filenames) in os.walk(options.inputdir):
            output_path = dirpath.replace(options.inputdir, options.outputdir).rstrip('/')
            for dirname in dirnames:
                print('Creating directory... %s' % os.path.join(output_path, dirname))
                os.makedirs(os.path.join(output_path, dirname))
            for fname in filenames:
                inputFile = os.path.join(dirpath, fname)
                try:
                    str_inputFileStem, str_inputFileExtension = os.path.splitext(inputFile)
                    b_niftiExt = (str_inputFileExtension == '.nii' or
                                  str_inputFileExtension == '.gz')
                    b_dicomExt = str_inputFileExtension == '.dcm'

                    if b_niftiExt:
                        C_convert = med2image.med2image_nii(
                            inputFile=inputFile,
                            outputDir=output_path,
                            outputFileStem=fname.split('.')[0],
                            outputFileType=options.outputFileType,
                            sliceToConvert=str(options.sliceToConvert),
                            frameToConvert='-1',
                            showSlices=False,
                            reslice=False
                        )

                    if b_dicomExt:
                        C_convert = med2image.med2image_dcm(
                            inputFile=inputFile,
                            outputDir=output_path,
                            outputFileStem='.'.join(fname.split('.')[:-1]),
                            outputFileType=options.outputFileType,
                            sliceToConvert=str(options.sliceToConvert),
                            reslice=False
                        )

                    if options.func:
                        C_convert.func = options.func
                    C_convert.run()

                    if b_dicomExt:
                        break
                except Exception as e:
                    print(e)


# ENTRYPOINT
if __name__ == "__main__":
    app = Med2ImgApp()
    app.launch()
