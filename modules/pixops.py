import jiplib as _jl


class _PixOps():
    def __init__(self, jim_object):
        """Initialize the module.

        :param jim_object: parent Jim object to have access to its attributes
        """
        self._jim_object = jim_object

    def pointOpBitWise(self, sec_jim_object, operation_code):
        """Bitwise operation between two images.

        Modifies the instance on which the method was called.

        :param sec_jim_object: a Jim object
        :param operation_code: 10 or AND op, 11 or OR op, and 12 or XOR op
        """
        self._jim_object._set(self._jim_object.pointOpBitwise(
            self._jim_object, sec_jim_object, operation_code))

    def pointOpBlank(self, value):
        """Set all pixels of image to value.

        Modifies the instance on which the method was called.

        :param value: new value for pixels of Jim object
        """
        self._jim_object.d_pointOpBlank(value)


    def convert(self, **kwargs):
        """Convert Jim image with respect to data type.

        :param kwargs: See table below
        Modifies the instance on which the method was called.


        +------------------+---------------------------------------------------------------------------------+
        | key              | value                                                                           |
        +==================+=================================================================================+
        | otype            | Data type for output image                                                      |
        +------------------+---------------------------------------------------------------------------------+
        | scale            | Scale output: output=scale*input+offset                                         |
        +------------------+---------------------------------------------------------------------------------+
        | offset           | Apply offset: output=scale*input+offset                                         |
        +------------------+---------------------------------------------------------------------------------+
        | autoscale        | Scale output to min and max, e.g., [0,255]                                      |
        +------------------+---------------------------------------------------------------------------------+
        | a_srs            | Override the projection for the output file                                     |
        +------------------+---------------------------------------------------------------------------------+

        .. note::
            To ignore some pixels from the extraction process, see list of :ref:`mask <extract_mask>` key values:

        Example:

        Convert data type of input image to byte using autoscale::

        jim0=jl.io.createJim('/path/to/raster.tif')
        jim0.convert(otype=Byte,autoscale=[0,255])

        Clip raster dataset between 0 and 255 (set all other values to 0), then convert data type to byte::

        jim1=jl.io.createJim('/path/to/raster.tif')
        jim1.setThreshold(min=0,max=255,nodata=0)
        jim1.convert({'otype':'Byte'})
        """
        self._jim_object._set(self._jim_object.convert(kwargs))

    def setThreshold(self, **kwargs):
        """Apply minimum and maximum threshold to pixel values in raster dataset.

        :param kwargs: See table below
        Modifies the instance on which the method was called.


        +------------------+---------------------------------------------------------------------------------+
        | key              | value                                                                           |
        +==================+=================================================================================+
        | min              | Minimum threshold value (if pixel value < min set pixel value to no data)       |
        +------------------+---------------------------------------------------------------------------------+
        | max              | Maximum threshold value (if pixel value < max set pixel value to no data)       |
        +------------------+---------------------------------------------------------------------------------+
        | value            | value to be set if within min and max                                           |
        |                  | (if not set, valid pixels will remain their input value)                        |
        +------------------+---------------------------------------------------------------------------------+
        | abs              | Set to True to perform threshold test to absolute pixel values                  |
        +------------------+---------------------------------------------------------------------------------+
        | nodata           | Set pixel value to this no data if pixel value < min or > max                   |
        +------------------+---------------------------------------------------------------------------------+

        Example:

        Mask all values not within [0,250] and set to 255 (no data)::

        jim_threshold=jim.setThreshold({'min':0,'max':250,'nodata':255})
        """
        # pointOpThres(IMAGE *im, G_TYPE gt1, G_TYPE gt2, G_TYPE gbg, G_TYPE gfg)
        gt1=
        self_jim_object.pointOpThres(gt1,gt2,gbg,gfg)
        self._jim_object._set(self._jim_object.setThreshold(kwargs))
