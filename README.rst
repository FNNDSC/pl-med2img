##########
pl-med2img
##########


Abstract
========

``pl-med2img`` is a ChRIS ``DS`` plugin that converts medical image data files (``DICOM`` and ``NifTI``) to web display-friendly formats (like ``png`` and ``jpg``). This plug-in is a really a simple wrapper around the ``med2image`` application which is the actual workhorse converting ``NIfTI`` volumes or ``DICOM`` files to ``png`` or ``jpg`` formats. To better understand ``med2image`` and its features, please take a look at its repo: https://github.com/FNNDSC/med2image


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

This plugin can be run in two modes: 

1. Natively as a python package
2. As a containerized docker image.

Clone the git repository ``FNNDSC/pl-med2img`` in the current working directory (which also contains ``SAG-anon-nii`` and ``SAG-anon``) using the following command

::

    git clone https://github.com/FNNDSC/pl-med2img.git


Natively
^^^^^^^^

Clone the repo and ``pip install`` the package

::
    pip install -r requirements.txt
    pip install .

Make sure that your current working directory is the one that contains the 3 directories: ``pl-med2img``, ``SAG-anon-nii``, and ``SAG-anon``


**EXAMPLES:**

**NIFTI volume:**

Create a directory called ``image-results-nii`` in the current working directory.

Run ``med2img``  using the following command to convert the NIfTI volume within the ``SAG-anon-nii`` directory to images:

::

    med2img                                             \
        -i SAG-anon.nii                                 \
        -o sample.png                                   \
        ./SAG-anon-nii ./image-results-nii

**DICOM files:**

Create a directory called ``image-results-dcm`` in the current working directory.

Run ``med2img`` file using the following command to convert all DICOM files within the ``SAG-anon`` directory to images:

::

    med2img                                                              \
        -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm \
        -o sample.png                                                    \
        ./SAG-anon ./image-results-DICOM                 

Using ``docker`` (preferred)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**NOTE:** Make sure that your current working directory is the one that contains the 3 directories: ``pl-med2img``, ``SAG-anon-nii``, and ``SAG-anon``

First, pull the docker image using the following command:

::

    docker pull fnndsc/pl-med2img .

Now, to run the docker image, see the following examples:

**EXAMPLES:**

**NIFTI volume:**

Run the docker image ``fnndsc/pl-med2img`` using the following command to convert the NIfTI files within the ``SAG-anon-nii`` directory to images:


.. code-block:: bash

    docker run --rm                                         \
        -v $PWD/SAG-anon-nii/:/incoming                     \
        -v $PWD/image-results-nii/:/outgoing                \
        fnndsc/pl-med2img med2img                           \
        -i SAG-anon.nii                                     \
        -o sample.png                                       \
         /incoming /outgoing

**DICOM files:**

Run the docker image ``fnndsc/pl-med2img`` using the following command to convert the DICOM files within the ``SAG-anon`` directory to images:

.. code-block:: bash

    docker run --rm                                                        \
        -v $PWD/SAG-anon/:/incoming                                        \
        -v $PWD/image-results-dcm/:/outgoing                               \
        fnndsc/pl-med2img med2img                                          \
        -i 0001-1.3.12.2.1107.5.2.19.45152.2013030808110258929186035.dcm   \
        -o sample.png                                                      \
         /incoming /outgoing

The above NIfTI or DICOM examples will push a copy of each file/folder in the container's ``/incoming``
storage. Some metadata files will be written to the container's ``/outgoing`` directory.

Make sure that the host ``$PWD/SAG-anon-nii`` or ``$PWD/SAG-anon`` directory is world readable and ``$PWD/image-results-nii`` or ``$PWD/image-results``
directory is world writable!

Development
^^^^^^^^^^^

To develop ``pl-med2img`` from within a containerized deployment, do

.. code-block:: bash

    docker run --rm -it                                                     \
        -v $PWD/med2img:/usr/local/lib/python3.8/dist-packages/med2img:ro   \ 
        -v $PWD/in:/incoming:ro -v $PWD/out:/outgoing:rw                    \
        fnndsc/pl-med2img med2img                                           \
        --inputFileSubStr "dcm" --sliceToConvert 0                          \
        /incoming /outgoing

(obviously in the above use whatever CLI flags are relevant to your debugging case).

*-30-*