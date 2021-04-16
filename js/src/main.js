import { list } from "./restapi.js";

require(["tinymce"], function (tinymce) {
  console.log("create and add collectivebbcodesnippets")

  tinymce.PluginManager.add('collectivebbcodesnippets', function(editor, url) {

    console.log(editor)
    console.log(url)
    const portalUrl = $("body").attr("data-portal-url")
    const buttonIcon = portalUrl + "/++plone++collective.bbcodesnippets/bbcodeicon.png"
    list()
    .then((datalist) => {
      console.log(datalist)
      datalist.forEach( (entry, index) => {
        const name = 'bbcs_' + entry.name
        console.log(entry.name)
        editor.addMenuItem(name, {
          text: entry.name,
          onAction: () => {
            alert(entry.snippet)
          }
        })
      })
    })
    .catch( (err) => {
      console.log(err)
    })

    /* Return the metadata for the help plugin */
    return {
      getMetadata: function () {
        return  {
          name: 'collective.bbcodesnippets plugin',
          url: 'https://github.com/collective/collective.bbcodesnippets'
        };
      }
    };
  });
  

  // tinymce.PluginManager.add("collectivebbcodesnippets", (editor, url) => {
  //   console.log(editor)
  //   console.log(url)
  //   const portalUrl = $("body").attr("data-portal-url")
  //   const buttonIcon = portalUrl + "/++plone++collective.bbcodesnippets/bbcodeicon.png"
  //   list()
  //   .then((datalist) => {
  //     console.log(datalist)
  //     datalist.forEach( (entry, index) => {
  //       const name = 'bbcs_' + entry.name
  //       console.log(entry.name)
  //       editor.ui.registry.addMenuItem(name, {
  //         text: entry.name,
  //         onAction: () => {
  //           alert(entry.snippet)
  //         }
  //       })
  //     })
  //   })
  //   .catch( (err) => {
  //     console.log(err)
  //   })
  //   return {
  //     init: (editor) => {
  //       console.log("init collectivebbcodesnippets")
  //     },
  //     getMetadata: function () {
  //       return  {
  //         name: 'https://github.com/collective/collective.bbcodesnippets',
  //         url: 'https://github.com/collective/collective.bbcodesnippets'
  //       };
  //     }      
  //   }
  // })

})()
