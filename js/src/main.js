require(["jquery", "pat-registry", "tinymce"], function ($, Registry, tinymce) {
  "use strict";
  console.log("works 1");
  var portalUrl = $("body").attr("data-portal-url");
  const buttonIcon =
    portalUrl + "/++plone++collective.bbcodesnippets/bbcodeicon.png";
  console.log("create and add collectivebbcodesnippets");
  var tinymce = require("tinymce");
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
    },
  });
  tinymce.PluginManager.add(
    "collectivebbcodesnippets",
    tinymce.plugins.CollectiveBBCodeSnippetsPlugin
  );
});
