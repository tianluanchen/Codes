/**
 * @description: 生成markdown语法的图片标签
 * @param {string} imgURL 图片地址
 * @param {string} link 点击跳转的链接
 * @param {string} title alt 文本
 * @return {string} 
 */
function genMarkdown(imgURL = "", link = "", title = "GitHub Stat Img") {
    if (!link) {
        link = imgURL;
    }
    return `[![${title}](${imgURL})](${link})`;
}

/**
 * @description: 生成HTML的图片标签
 * @param {string} imgURL 图片地址
 * @param {string} link 点击跳转的链接
 * @param {string} title alt 文本
 * @param {object} imgOpt img标签属性的配置
 * @return {string} 
 */
function genHTML(imgURL = "", link = "", title = "GitHub Stat Img", imgOpt = {}) {
    if (!link) {
        link = imgURL;
    }
    return `<a href="${link}">\n\t<img ${Reflect.ownKeys(imgOpt).map(key => `${key}="${imgOpt[key]}"`).join(" ")} alt="${title}" src="${imgURL}" />\n</a>`;
}

/**
 * @description: 设置参数
 * @param {URLSearchParams} params
 * @param {object} opt
 * @return {URLSearchParams}
 */
function setParams(params, opt) {
    Reflect.ownKeys(opt).forEach((key) => {
        if (opt[key] == undefined || opt[key] == null) {
            return;
        }
        if (typeof opt[key] != "string" && opt[key].length != undefined) {
            opt[key] = opt[key].join(",").trim();
        } else {
            opt[key] = String(opt[key]).trim();
        }
        params.set(key, opt[key]);
    });
    return params;
}


module.exports = {
    genHTML,
    genMarkdown,
    setParams
}