import os

from scrapy.utils.conf import closest_scrapy_cfg
from scrapy.utils.project import inside_project


def get_project_root():
    """
    Returns the absolute path of the root of the project
    """
    os.path.abspath('.')
    if inside_project():
        return os.path.dirname(closest_scrapy_cfg())
    return '.'
