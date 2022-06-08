/**
 * @description: 闭包生成api操作函数 
 * @return {array}
 */
function createAPI() {
    let apiDomain = "github-readme-stats.vercel.app";
    return [
        () => {
            return apiDomain;
        },
        (api) => {
            if (typeof api === "string") {
                apiDomain = api;
            }
        }
    ]
}
/**
 * @description: api操作函数
 */
const [getAPI, setAPI] = createAPI();

/**
 * @description: 所有主题
 */
const themes = ["dark", "radical", "merko", "gruvbox", "tokyonight", "onedark", "cobalt", "synthwave", " highcontrast", "dracula"];

/**
 * @description: 热门使用语言布局
 */
const layouts = ["default", "compact"];

module.exports = {
    themes,
    layouts,
    setAPI,
    getAPI
}