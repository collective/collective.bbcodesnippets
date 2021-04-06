import CodeSnippets from './CodeSnippets.svelte';


tinymce.create("tinymce.plugins.Collective.BBCodeSnippetsPlugin", {
    init: function (editor) {
      var portalUrl = $("body").attr("data-portal-url");
      var buttonIcon = portalUrl + "/++static++/bbcodeicon.png";
      editor.on("init", function () {
      });

      editor.addCommand("bbcodesnippets", function () {
        alert("Todo!");
      });

      editor.addButton("collective.bbcodesnippets-button", {
        cmd: "bbcodesnippets",
        image: buttonIcon,
      });
    },
});

tinymce.PluginManager.add(
  "collectivebbcodesnippets",
  tinymce.plugins.FhstpSnippetsPlugin
);
