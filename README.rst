##########
pl-med2img
##########


Abstract
========

A Chris 'ds' plugin to convert from medical image data files to display-friendly formats
(like png and jpg).

Preconditions
=============

This plugin requires input and output directories as a precondition.

How to pull medical image data
==============================

These medical image data files are in 2 formats:
- NIfTI
- DICOM

The following steps show how to pull sample files for NIfTI or DICOM files.

Pull NIfTI
^^^^^^^^^^

The input should be a NIfTI volume with extension .nii.

We provide a sample volume here https://github.com/FNNDSC/SAG-anon-nii.git

- Clone this repository (SAG-anon-nii) to your local computer.

::

    git clone https://github.com/FNNDSC/SAG-anon-nii.git

Pull DICOM
^^^^^^^^^^

The input should be a DICOM file usually with extension .dcm

We provide a sample directory of .dcm images here. (https://github.com/FNNDSC/SAG-anon.git)

-   Clone this repository (SAG-anon) to your local computer.

::

    git clone https://github.com/FNNDSC/SAG-anon.git

Run
===

**NOTE:** Make sure that the 3 directories: ``pl-med2img``, ``SAG-anon-nii``, and ``SAG-anon`` are all within the same directory.

This plugin can be run in two modes: natively as a python package or as a containerized docker image.

Clone the git repository ``FNNDSC/pl-med2img`` in the current working directory (which also contains ``SAG-anon-nii`` and ``SAG-anon``) using the following command

::

    git clone https://github.com/FNNDSC/pl-med2img.git

**NOTE:**

- This plug-in is a wrap around the ``med2image`` application.

- You can go through more details to understand the various Command Line Arguments of the ``med2image`` application using the following link:

::

    https://github.com/FNNDSC/med2image


Using python `.py` file
^^^^^^^^^^^^^^^^^^^^^^^

Make sure that your current working directory is the one that contains the 3 directories: ``pl-med2img``, ``SAG-anon-nii``, and ``SAG-anon``


**EXAMPLES:**

**NIFTI volume:**

Create a directory called ``image-results-nii`` in the current working directory.

Run the ``med2img.py`` file using the following command to convert the NIfTI volume within the ``SAG-anon-nii`` directory to images:

::

    python3 pl-med2img/med2img/med2img.py           \
    /SAG-anon-nii/ /image-results-nii/              \
    -i SAG-anon.nii                                 \
    -o sample.png

**DICOM files:**

Create a directory called ``image-results-dcm`` in the current working directory.

Run the ``med2img.py`` file using the following command to convert the DICOM files within the ``SAG-anon`` directory to images:

::

    python3 pl-med2img/med2img/med2img.py                            \
    /SAG-anon/ /image-results-dcm/                                   \ 
    -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm \
    -o sample.png

Using ``docker run``
^^^^^^^^^^^^^^^^^^^^
**NOTE:** Make sure that your current working directory is the one that contains the 3 directories: ``pl-med2img``, ``SAG-anon-nii``, and ``SAG-anon``

First, build a docker image using the following command:

::

    docker build -t fnndsc/pl-med2img .

Now, to run the docker image, see the following examples:

**EXAMPLES:**

**NIFTI volume:**

Run the docker image ``fnndsc/pl-med2img`` using the following command to convert the NIfTI files within the ``SAG-anon-nii`` directory to images:


.. code-block:: bash

    docker run --rm                                         \
        -v $(pwd)/SAG-anon-nii/:/incoming                   \
        -v $(pwd)/image-results-nii/:/outgoing              \
        fnndsc/pl-med2img med2img.py                        \
        -i SAG-anon.nii                                     \
        -o sample.png                                       \
         /incoming /outgoing

**DICOM files:**

Run the docker image ``fnndsc/pl-med2img`` using the following command to convert the DICOM files within the ``SAG-anon`` directory to images:

.. code-block:: bash

    docker run --rm                                                        \
        -v $(pwd)/SAG-anon/:/incoming                                      \
        -v $(pwd)/image-results-dcm/:/outgoing                             \
        fnndsc/pl-med2img med2img.py                                       \
        -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm   \
        -o sample.png                                                      \
         /incoming /outgoing

The above NIfTI or DICOM examples will push a copy of each file/folder in the container's ``/incoming``
storage. Some metadata files will be written to the container's ``/outgoing`` directory.

Make sure that the host ``$(pwd)/SAG-anon-nii`` or ``$(pwd)/SAG-anon`` directory is world readable and ``$(pwd)/image-results-nii`` or ``$(pwd)/image-results``
directory is world writable!
