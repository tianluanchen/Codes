const { themes, layouts, getAPI } = require("./rule");
const { setParams } = require("./utils");

/**
 * @description: 返回热门使用语言的imgurl
 * @param {object} obj 配置项
 * @return {string}
 */
function genTopLangsURL({
    username = "",
    hide = [], //从卡片中隐藏指定语言
    hide_title = undefined, //bool 隐藏标题
    layout = "compact", // 布局 default 
    card_width = undefined, // 卡片宽度 number
    theme = undefined,
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
    return `https://${getAPI()}/api/top-langs/?${params.toString()}`;
}

/**
 * @description: 返回github 统计卡片的imgurl
 * @param {object} obj 配置项
 * @return {string}
 */
function genStatCardURL({
    username = "", // 登录github的用户名
    theme = undefined, // 主题
    count_private = undefined, //bool 是否加入私人项目贡献
    show_icons = true, //bool icon
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
    return `https://${getAPI()}/api?${params.toString()}`;
}

/**
 * @description: 返回热门使用语言的imgurl
 * @param {object} opt 配置项
 * @return {string}
 */
function genPinURL({
    username = "",
    theme = "",
    show_owner = undefined, // bool 显示作者
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
    return `https://${getAPI()}/api/pin/?${params.toString()}`;
}

module.exports = {
    genPinURL,
    genStatCardURL,
    genTopLangsURL
}