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

Run
===

Using ``docker run``
--------------------

Assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``

.. code-block:: bash

    docker run --rm                                                     \
        -v $(pwd)/out:/incoming                                         \
        -v $(pwd)/out2:/outgoing                                        \
        fnndsc/pl-med2img                                                \
        med2img.py --bucket bch-fnndsc --prefix test /incoming /outgoing

The above will push a copy of each file/folder in the container's ``/incoming``
storage and prefix the copy with the ``prefix`` text (in this case "test"). Some
metadata files will be written to the container's ``/outgoing`` directory.

Make sure that the host ``$(pwd)/out`` directory is world readable and ``$(pwd)/out2``
directory is world writable!
