<?php
/*
 * @Author       :  Ayouth
 * @Date         :  2021-10-03 GMT+0800
 * @LastEditTime :  2022-06-24 GMT+0800
 * @FilePath     :  rainyun.php
 * @Description  :  日志审阅
 * Copyright (c) 2022 by Ayouth, All Rights Reserved. 
 */

// 若有bug 隐藏错误
error_reporting(E_ERROR);
ini_set("display_errors", "Off");

//自定义网页标题和大标题
$title = "雨云签到日志";
//文件路径，推荐绝对路径
$file = "./rainyun-signin-log.csv";
//设置审阅令牌
$token = "123";
// session名
$session_name  = 'rainyun_signin_log_token';

$verified = false;
// 开启会话
session_start([
    "cookie_httponly" => true,
    "cookie_samesite" => "Strict"
]);

// 作为反馈
$script = '';

// 判断是否提交了验证请求
if (isset($_POST['token'])) {
    if ($_POST['token'] == $token) {
        $script .= '<script>alert("验证成功");</script>';
        $_SESSION[$session_name] = 'verified';
    } else {
        $script .= '<script>alert("验证失败");</script>';
    }
}


// 判断当前是否是验证状态
if (isset($_SESSION[$session_name]) && $_SESSION[$session_name] == 'verified') {
    $verified = true;
    // 处理用户请求
    handle_user_req();
}

// 处理用户请求
function handle_user_req()
{
    global $script;
    global $file;
    // 登出
    if (isset($_GET['logout'])) {
        session_destroy();
        header('Location:' . $_SERVER['PHP_SELF']);
        exit(0);
    }
    // 删除
    if (isset($_POST['delete'])) {
        deleteFile($file);
        $script .= '<script>alert("删除成功");</script>';
    }
}

// 读取并渲染表单
function renderTable()
{
    global $file, $script;
    if (!is_file($file)) {
        $script .= '<script>alert("日志文件不存在");</script>';
        return '';
    }
    $tb = "";
    $num = -1;
    $f = fopen($file, 'r');
    while ($line = fgetcsv($f)) {
        if (count($line) == 3) {
            $num += 1;
        }
        if ($num < 1) {
            continue;
        }
        $tr = '';
        $class = '';
        foreach ($line as $key => $value) {
            if ($key == 2) {
                if ($value == 'False') {
                    $class = 'class="wrong"';
                    $value = '失败';
                } else {
                    $value = '成功';
                }
            }
            $tr .= '<td>' . htmlentities($value) . '</td>';
        }
        $tb .= '<tr ' . $class . ' ><td>' . $num . '</td>' . $tr . '</tr>';
    }
    fclose($f);
    return $tb;
}

// 删除文件
function deleteFile(string $file)
{
    $f = fopen($file, "w");
    fwrite($f, 'date,user,status' . PHP_EOL);
    fclose($f);
}

?>
<!DOCTYPE html>
<html lang="zh">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php print($title); ?></title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            letter-spacing: 1px;
            font-family: Tahoma, Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        }

        button,
        textarea,
        input,
        iframe {
            -webkit-appearance: none;
            border: none;
            outline: none;
        }

        body {
            -webkit-tap-highlight-color: transparent;
            font-size: 16px;
            min-height: 100vh;
            background-color: rgb(56, 62, 95);
            position: relative;
            color: rgb(56, 56, 56);
        }

        input,
        button {
            font-size: 19px;
            height: 50px;
            min-width: 90px;
            border-radius: 4px;
            transition: 0.25s;
        }

        button:focus {
            box-shadow: 0 0 0 5px var(--bscolor, rgba(255, 255, 255, 0.6));
        }

        input:focus {
            box-shadow: 0 0 0 5px #8bacfe;
        }

        button {
            color: #fefefe;
            background-color: var(--bgcolor, #4c73d2);
            cursor: pointer;
            padding: 0 12px;
        }

        <?php if ($verified == false) { ?>.verify {
            margin: auto;
            position: absolute;
            left: 0;
            right: 0;
            top: 0;
            bottom: 0;
            padding: 10px;
            height: fit-content;
            width: fit-content;
        }

        #token {
            width: 250px;
            padding: 10px 15px;
            margin-right: 9px;
        }

        <?php } else { ?>#title {
            margin: auto;
            padding: 60px 0 30px;
            text-align: center;
            font-size: 27px;
            cursor: pointer;
            color: #fefefe;
        }

        table {
            min-width: 56vw;
            width: fit-content;
            max-width: 88vw;
            margin: auto;
            border-collapse: collapse;
            letter-spacing: 1px;
            font-size: 18px;
            background-color: #efefef;
            border-radius: 6px;
            box-shadow: 0 0 8px 0 rgba(255, 255, 255, 0.3);
            color: #363636;
            background-color: rgba(235, 235, 235);
            overflow: hidden;
        }

        th,
        td {
            padding: 10px 12px;
        }

        th {
            text-align: left;
        }

        tbody>tr:nth-child(2n+1) {
            background-color: rgba(219, 219, 219, 0.84);
        }

        tbody>tr:hover {
            background-color: rgba(209, 209, 209, 0.85);
        }

        th:nth-child(1),
        td:nth-child(1) {
            text-align: center;
            font-weight: bold;
        }

        tr.wrong {
            background-color: #deafaf !important;
        }

        .control {
            width: 55vw;
            min-width: 300px;
            margin: auto;
            padding: 36px 0;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-evenly;
        }

        .control>button {
            margin: 20px;
        }

        #delete {
            --bgcolor: #d23c3c;
        }

        #refresh {
            --bgcolor: #339848;
        }

        #logout {
            --bgcolor: gray;
        }

        <?php } ?>
    </style>
</head>

<body>
    <?php if ($verified == false) { ?>
        <div class="verify">
            <form action="" method="POST">
                <input name="token" placeholder="请输入token验证" required type="password" id="token">
                <button type="submit">验证</button>
            </form>
        </div>
    <?php } else { ?>
        <h1 id="title" onclick="document.querySelector('.control').scrollIntoView()" title="点击定位至底部"><?php print($title); ?></h1>
        <table>
            <thead>
                <tr>
                    <th>序号</th>
                    <th>日期</th>
                    <th>用户</th>
                    <th>签到结果</th>
                </tr>
            </thead>
            <tbody>
                <?php print(renderTable()); ?>
                <script>
                    let trArr = [...document.querySelectorAll("tbody tr")];
                    let df = document.createDocumentFragment();
                    while (trArr.length > 0) {
                        df.appendChild(trArr.pop());
                    }
                    document.querySelector("tbody").appendChild(df);
                </script>
            </tbody>
        </table>
        <div class="control">
            <button onclick="del()" id="delete">删除</button>
            <button id="refresh" onclick="(location.href =location.href)">刷新</button>
            <button id="backtop" onclick="document.querySelector('#title').scrollIntoView()">回到顶部</button>
            <button id="logout" onclick="(location.href = location.pathname+'?logout=true')">登出</button>
        </div>
        <form id="del" action="" method="POST" style="display: none;">
            <input type="text" name="delete" value="true">
        </form>
        <script>
            function del() {
                let r = confirm('是否确认删除所有日志？');
                if (!r) {
                    return;
                }
                document.querySelector('#del').submit();
            }
        </script>
    <?php } ?>
    <?php print($script); ?>
</body>

</html>