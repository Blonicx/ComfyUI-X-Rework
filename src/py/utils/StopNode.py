import server

from ..Utils import AnyType

def stop_workflow():
    server.PromptServer.instance.send_sync("xrework.stop_workflow", {})
    
any = AnyType("*")
class StopNode:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "anything": (any, {}),
            },
            "optional": {
            }
        }

    CATEGORY = 'rework-x/utils'

    RETURN_TYPES = ()
    FUNCTION = "stop_workflow"

    OUTPUT_NODE = True

    def stop_workflow(self, anything):
        stop_workflow()
                
        return (None,)
