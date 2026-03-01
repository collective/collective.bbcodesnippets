(function () {
  'use strict';

  const replace = (editor, template) => {
    const content = editor.selection.getContent({ format: "text" });
    let replaced = template.replace("$TEXT", content);
    replaced = replaced.replace("$CURSOR", "");
    editor.selection.setContent(replaced);
  };

  tinymce.PluginManager.add("collectivebbcodesnippets", (editor) => {
    const portalUrl = document.body.dataset.portalUrl;

    // Eagerly fetch snippets and register menu items for the menubar.
    // Item names must match those configured in tinymce.py (bbcs{name}).
    fetch(`${portalUrl}/@bbcodesnippets_enabled`, {
      headers: { Accept: "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
        data.forEach((entry) => {
          editor.ui.registry.addMenuItem(`bbcs${entry.name}`, {
            text: `${entry.name} (${entry.snippet})`,
            onAction: () => replace(editor, entry.template),
          });
        });
      })
      .catch((err) => {
        console.error("BBCode Snippets: Failed to load snippets", err);
      });
  });

})();
//# sourceMappingURL=collective.bbcodesnippets.js.map
