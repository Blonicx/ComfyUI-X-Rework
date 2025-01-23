import requests
import folder_paths
import pathlib
import os
import json
import time
import numpy as np

from dotenv import load_dotenv
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args

from ..ErrorHandler import ErrorHandler

dotnev_path = os.path.join(pathlib.Path(__file__).parent.parent.parent.parent.resolve(), ".env")

load_dotenv(dotenv_path=dotnev_path)

webhook_url=os.getenv('DISCORD_WEBHOOK')

def upload_img_discord(img_path):
    if webhook_url != "":
        pass
    else: ErrorHandler().handle_error("image", f"Error sending image to {webhook_url}.")
    
    file = open(img_path, 'rb')

    files = {
        'media': file
    }

    requests.post(webhook_url, files=files)
    
    file.close()

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
                "images": ("IMAGE", {"tooltip": "The images to upload."}),
                "save_image": ("BOOLEAN", {"default": True}),
                "upload_discord": ("BOOLEAN", {"default": False}),
            },
            "optional": {
            }
        }
    
    CATEGORY = 'x-rework/image'
    
    RETURN_TYPES = ()
    FUNCTION = "upload_image"
    
    OUTPUT_NODE = True    
    
    def upload_image(self, images, save_image, upload_discord, filename_prefix="xrework", prompt=None, extra_pnginfo=None):
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

                if upload_discord == True:
                    upload_img_discord(img_path)
        
        finally:
            if save_image:
                return { "ui": { "images": results }}
            else: os.remove(img_path); return (None,)
