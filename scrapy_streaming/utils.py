import json
import os

from scrapy.utils.conf import closest_scrapy_cfg
from scrapy.utils.project import inside_project
from scrapy.utils.python import to_bytes


def get_project_root():
    """
    Returns the absolute path of the root of the project, and raise an exception
    if the current directory is not inside a project path
    """
    os.path.abspath('.')
    if inside_project():
        return os.path.dirname(closest_scrapy_cfg())
    raise Exception(os.getcwd(), " does not belong to a Scrapy project")


def dict_serialize(dict_obj, enc=None):
    """
    Serialize a dict object and converts it to bytes
    """
    return to_bytes(json.dumps(dict_obj), enc)


class WrongMessage(Exception):
    pass
