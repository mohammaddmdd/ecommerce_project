from enum import Enum
from .typing import (
    Byte,
    MegaByte,
    Dimension
)


class ImageExtensionEnum(Enum):
    JPG = ['JPG', 'JPEG', 'jpg', 'jpeg']
    PNG = ['PNG', 'png']
    GIF = ['GIF', 'gif']
    BMP = ['BMP', 'bmp']
    TIFF = ['TIFF', 'tiff']
    WEBP = ['WEBP', 'webp']


class RegexPatternEnum(Enum):
    IRAN_PHONE_NUMBER = r'^(\+98|0)?9\d{9}$'
    INTERNATIONAL_PHONE_NUMBER = r'^(\(?\+?[0-9]*\)?)?[0-9_\- \(\)]*$'
    EMAIL_ADDRESS = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
    IPV4 = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    CREDIT_CARD = r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|(222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})$'
    SOCIAL_SECURITY_NUMBER = r'^\d{3}-\d{2}-\d{4}$'
    HEX_COLOR_CODE = r'^#?([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$'
    TIME_IN_12_FORMAT = r'^(1[0-2]|0?[1-9]):[0-5]0-9?(?i)(am|pm)$'
    URL = r'^https?://(www.)?[-a-zA-Z0-9@:%.+~#=]{1,256}.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%+.~#?&//=]*)$'
    PERSIAN_NATIONAL_ID = r'^(?=.*\d)[\dX]{10}$'
    PASSPORT_ID = r'^[A-Z]{2}\d{7}$'
    STRONG_PASSWORD = r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'

class URLRegexPatternEnum(Enum):
    Url_slug_finder = r'(?P<slug>[-\w]+)'
    Url_pk_finder = r'(?P<pk>\d+)'
    Url_username_finder = r'(?P<username>[\w.@+-]+)'
    Url_year_finder = r'(?P<year>[0-9]{4})'
    Url_month_finder = r'(?P<month>[0-9]{2})'
    Url_day_finder = r'(?P<day>[0-9]{2})'


class VisualStudioCodeEnum(Enum):
    Image_source = r'src="([A-Za-z0-9/-]+\.[a-z]+)"'
    Replace_django_static = r'src="{% static \'$1\' %}"'


class FileSizeEnum(Enum):
    TINY = Byte(1024)
    SMALL = MegaByte(1)
    MEDIUM = MegaByte(5)
    LARGE = MegaByte(10)
    XLARGE = MegaByte(50)


class ImageDimensionEnum(Enum):
    SMALL = Dimension("100x100")
    MEDIUM = Dimension("500x500")
    LARGE = Dimension("1000x1000")
    XLARGE = Dimension("5000x5000")
    FULL = Dimension("original")


class VideoDimensionEnum(Enum):
    SMALL = Dimension("320x240")
    MEDIUM = Dimension("640x480")
    LARGE = Dimension("1280x720")
    XLARGE = Dimension("1920x1080")
    FULL = Dimension("original")

class AudioBitrateEnum(Enum):
    LOW = 64
    MEDIUM = 128
    HIGH = 256
    VERY_HIGH = 320
    EXTRA_HIGH = 'lossless'

class VideoBitrateEnum(Enum):
    LOW = 64
    MEDIUM = 128
    HIGH = 256
    VERY_HIGH = 320
    EXTRA_HIGH = 'lossless'

class VideoFrameRateEnum(Enum):
    LOW = 30
    MEDIUM = 60
    HIGH = 120
    VERY_HIGH = 240
    EXTRA_HIGH = 'lossless'

class AudioSampleRateEnum(Enum):
    LOW = 8000
    MEDIUM = 44100
    HIGH = 48000
    VERY_HIGH = 96000
    EXTRA_HIGH = 'lossless'

class AudioChannelsEnum(Enum):
    MONO = 1
    STEREO = 2
    SURROUND = 4
    EXTRA_HIGH = 8
    EXTREME_HIGH = 'lossless'

class VideoResolutionEnum(Enum):
    LOW = "480p"
    MEDIUM = "720p"
    HIGH = "1080p"
    VERY_HIGH = "4K"
    EXTRA_HIGH = "8K"
    EXTREME_HIGH = "16K"
    LOSS_LESS = "lossless"
