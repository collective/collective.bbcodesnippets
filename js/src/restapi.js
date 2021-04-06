// Api.js
import axios from "axios";

let api_url
let axiosAPI

const bbcodesnippet_enabled_surl = "@bbcodesnippets_enabled"

function fetch_ploneinfo() {
    api_url = document.getElementsByTagName('body')[0].dataset["portalUrl"]
    axiosAPI = axios.create({
        baseURL : api_url,
        headers: {'Accept': 'application/json'}
    });
}

if (document.readyState !== 'loading') {
    fetch_ploneinfo()
} else {
    document.addEventListener("DOMContentLoaded", fetch_ploneinfo)
}

// implement a method to execute all the request from here.
const apiRequest = (method, url, request, headers) => {
    // using the axios instance to perform the request that received from each http method
    let requestdata = {
        method: method,
        url: url,
        headers: headers
    }
    if (method == 'get') {
        requestdata.params = request
    } else {
        requestdata.data = request
    }
    return axiosAPI(requestdata).then(res => {
        return Promise.resolve(res.data);
      })
      .catch(err => {
          if (error.response.status != 404) {
            console.error(err)
          }
        return Promise.reject(err)
      });
};

// function to execute the http get request
const get = (url, request) => apiRequest("get", url, request);

// list enabled bbcodesnippets
export const list = () => get(bbcodesnippetsurl).catch(err => {})
