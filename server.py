import os
import pathlib

import server
web = server.web

## Gallery ##
gallery_files = os.path.join(pathlib.Path(__file__).parent.resolve(), "src", "web", "gallery")
gallery_enabled = True

## Setup Gallery ##
if gallery_enabled == True:
    @server.PromptServer.instance.routes.get("/gallery")
    async def get_gallery(request):
        response = web.FileResponse(os.path.join(gallery_files, "gallery.html"))
        response.headers['Cache-Control'] = 'no-cache'
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response