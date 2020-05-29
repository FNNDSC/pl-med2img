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
import sys
import traceback
from pydoc import synopsis

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
    VERSION         = '0.1.1'
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
        self.add_argument('-i', '--inputFile', dest='inputFile', type=str,
                          optional=False, help='name of the input file within the inputDir')

        # self.add_argument('-d', dest='outputDir', type=str, optional=False,
        #                   help='output image Directory', default='') #default?
        #
        # self.add_argument('-I', '--inputDir', dest='inputDir', type=str,
        #                   optional=False, help='input Directory', default='')

        self.add_argument('-o', '--outputFileStem', dest='outputFileStem', type=str, optional=True,
                          help='output file', default='sample')

        self.add_argument('-t', '--outputFileType', dest='outputFileType', type=str,
                          default='jpg', optional=True, help='output image file format')

        self.add_argument('-s' '--sliceToConvert', dest='sliceToConvert', type=str,
                          default="-1", optional=True, help='slice to convert (for 3D data)')

        self.add_argument('-f', '--frameToConvert', dest='frameToConvert', type=str,
                          default="-1", optional=True, help='frame to convert (for 4D data)')

        self.add_argument('--printElapsedTime', dest='printElapsedTime', type=str, action='store_true',
                          default=False, optional=True, help='print program run time')

        self.add_argument('-r', '--reslice', dest='reslice', type=bool, action='store_true',
                          default=False, optional=True, help='save images along i, j, k direction -- 3D input only')

        self.add_argument('--showSlices', dest='showSlices', type=bool, action='store_true',
                          default=False, optional=True, help='show slices that are converted')

        self.add_argument('--func', dest='func', type=str, default='', optional=True,
                          help='apply the specified transformation function before saving')

        # self.add_argument('-x', '--man', dest='man', type=bool, action='store_true',
        #                   default=False, optional=True, help='man')

        self.add_argument('-y', '--synopsis', dest='synopsis', type=bool, action='store_true',
                          default=False, optional=True, help='short synopsis')

        # self.add_argument('--version', dest='b_version', type=bool, action='store_true',
        #                   default=False, optional=True, help='if specified, print version number')


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        try:
            options.inputDir = options.inputdir
            options.outputDir = options.outputdir
            options.sliceToConvert = options.sliceToConvert
            options.frameToConvert = options.frameToConvert

            imgConverter = med2image.object_factoryCreate(options).C_convert

            if options.version:
                print("Version: %s" % options.version)
                sys.exit(1)

            if options.man or options.synopsis:
                print(options.synopsis)
                if options.man:
                    str_help = synopsis(False)
                else:
                    str_help = synopsis(True)
                print(str_help)
                sys.exit(1)

            if options.func:
                imgConverter.func = options.func

            imgConverter.tic()
            imgConverter.run()

            # if b_dicomExt:
            #     break

            if options.printElapsedTime:
                print("Elapsed time = %f seconds" % imgConverter.toc())
                sys.exit(0)

        except Exception as e:
            traceback.print_exc()


# ENTRYPOINT
if __name__ == "__main__":
    app = Med2ImgApp()
    app.launch()
