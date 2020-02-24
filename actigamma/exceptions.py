"""
    All ActiGamma exception definitions
"""


class ActiGammaException(Exception):
    """
        Base exception for all ActiGamma exceptions
    """


class AbstractClassException(ActiGammaException):
    """
        Exception for all intantiating abstract classes
    """


class UnphysicalValueException(ActiGammaException):
    """
        Exception for all using or defining unphysical values
        such as negative mass or energy
    """


class UnknownOrUnstableNuclideException(ActiGammaException):
    """
        Exception for a nuclide that is unknown in the database
    """


class NoDataException(ActiGammaException):
    """
        Exception for missing data in the database
    """
