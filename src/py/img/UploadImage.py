import requests
import base64
import folder_paths
import os
import json
import time
import numpy as np

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args

from ..ErrorHandler import ErrorHandler

def upload_discord(webhook_url, img_path):
    if webhook_url != "":
        pass
    else: ErrorHandler().handle_error("image", f"Error sending image to {webhook_url}.")
    
    file = open(img_path, 'rb')

    files = {
        'media': file
    }

    requests.post(webhook_url, files=files)
    
    file.close()

def upload_imgur():
    headers = {
        'Authorization': 'Client-ID f1XXXXXXXXXXXXX',
    }

    params = {
    'image': base64.b64encode(open('images.png', 'rb').read())
    }

    response = requests.post(f'https://api.imgur.com/3/image', headers=headers, data=params)
    
    if response.status_code == 200:
        pass
    else: ErrorHandler().handle_error("image", f"Error uploading Image to Imgur.")

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
                "save_image": ("BOOLEAN", {"default": False}),
                "upload_imgur": ("BOOLEAN", {"default": False}),
                "webhook_url": ("STRING", {"default" : ""}, {"tooltip": "The Url the Image should be send to. Leave empty for X-Rework Discord."}),
            },
            "optional": {
            }
        }
    
    CATEGORY = 'x-rework/image'
    
    RETURN_TYPES = ()
    FUNCTION = "upload_image"
    
    OUTPUT_NODE = True    
    
    def upload_image(self, images, save_image, upload_imgur, webhook_url, filename_prefix="temp", prompt=None, extra_pnginfo=None):
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

                file = None
                results = None
                
                if save_image:
                    file = f'image_{str(time.time())}.png'
                    results = list()
                    results.append({
                        "filename": file,
                        "subfolder": subfolder,
                        "type": self.type
                    })
                else:
                    file = f"temp_file.png"
                
                img_path = os.path.join(full_output_folder, file)
                img.save(img_path, pnginfo=metadata, compress_level=self.compress_level)
        
        except Exception:
            ErrorHandler().handle_error("image", f"Error sending image to {webhook_url}.")
            return (None, )
        
        finally:
            if save_image:
                return { "ui": { "images": results }}
            else: os.remove(img_path); return (None,)
