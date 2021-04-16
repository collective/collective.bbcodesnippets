require(["jquery", "pat-registry", "tinymce"], function ($, Registry, tinymce) {
  "use strict";
  console.log("works 1");
  var portalUrl = $("body").attr("data-portal-url");
  const buttonIcon =
    portalUrl + "/++plone++collective.bbcodesnippets/bbcodeicon.png";
  console.log("create and add collectivebbcodesnippets");

  tinymce.create("tinymce.plugins.CollectiveBBCodeSnippetsPlugin", {
    init: function (editor) {
      editor.on("init", function () {
        // make all existing not editable
        $('[data-type="snippet_tag"]', editor.getBody()).each(function () {
          this.setAttribute("contenteditable", false);
        });
      });

      editor.addCommand("collectivebbcodesnippets", function () {
        var $el = $(editor.selection.getNode());
        console.log("works!");
      });

      editor.addButton("cbbcodesnippetsbutton", {
        cmd: "collectivebbcodesnippets",
        image: buttonIcon,
      });

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
          });
        },
      });
    },
  });
  tinymce.PluginManager.add(
    "collectivebbcodesnippets",
    tinymce.plugins.CollectiveBBCodeSnippetsPlugin
  );
});
