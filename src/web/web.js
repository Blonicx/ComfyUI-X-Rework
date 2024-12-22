import { app } from "../../scripts/app.js";

function make_submenu(value, options, e, menu, node) {
    const submenu = new LiteGraph.ContextMenu(
        ["⭐Visit on Github⭐", "❤️Donate on Ko-Fi❤️",],
        { 
            event: e, 
            callback: function (v) { 
                if(v == "⭐Visit on Github⭐"){
                    window.open("https://github.com/Blonicx/ComfyUI-X-Rework");
                }
                else if(v == "❤️Donate on Ko-Fi❤️"){
                    window.open("https://ko-fi.com/blonicx");
                }
                else{
                    alert("Not Implemented yet.")
                }
            }, 
            parentMenu: menu, 
            node:node
        }
    )
}

app.registerExtension({ 
	name: "com.blonicx.comfyui-x-rework",
	async setup() {
        const original_getCanvasMenuOptions = LGraphCanvas.prototype.getCanvasMenuOptions;
        LGraphCanvas.prototype.getCanvasMenuOptions = function () {
            const options = original_getCanvasMenuOptions.apply(this, arguments);
            options.push(null);
            options.push({
                content: "X-Rework",
                has_submenu: true,
                callback: make_submenu,
            })
            return options;
        }
	},
})