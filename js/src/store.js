import { writable } from "svelte/store";
import { list } from "./restapi.js";

const store = writable(new Map())


document.addEventListener("DOMContentLoaded", () => {
  list()
  .then(datalist => {
    store.update(storage => {
        storage.set('enabled', datalist)
        return storage
    })
  })
  .catch(err => {})
})