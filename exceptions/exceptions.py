from os import EX_CANTCREAT


class SocialNetworkNotRecognizedException(Exception):
    """
    Raised when a record contains a social network that
    does not have an associated strategy.
    """

    pass


class MissingSocialNetworkException(Exception):
    """
    Raised when a record does not contain a social network
    in its partition_key
    """

    pass


class MissingKeyValueException(Exception):
    """
    Raised when a record is missing a (key,value).
    """
    

class InsertErrorException(Exception):
    """
    Raised when a processed profile could not be inserted into its corresponding table
    """