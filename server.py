import os
import pathlib

import server
web = server.web

## Files ##
mainpage_files = os.path.join(pathlib.Path(__file__).parent.resolve(), "src", "web", "index_website")

## Main Page ##
@server.PromptServer.instance.routes.get("/xrework")
async def get_gallery(request):
    response = web.FileResponse(os.path.join(mainpage_files, "index.html"))
    response.headers['Cache-Control'] = 'no-cache'
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response