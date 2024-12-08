import requests
import folder_paths
import os
import json
import time
import numpy as np

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args

from ..ErrorHandler import ErrorHandler

class UploadImage:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "webhook_url": ("STRING", {"default" : ""}),
            },
            "optional": {
            }
        }
    
    CATEGORY = 'x-rework/image'
    
    RETURN_TYPES = ()
    FUNCTION = "upload_image"
    
    OUTPUT_NODE = True    
    
    def upload_image(self, images, webhook_url, filename_prefix="temp", prompt=None, extra_pnginfo=None):
        try:
            filename_prefix += self.prefix_append
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
            for (batch_number, image) in enumerate(images):
                i = 255. * image.cpu().numpy()
                img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                metadata = None
                if not args.disable_metadata:
                    metadata = PngInfo()
                    if prompt is not None:
                        metadata.add_text("prompt", json.dumps(prompt))
                    if extra_pnginfo is not None:
                        for x in extra_pnginfo:
                            metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                file = f"temp_file.png"
                img_path = os.path.join(full_output_folder, file)
                img.save(img_path, pnginfo=metadata, compress_level=self.compress_level)

                file = open(img_path, 'rb')

                files = {
                    'media': file
                }

                requests.post(webhook_url, files=files)
                
                file.close()
        
        except Exception as e:
            ErrorHandler().handle_error("image", f"Error sending image to {webhook_url}.")
            return (None, )
        
        finally:
            os.remove(img_path)
            
        return ()
