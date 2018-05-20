import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_resource_path(resource):
    return os.path.join(PROJECT_DIR, '../res', resource)
