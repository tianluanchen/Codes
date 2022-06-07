const { setAPI, genStatCardMD, genTopLangsMD, genPinMD, genStatCardURL, genPinURL, genTopLangsURL } = require("./index");
// 测试

// 设置API 若自己未部署服务则不配置
// setAPI("your-api-domain");

const username = "your-username"; // 用户
const theme = "dark"; // 主题

// genStatCardURL等函数与下列用法一致，只不过只返回url

console.log(
    // 生成大的统计卡片markdown
    genStatCardMD({
        username: username,
        theme: theme,
        link: "xxx网址",//link 指定markdown图片点击跳转的网址
        show_icons: false,// 显示图表否
        //... 配置 与github-readme-stats配置相同
    }),
    "\n",
    // 生成热门语言使用的markdown
    genTopLangsMD({
        username: username,
        theme: "merko",
        hide: ["css", "html"] // 不显示的语言 可以填写数组或字符串
        // hide: "css,html"
        //... 配置 与github-readme-stats配置相同
    }),
    "\n",
    // 生成指定仓库的markdown
    genPinMD({
        username: username,
        theme: "gruvbox",
        repo: "your-repository", //你的仓库名
        link: "xxx网址",//link 指定markdown图片点击跳转的网址 此处不设置则默认你的仓库网址
        //... 配置 与github-readme-stats配置相同
    })
)