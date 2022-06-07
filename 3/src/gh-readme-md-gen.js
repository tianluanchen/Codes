
/**
 * @description: 接口域名
 */
var apiDomain = "github-readme-stats.vercel.app";

/**
 * @description: 设置api域名
 * @param {string} apiDomain
 * @return {void}
 */
function setAPI(api) {
    if (api) {
        apiDomain = String(api);
    }
}

/**
 * @description: 所有主题
 */
const themes = ["dark", "radical", "merko", "gruvbox", "tokyonight", "onedark", "cobalt", "synthwave", " highcontrast", "dracula"];

/**
 * @description: 热门使用语言布局
 */
const layouts = ["default", "compact"];



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
 * @description: 返回热门使用语言的imgurl
 * @param {object} opt 配置项
 * @return {string}
 */
function genPinURL({
    username = "",
    theme = "",
    show_owner = false,
    repo = "",
    // title_color - 卡片标题颜色 （十六进制色码）
    // text_color - 内容文本颜色 （十六进制色码）
    // icon_color - 图标颜色（如果可用）（十六进制色码）
    // bg_color - 卡片背景颜色 （十六进制色码） 或者 以 angle,start,end 的形式渐变
    // hide_border - 隐藏卡的边框 (布尔值)
    // theme - 主题名称，从所有可用主题中选择
    // cache_seconds - 手动设置缓存头 （最小值: 1800，最大值: 86400）
    // locale - 在卡片中设置语言 (例如 cn, de, es, 等等)
}) {
    let params = new URLSearchParams();
    const opt = [...arguments][0] || {};
    params = setParams(params, opt);
    params.set("username", String(username).trim());
    params.set("show_owner", Boolean(show_owner));
    params.set("repo", String(repo));
    theme = String(theme).trim().toLowerCase();
    themes.includes(theme) ? params.set("theme", theme) : params.delete("theme");
    return `https://${apiDomain}/api/pin/?${params.toString()}`;
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
 * @description: 返回热门使用语言的imgurl
 * @param {object} obj 配置项
 * @return {string}
 */
function genTopLangsURL({
    username = "",
    hide = [], //从卡片中隐藏指定语言
    hide_title = false, // 隐藏标题
    layout = "compact", // 布局 default 
    card_width = undefined, // 卡片宽度 number
    theme = "",
    // title_color - 卡片标题颜色 （十六进制色码）
    // text_color - 内容文本颜色 （十六进制色码）
    // icon_color - 图标颜色（如果可用）（十六进制色码）
    // bg_color - 卡片背景颜色 （十六进制色码） 或者 以 angle,start,end 的形式渐变
    // hide_border - 隐藏卡的边框 (布尔值)
    // theme - 主题名称，从所有可用主题中选择
    // cache_seconds - 手动设置缓存头 （最小值: 1800，最大值: 86400）
    // locale - 在卡片中设置语言 (例如 cn, de, es, 等等)
} = {}) {
    let params = new URLSearchParams();
    const opt = [...arguments][0] || {};
    params = setParams(params, opt);
    params.set("username", String(username).trim());
    params.set("hide_title", Boolean(hide_title));
    layout = String(layout).trim().toLowerCase();
    layouts.includes(layout) ? params.set("layout", layout) : params.delete("layout");
    if (layout) {
        params.set("layout", layout);
    }
    card_width = Number(card_width);
    if (!isNaN(card_width)) {
        params.set("card_width", card_width);
    }
    theme = String(theme).trim().toLowerCase();
    themes.includes(theme) ? params.set("theme", theme) : params.delete("theme");
    hide = typeof hide === "string" ? hide : (hide || []).map(e => encodeURIComponent(e)).join(",");
    if (hide) {
        params.set("hide", hide);
    }
    return `https://${apiDomain}/api/top-langs/?${params.toString()}`;
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


/**
 * @description: 返回github 统计卡片的imgurl
 * @param {object} obj 配置项
 * @return {string}
 */
function genStatCardURL({
    username = "", // 登录github的用户名
    theme = "", // 主题
    count_private = false, // 是否加入私人项目贡献
    show_icons = true,
    hide = [],
    link = "",
    // title_color - 卡片标题颜色 （十六进制色码）
    // text_color - 内容文本颜色 （十六进制色码）
    // icon_color - 图标颜色（如果可用）（十六进制色码）
    // bg_color - 卡片背景颜色 （十六进制色码） 或者 以 angle,start,end 的形式渐变
    // hide_border - 隐藏卡的边框 (布尔值)
    // theme - 主题名称，从所有可用主题中选择
    // cache_seconds - 手动设置缓存头 （最小值: 1800，最大值: 86400）
    // locale - 在卡片中设置语言 (例如 cn, de, es, 等等)

    // 专属
    // hide - 隐藏特定统计信息 (以逗号分隔)
    // hide_title - (boolean)
    // hide_rank - (boolean)
    // show_icons - (boolean)
    // include_all_commits - 统计总提交次数而不是仅统计今年的提交次数 (boolean)
    // count_private - 统计私人提交 (boolean)
    // line_height - 设置文本之间的行高 (number)

} = {},) {
    let params = new URLSearchParams();
    const opt = [...arguments][0] || {};
    params = setParams(params, opt);
    params.set("username", String(username).trim());
    theme = String(theme).trim().toLowerCase();
    themes.includes(theme) ? params.set("theme", theme) : params.delete("theme");
    params.set("count_private", Boolean(count_private));
    params.set("show_icons", Boolean(show_icons));
    hide = typeof hide === "string" ? hide : (hide || []).join(",");
    if (hide) {
        params.set("hide", hide);
    }
    return `https://${apiDomain}/api?${params.toString()}`;
}

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
 * @description: 设置参数
 * @param {URLSearchParams} params
 * @param {object} opt
 * @return {URLSearchParams}
 */
function setParams(params, opt) {
    Reflect.ownKeys(opt).forEach((key) => {
        if (key === "link" || opt[key] == undefined || opt[key] == null) {
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

//quick generate
function quickGen() {
    if (typeof window === undefined) {
        return;
    }
    if (location.hostname !== "github.com" || location.pathname.indexOf("/") !== 0) {
        alert("当前页面不是你的GitHub主页，无法生成MarkDown");
        return;
    }
    const theme = prompt(`请输入生成主题，选项为：${themes.join(",")}`, "");
    const username = document.querySelector("span.p-nickname")?.textContent.trim();
    let opt = { theme, username };
    const repos = [...document.querySelectorAll("span.repo")].map(e => {
        return e.textContent.trim();
    });
    let md = `<!-- GitHub 统计卡片 -->\n\n${genStatCardMD(opt)}\n\n<!-- GitHub 热门使用语言卡片 -->\n\n${genTopLangsMD(opt)}\n\n<!-- GitHub 置顶仓库卡片 -->\n\n${repos.map(e => (opt.repo = e, genPinMD(opt))).join("\n\n")}\n`;
    const container = document.createElement("div");
    container.setAttribute("style", "max-height:85vh;border-radius:5px;background:rgba(0,0,0,.4);padding:20px;position:fixed;width:500px;max-width:85vw;z-index:999;inset:0;margin:auto;display:flex;flex-flow:wrap column;justify-content:space-around")
    container.innerHTML = `<textarea style=width:100%;height:360px;font-size:18px;padding:12px;color:#efefef;background:#2b2a33></textarea><div style=text-align:center;width:100%><button style=padding:12px;min-width:90px;height:60px;font-size:18px;color:#efefef;background:#2b2a33>关闭</button></div>`;
    container.querySelector('textarea').value = md;
    container.querySelector('button').onclick = () => {
        container.remove();
    };
    document.documentElement.appendChild(container);
}

module.exports = {
    apiDomain,
    layouts,
    themes,
    setParams,
    setAPI,
    genMarkdown,
    genPinMD,
    genPinURL,
    genStatCardMD,
    genStatCardURL,
    genTopLangsMD,
    genTopLangsURL,
    quickGen
}

