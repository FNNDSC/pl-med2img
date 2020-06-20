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

        self.add_argument('-o', '--outputFileStem', dest='outputFileStem', type=str, optional=True,
                          help='output file', default='sample')

        self.add_argument('-t', '--outputFileType', dest='outputFileType', type=str,
                          default='jpg', optional=True, help='output image file format')

        self.add_argument('-s' '--sliceToConvert', dest='sliceToConvert', type=str,
                          default="-1", optional=True, help='slice to convert (for 3D data)')

        self.add_argument('-f', '--frameToConvert', dest='frameToConvert', type=str,
                          default="-1", optional=True, help='frame to convert (for 4D data)')

        self.add_argument('--printElapsedTime', dest='printElapsedTime', type=bool, action='store_true',
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

    def show_man_page(self, ab_shortOnly=False):
        scriptName = os.path.basename(sys.argv[0])
        shortSynopsis = '''
        NAME

    	    pl-med2img - convert medical images to jpg/png/etc.

        SYNOPSIS

                %s                                       \\
                         -i|--input <inputFile>                 \\
                        [-d|--outputDir <outputDir>]            \\
                         -o|--output <outputFileStem>           \\
                        [-t|--outputFileType <outputFileType>]  \\
                        [-s|--sliceToConvert <sliceToConvert>]  \\
                        [-f|--frameToConvert <frameToConvert>]  \\
                        [--showSlices]                          \\
                        [--func <functionName>]                 \\
                        [--reslice]                             \\
                        [-x|--man]                              \\
                        [-y|--synopsis]

        
        ''' % scriptName

        description = '''
        DESCRIPTION

            `%s' converts input medical image formatted data to a more
            display friendly format, such as jpg or png.

            Currently understands NIfTI and DICOM input formats.

        ARGS

            -i|--inputFile <inputFile>
            Input file to convert. Typically a DICOM file or a nifti volume.

            [-d|--outputDir <outputDir>]
            The directory to contain the converted output image files.

            -o|--outputFileStem <outputFileStem>
            The output file stem to store conversion. If this is specified
            with an extension, this extension will be used to specify the
            output file type.

            SPECIAL CASES:
            For DICOM data, the <outputFileStem> can be set to the value of
            an internal DICOM tag. The tag is specified by preceding the tag
            name with a percent character '%%', so 

                -o %%ProtocolName

            will use the DICOM 'ProtocolName' to name the output file. Note
            that special characters (like spaces) in the DICOM value are 
            replaced by underscores '_'.

            Multiple tags can be specified, for example

                -o %%PatientName%%PatientID%%ProtocolName

            and the output filename will have each DICOM tag string as 
            specified in order, connected with dashes.

            A special %%inputFile is available to specify the input file that
            was read (without extension).

            [-t|--outputFileType <outputFileType>]
            The output file type. If different to <outputFileStem> extension,
            will override extension in favour of <outputFileType>.

            [-s|--sliceToConvert <sliceToConvert>]
            In the case of volume files, the slice (z) index to convert. Ignored
            for 2D input data. If a '-1' is sent, then convert *all* the slices.
            If an 'm' is specified, only convert the middle slice in an input
            volume.

            [-f|--frameToConvert <sliceToConvert>]
            In the case of 4D volume files, the volume (V) containing the
            slice (z) index to convert. Ignored for 3D input data. If a '-1' is
            sent, then convert *all* the frames. If an 'm' is specified, only
            convert the middle frame in the 4D input stack.

            [--showSlices]
            If specified, render/show image slices as they are created.

            [--func <functionName>]
            Apply the specified transformation function before saving. Currently 
            support functions:

                * invertIntensities
                  Inverts the contrast intensity of the source image.

            [--reslice]
            For 3D data only. Assuming [i,j,k] coordinates, the default is to save
            along the 'k' direction. By passing a --reslice image data in the 'i' and
            'j' directions are also saved. Furthermore, the <outputDir> is subdivided into
            'slice' (k), 'row' (i), and 'col' (j) subdirectories.

            [-x|--man]
            Show full help.

            [-y|--synopsis]
            Show brief help.

                ''' % (scriptName)
                
        if ab_shortOnly:
            return shortSynopsis
        else:
            return shortSynopsis + description

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
                if options.man:
                    str_help = self.show_man_page(False)
                else:
                    str_help = self.show_man_page(True)
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
