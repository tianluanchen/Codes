const { genMarkdown } = require("./utils");
const { genPinURL, genStatCardURL, genTopLangsURL } = require("./gen-url");

/**
 * @description: 返回指定仓库的Markdown
 * @param {object} opt 配置项
 * @return {string}
 */
function genPinMD(opt = {}) {
    const username = String(opt.username || "").trim();
    const repo = String(opt.repo || "").trim();
    const imgURL = genPinURL(opt);
    const title = `${username}/${repo}`;
    let link;
    if (!opt.link) {
        link = `https://github.com/${username}/${repo}`;
    } else {
        link = String(opt.link || "").trim();
    }
    return genMarkdown(imgURL, link, title);
}

/**
 * @description: 返回热门使用语言的MarkDown
 * @param {object} opt 配置项
 * @return {string}
 */
function genTopLangsMD(opt = {}) {
    const username = String(opt.username || "").trim();
    const link = String(opt.link || "").trim();
    const imgURL = genTopLangsURL(opt);
    const title = `${username}'s Top Langs`;
    return genMarkdown(imgURL, link, title);
}

/**
 * @description: 返回github 统计卡片的Markdown
 * @param {object} opt 配置项
 * @return {string}
 */
function genStatCardMD(opt = {}) {
    const username = String(opt.username || "").trim();
    const link = String(opt.link || "").trim();
    const imgURL = genStatCardURL(opt);
    const title = `${username}'s GitHub stats`;
    return genMarkdown(imgURL, link, title);
}

module.exports = {
    genPinMD,
    genStatCardMD,
    genTopLangsMD
}