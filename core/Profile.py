class Profile:
    """ Domain Class that will hold the different normalizations of a profile. """

    def __init__(self, raw_profile):
        self.raw_profile = raw_profile
        self.common_processed_profile = None
        self.metric_processed_profile = None