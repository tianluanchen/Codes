const { themes } = require("./rule");
const { genPinHTML } = require("./gen-html");
const { genStatCardMD, genTopLangsMD, genPinMD } = require("./gen-md");


/**
 * @description: 将此代码在github个人主页上运行，快速生成readme
 * @return {void}
 */
function quickGen() {
    if (typeof window === undefined) {
        return;
    }
    if (location.hostname !== "github.com" || location.pathname.indexOf("/") !== 0) {
        alert("当前页面不是你的GitHub主页，无法生成MarkDown");
        return;
    }
    const theme = prompt(`请输入生成主题，选项为：${themes.join(" ,  ")}`, "").trim().replace(",", "");
    const isAlign = confirm("置顶仓库是否一行二列放置？");
    let isBigGap = false;
    if (isAlign) {
        isBigGap = confirm("是否使仓库之间具有较大的间隔？");
    }
    const username = document.querySelector("span.p-nickname")?.textContent.trim();
    let hide = prompt("热门使用语言中不显示的语言，逗号分割，如：less,html", "");
    hide = hide.split(",");
    hide = hide.length > 0 ? hide : undefined;
    let opt = { theme, username };
    let repos = [...document.querySelectorAll("span.repo")].map(e => {
        return e.textContent.trim();
    });
    let order = prompt(`自定义排列，填写序号，逗号分割，如：3,2,1\n${repos.map((e, i) => `${e} :  ${i}`).join("\n")}`, "");
    order = order.trim().replace("，", ",");
    if (order) {
        order = order.split(",").map(e => Number(e.trim())).filter((e) => {
            if (!isNaN(e) && e >= 0 && e <= 5) {
                return true;
            } else {
                return false;
            }
        });
        repos = repos.filter((e, i) => order.includes(i)).sort((a, b) => order.indexOf(repos.indexOf(a)) < order.indexOf(repos.indexOf(b)) ? -1 : 1);
    }
    let reposMD = "";
    const bigGapOpt = Object.assign({ imgOpt: { align: "left" } }, opt);
    if (isAlign) {
        repos.forEach((repo, i) => {
            opt.repo = repo;
            if (isBigGap) {
                bigGapOpt.repo = repo;
                reposMD += genPinHTML(i % 2 == 0 ? bigGapOpt : opt);
                if (i % 2 === 1 && i !== repos.length - 1) {
                    reposMD += "\n\n<br/><br/>\n\n";
                } else {
                    reposMD += "\n\n";
                }
            } else {
                reposMD += genPinHTML(opt);
                reposMD += "\n\n";
            }
        })
    } else {
        reposMD = `${repos.map(e => (opt.repo = e, genPinMD(opt))).join("\n\n")}\n`;
    }
    let md = `<!-- GitHub 统计卡片 -->\n\n${genStatCardMD(opt)}\n\n<!-- GitHub 热门使用语言卡片 -->\n\n${(opt.hide = hide, genTopLangsMD(opt))}\n\n<!-- GitHub 置顶仓库卡片 -->\n\n${reposMD}`;
    const container = document.createElement("div");
    container.setAttribute("style", "max-height:85vh;border-radius:5px;background:rgba(0,0,0,.4);padding:20px;position:fixed;width:500px;max-width:85vw;z-index:999;inset:0;margin:auto;display:flex;flex-flow:wrap column;justify-content:space-around")
    container.innerHTML = `<textarea style=width:100%;height:360px;font-size:18px;padding:12px;color:#efefef;background:#2b2a33></textarea><div style=text-align:center;width:100%><button style=margin-right:30px;padding:12px;min-width:90px;height:60px;font-size:18px;color:#efefef;background:#2b2a33>复制</button><button style=padding:12px;min-width:90px;height:60px;font-size:18px;color:#efefef;background:#2b2a33>关闭</button></div>`;
    const textarea = container.querySelector('textarea');
    textarea.value = md;
    container.querySelector('button:last-child').onclick = () => {
        container.remove();
    };
    container.querySelector('button:first-child').onclick = () => {
        textarea.focus();
        textarea.select();
        document.execCommand("copy");
    };
    document.documentElement.appendChild(container);

}

module.exports = {
    quickGen
}