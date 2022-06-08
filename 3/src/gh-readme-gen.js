const {
    genPinHTML,
    genStatCardHTML,
    genTopLangsHTML
} = require("./gen-html");

const {
    quickGen
} = require("./quick-gen");

const {
    genPinMD,
    genStatCardMD,
    genTopLangsMD
} = require("./gen-md");

const {
    genPinURL,
    genStatCardURL,
    genTopLangsURL
} = require("./gen-url");

const {
    themes,
    layouts,
    setAPI,
    getAPI
} = require("./rule");

module.exports = {
    getAPI,
    setAPI,
    layouts,
    themes,
    genPinMD,
    genPinHTML,
    genPinURL,
    genStatCardMD,
    genStatCardHTML,
    genStatCardURL,
    genTopLangsMD,
    genTopLangsHTML,
    genTopLangsURL,
    quickGen
}