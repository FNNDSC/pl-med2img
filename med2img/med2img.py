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

    def define_parameters(self):
        self.add_parameter('--outputFileType', action='store', dest='outputFileType',
                           type=str, default='jpg', optional=True,
                           help='output image file format')
        self.add_parameter('--sliceToConvert', action='store', dest='sliceToConvert',
                           type=int, default=-1, optional=True,
                           help='slice to convert (for 3D data)')

    def run(self, options):
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
                        C_convert.run()

                    if b_dicomExt:
                        C_convert = med2image.med2image_dcm(
                            inputFile=inputFile,
                            outputDir=output_path,
                            outputFileStem='.'.join(fname.split('.')[:-1]),
                            outputFileType=options.outputFileType,
                            sliceToConvert=str(options.sliceToConvert),
                            reslice=False
                        )
                        C_convert.run()
                        break
                except Exception as e:
                    print(e)


# ENTRYPOINT
if __name__ == "__main__":
    app = Med2ImgApp()
    app.launch()
