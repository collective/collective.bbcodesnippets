(function () {
  'use strict';

  // keep import for unknown reason, otherwise:

  const replace = (selection, template) => {
    const content = selection.getContent({format: 'text'});
    let replaced = template.replace("$TEXT", content);
    let position = replaced.indexOf("$CURSOR");
    replaced = replaced.replace("$CURSOR", "");
    selection.setContent(replaced);
    // if (position >= 0) {
    //   selection.setCursorLocation(selection, position)
    // }
  };

  require(["tinymce"], function (tinymce) {
    console.log("create and add collectivebbcodesnippets");
    const portalUrl = document.body.dataset["portalUrl"];
    const bbcodesnippet_enabled_url = portalUrl + "/@bbcodesnippets_enabled";
    fetch(
      bbcodesnippet_enabled_url, 
      {
        headers: {'Accept': 'application/json'}
      }
    )
    .then(response => response.json())
    .then(data => {
      tinymce.create("tinymce.plugins.CollectiveBBCodeSnippetsPlugin", {
        init: editor => {
          editor.on("init", function () {
            console.log("editor on init!");
          });
          // Adds a menu item to the tools menu
          data.forEach( (entry, index) => {
            const identifier = 'bbcs' + entry.name;
            console.log(index + " " + identifier);
            editor.addMenuItem(identifier, {
              text: entry.name + " (" + entry.snippet + ")",
              context: "bbcs",
              onClick: () => {
                replace(editor.selection, entry.template);
              }
            });
          });
        }
      });
      tinymce.PluginManager.add(
        "collectivebbcodesnippets",
        tinymce.plugins.CollectiveBBCodeSnippetsPlugin
      );
    })
    .catch(err => {
      console.log(err);
    });   
  })();

}());
//# sourceMappingURL=collective.bbcodesnippets.js.map
