import { list } from "./restapi.js";

require(["tinymce"], function (tinymce) {
  console.log("create and add collectivebbcodesnippets")

  const portalUrl = document.body.dataset["portalUrl"]

  tinymce.create("tinymce.plugins.CollectiveBBCodeSnippetsPlugin", {
    init: function (editor) {
      editor.on("init", function () {
        console.log("editor on init!")
      })

      // Adds a menu item to the tools menu
      editor.addMenuItem("example", {
        text: "Example plugin",
        context: "tools",
        onclick: function () {
          // Open window with a specific url
          editor.windowManager.open({
            title: "TinyMCE site",
            url: "https://www.tinymce.com",
            width: 800,
            height: 600,
            buttons: [
              {
                text: "Close",
                onclick: "close",
              },
            ],
          })
        },
      })
    },
  })
  tinymce.PluginManager.add(
    "collectivebbcodesnippets",
    tinymce.plugins.CollectiveBBCodeSnippetsPlugin
  )
})()
