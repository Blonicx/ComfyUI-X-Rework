import toml
import os
import pathlib

from .src.py.utils.ClearNode import ClearNode
from .src.py.img.LoadImage import LoadImageURL
from .src.py.img.UploadImage import UploadImage
from .src.py.img.SaveImage import XSave
from .src.py.sampler.XSampler import XSampler

config_path = pathlib.Path(__file__).parent.resolve()
config = None

with open(os.path.join(config_path,'pyproject.toml'), 'r') as f:
    config = toml.load(f)

XREWORK_COMFYUI_VERSION = config['project']['version']

RESET_COLOR = "\033[0m"
GREEN_COLOR = "\033[92m"
LIGHT_BROWN = "\033[38;5;173m"
print("[" + LIGHT_BROWN + "STATUS" + RESET_COLOR + "] " + GREEN_COLOR + f"X-Rework Version {XREWORK_COMFYUI_VERSION} loaded successfully!" + RESET_COLOR)

NODE_CLASS_MAPPINGS = {
    "ClearNode" : ClearNode,
    "LoadImageURL" : LoadImageURL,
    "UploadImage" : UploadImage,
    "XSave" : XSave,
    #"XSampler" : XSampler,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ClearNode" : "ClearNode",
    "LoadImageURL" : "LoadImage (URL)",
    "UploadImage" : "UploadImage (DISCORD)",
    "XSave" : "XSave",    
    #"XSampler" : "XSampler",
}

WEB_DIRECTORY = "./src/web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']