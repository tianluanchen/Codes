const { genHTML } = require("./utils");
const { genPinURL, genStatCardURL, genTopLangsURL } = require("./gen-url");

/**
 * @description: 返回指定仓库的Markdown
 * @param {object} opt 配置项
 * @return {string}
 */
function genPinHTML(opt = {}) {
    const username = String(opt.username || "").trim();
    const repo = String(opt.repo || "").trim();
    const title = `${username}/${repo}`;
    // img标签设置
    const imgOpt = typeof opt.imgOpt == "object" ? opt.imgOpt : {};
    let link;
    if (!opt.link) {
        link = `https://github.com/${username}/${repo}`;
    } else {
        link = String(opt.link || "").trim();
    }
    // 移除其它配置
    const pureOpt = Object.assign({}, opt);
    pureOpt.imgOpt = undefined;
    pureOpt.link = undefined;
    const imgURL = genPinURL(pureOpt);
    return genHTML(imgURL, link, title, imgOpt);
}


/**
 * @description: 返回github 统计卡片的HTML
 * @param {object} opt 配置项
 * @return {string}
 */
function genStatCardHTML(opt = {}) {
    const username = String(opt.username || "").trim();
    const repo = String(opt.repo || "").trim();
    const imgURL = genStatCardURL(opt);
    const title = `${username}'s GitHub stats`;
    // img标签设置
    const imgOpt = typeof opt.imgOpt == "object" ? opt.imgOpt : {};
    const link = String(opt.link || "").trim();
    return genHTML(imgURL, link, title, imgOpt);
}

/**
 * @description: 返回热门使用语言的HTML
 * @param {object} opt 配置项
 * @return {string}
 */
function genTopLangsHTML(opt = {}) {
    const username = String(opt.username || "").trim();
    const link = String(opt.link || "").trim();
    const imgURL = genTopLangsURL(opt);
    const title = `${username}'s Top Langs`;
    // img标签设置
    const imgOpt = typeof opt.imgOpt == "object" ? opt.imgOpt : {};
    return genHTML(imgURL, link, title, imgOpt);
}

module.exports = {
    genPinHTML,
    genStatCardHTML,
    genTopLangsHTML
}