import torch
import gc
import folder_paths
import os
import comfy.model_management

from ..Utils import AnyType
from ..ErrorHandler import ErrorHandler

input_dir = folder_paths.get_input_directory()
output_dir = folder_paths.get_output_directory()

def clear_memory():
    # Cleanup
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

def clear_input():
    for file in os.listdir(input_dir):
        # Exclude Example Img
        if file != "example.png":
            if not os.path.isdir(file):            
                os.remove(os.path.join(input_dir, file))

def clear_output():
    # Clear Dir
    for file in os.listdir(output_dir):
        if not os.path.isdir(file):
            os.remove(os.path.join(output_dir, file))
     
any = AnyType("*")
class ClearNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (any, {}),
                "clear_cache": ("BOOLEAN", {"default": True}),
                "clear_models": ("BOOLEAN", {"default": True}),
                "clear_input_dir": ("BOOLEAN", {"default": False}),
                "clear_output_dir": ("BOOLEAN", {"default": False}),        
            },
            "optional": {
            }
        }

    CATEGORY = 'rework-x/utils'

    RETURN_TYPES = ()
    FUNCTION = "clear"

    OUTPUT_NODE = True

    def clear(self, anything, clear_cache, clear_models, clear_input_dir, clear_output_dir):
        try:
            if clear_cache:
                clear_memory()
                
            if clear_models:
                comfy.model_management.unload_all_models()
                comfy.model_management.soft_empty_cache()
            
            if clear_input_dir:
                clear_input()
                
            if clear_output_dir:
                clear_output()
                
        except Exception:
            ErrorHandler().handle_error("utils", f"Error Clearing.")
            return (None, )
        
        return (None,)
