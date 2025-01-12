import comfy
import torch
import random
import latent_preview

def x_sampler(model, clip, vae, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent, denoise=1.0, disable_noise=False, start_step=None, last_step=None, force_full_denoise=False):
    ## get latent image ##
    latent_image = latent["samples"]
    latent_image = comfy.sample.fix_empty_latent_channels(model, latent_image)

    if disable_noise:
        noise = torch.zeros(latent_image.size(), dtype=latent_image.dtype, layout=latent_image.layout, device="cpu")
    else:
        batch_inds = latent["batch_index"] if "batch_index" in latent else None
        noise = comfy.sample.prepare_noise(latent_image, seed, batch_inds)

    noise_mask = None
    if "noise_mask" in latent:
        noise_mask = latent["noise_mask"]

    ## conditioning ##
    tokens1 = clip.tokenize(positive)
    output1 = clip.encode_from_tokens(tokens1, return_pooled=True, return_dict=True)
    cond1 = output1.pop("cond")
    ext_cond1 = [[cond1, output1]]    
    
    tokens2 = clip.tokenize(negative)
    output2 = clip.encode_from_tokens(tokens2, return_pooled=True, return_dict=True)
    cond2 = output2.pop("cond")
    ext_cond2 = [[cond2, output2]]

    ## sampling ##
    callback = latent_preview.prepare_callback(model, steps)
    disable_pbar = not comfy.utils.PROGRESS_BAR_ENABLED
    samples = comfy.sample.sample(model, noise, steps, cfg, sampler_name, scheduler, ext_cond1, ext_cond2, latent_image,
                                  denoise=denoise, disable_noise=disable_noise, start_step=start_step, last_step=last_step,
                                  force_full_denoise=force_full_denoise, noise_mask=noise_mask, callback=callback, disable_pbar=disable_pbar, seed=seed)
    out = latent.copy()
    out["samples"] = samples
    
    images = vae.decode(out["samples"])
    if len(images.shape) == 5: #Combine batches
        images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])
    return (images, )

class XSampler:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL", {"tooltip": "The model used for denoising the input latent."}),
                "clip": ("CLIP", {"tooltip": "The clip used for denoising the input latent."}),
                "vae": ("VAE", {"tooltip": "The VAE used for denoising the input latent."}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "tooltip": "The random seed used for creating the noise."}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 10000, "tooltip": "The number of steps used in the denoising process."}),
                "cfg": ("FLOAT", {"default": 8.0, "min": 0.0, "max": 100.0, "step":0.1, "round": 0.01, "tooltip": "The Classifier-Free Guidance scale balances creativity and adherence to the prompt. Higher values result in images more closely matching the prompt however too high values will negatively impact quality."}),
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"tooltip": "The algorithm used when sampling, this can affect the quality, speed, and style of the generated output."}),
                "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"tooltip": "The scheduler controls how noise is gradually removed to form the image."}),
                "positive": ("STRING", {"tooltip": "The conditioning describing the attributes you want to include in the image."}),
                "negative": ("STRING", {"tooltip": "The conditioning describing the attributes you want to exclude from the image."}),
                "latent_image": ("LATENT", {"tooltip": "The latent image to denoise."}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    OUTPUT_TOOLTIPS = ("The generated image.",)
    FUNCTION = "sample"

    CATEGORY = 'x-rework/sampler'

    def sample(self, model, vae, clip, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=1.0):
        return x_sampler(model, clip, vae, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise=denoise)