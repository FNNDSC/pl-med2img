#!/usr/bin/env python                                            
#
# med2img ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#               http://childrenshospital.org/FNNDSC/
#                         dev@babyMRI.org
#
#   Thin plugin wrapper about a `med2image` module.
#

import  os

import  sys

from    chrisapp.base  import ChrisApp
from    med2image      import med2image
import  pudb

Gstr_title = """
                    _  _____ _                 
                   | |/ __  (_)                
 _ __ ___   ___  __| |`' / /'_ _ __ ___   __ _ 
| '_ ` _ \ / _ \/ _` |  / / | | '_ ` _ \ / _` |
| | | | | |  __/ (_| |./ /__| | | | | | | (_| |
|_| |_| |_|\___|\__,_|\_____/_|_| |_| |_|\__, |
                                          __/ |
                                         |___/ 
"""

shortSynopsis = '''

    NAME

       med2img 

    SYNOPSIS

        med2img                                                         \\
            [--inputFileSubStr <substr>]                                \\
            [-o|--output <outputFileStem>]                              \\
            [-t|--outputFileType <outputFileType>]                      \\
            [-s|--sliceToConvert <sliceToConvert>]                      \\
            [--convertOnlySingleDICOM]                                  \\
            [-f|--frameToConvert <frameToConvert>]                      \\
            [--showSlices]                                              \\
            [--func <functionName>]                                     \\
            [--reslice]                                                 \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                                 \\
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing          \\
                fnndsc/pl-med2img med2img                               \\
                /incoming /outgoing
'''

description = '''
    DESCRIPTION

        The `med2img` plugin is a thin wrapper about a `med2image` module. 
        This plugin is little more than a ChRIS DS-ified version about this
        module and as serves as little more than a vehicle to expose the 
        `med2image` CLI and run appropriately.

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

        [--inputFile <file>]
        If specified, only process <file>.

        [--inputFileSubStr <substr>]
        As a convenience, the input file can be determined via a substring
        search of all the files in the <inputDir> using this flag. The first
        filename hit that contains the <substr> will be assigned the
        <inputFile>.
        
        This flag is useful is input names are long and cumbersome, but
        a short substring search would identify the file. For example, an
        input file of
        
            0043-1.3.12.2.1107.5.2.19.45152.2013030808110149471485951.dcm
        
        can be specified using ``--inputFileSubStr 0043-``        

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
        
        [--convertOnlySingleDICOM]
        If specified, will only convert the single DICOM specified by the
        '--inputFile' flag. This is useful for the case when an input
        directory has many DICOMS but you specifially only want to convert
        the named file. By default the script assumes that multiple DICOMS
        should be converted en mass otherwise.
        
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

'''

class Med2img(ChrisApp):
    """
    An app to ...
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS plugin app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = '' # url of an icon image
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('-i', '--inputFile',
                            dest        = 'inputFile',
                            type        = str,
                            optional    = True,
                            help        = 'name of the input file within the inputDir',
                            default     = ''
                        )
        self.add_argument("--inputFileSubStr",
                            help        = "input file substring to tag a file in the inputDir",
                            dest        = 'inputFileSubStr',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument('-o', '--outputFileStem',
                            dest        = 'outputFileStem',
                            type        = str,
                            optional    = True,
                            help        = 'output file stem name (with optional extension)',
                            default     = 'sample'
                        )
        self.add_argument('-t', '--outputFileType',
                            dest        = 'outputFileType',
                            type        = str,
                            default     = '',
                            optional    = True,
                            help        = 'output image file format'
                        )
        self.add_argument('-s', '--sliceToConvert',
                            dest        = 'sliceToConvert',
                            type        = str,
                            default     = "-1",
                            optional    = True,
                            help        = 'slice to convert (for 3D data)'
                        )
        self.add_argument('-f', '--frameToConvert',
                            dest        = 'frameToConvert',
                            type        = str,
                            default     = "-1",
                            optional    = True,
                            help        = 'frame to convert (for 4D data)'
                        )
        self.add_argument('--printElapsedTime',
                            dest        = 'printElapsedTime',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'print program run time'
                        )
        self.add_argument('-r', '--reslice',
                            dest        = 'reslice',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'save images along i, j, k direction -- 3D input only'
                        )
        self.add_argument('--showSlices',
                            dest        = 'showSlices',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'show slices that are converted'
                        )
        self.add_argument('--func',
                            dest        = 'func',
                            type        = str,
                            default     = '',
                            optional    = True,
                            help        = 'apply the specified transformation function before saving'
                        )
        self.add_argument('-y', '--synopsis',
                            dest        = 'synopsis',
                            type        = bool,
                            action      = 'store_true',
                            default     = False,
                            optional    = True,
                            help        = 'short synopsis'
                        )
        self.add_argument("--convertOnlySingleDICOM",
                            help        = "if specified, only convert the specific input DICOM",
                            dest        = 'convertOnlySingleDICOM',
                            type        = bool,
                            optional    = True,
                            action      = 'store_true',
                            default     = False
                        )


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        for k,v in options.__dict__.items():
            print("%25s:  [%s]" % (k, v))
        print("")    
        # The med2image module has slightly different variable
        # names for the same concept... convert from the plugin
        # name to the module name:
        options.inputDir        = options.inputdir
        options.outputDir       = options.outputdir

        if options.man or options.synopsis:
            if options.man:
                str_help = self.show_man_page(False)
            else:
                str_help = self.show_man_page(True)
            print(str_help)
            sys.exit(1)

        imgConverter = med2image.object_factoryCreate(options).C_convert

        if options.func:
            imgConverter.func = options.func

        imgConverter.tic()
        imgConverter.run()

        if options.printElapsedTime:
            print("Elapsed time = %f seconds" % imgConverter.toc())
            sys.exit(0)

    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_title + shortSynopsis + description)
