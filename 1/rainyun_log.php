<?php
//自定义网页标题
$html_title = "log";
//文件路径，推荐绝对路径
//例
$file_path = "log.csv";
//设置验证码
$token = "1234";


$table = "";
$demo = new LogPanel($file_path, $token);
$table = $demo->content;

# 日志类
class LogPanel
{
    var $FILE_PATH;
    var $TOKEN = "";
    var $content = "";
    function __construct($file_path, $token)
    {
        $this->FILE_PATH = $file_path;
        $this->TOKEN = $token;
        //执行
        $this->process();
    }
    function process()
    {
        session_start();
        $this->init_file();
        if ($_POST['del'] == "true") {
            if ($_SESSION["admin"] == true) {
                $this->del();
                header('location:' . $_SERVER['PHP_SELF'] . '?token=' . $this->TOKEN);
            }
            exit(0);
        }
        if ($_SERVER['REQUEST_METHOD'] != 'GET') {
            http_response_code(404);
            exit(0);
        }
        if ($_GET['token'] != $this->TOKEN) {
            $_SESSION["admin"] = false;
            http_response_code(404);
            exit(0);
        } else {
            $_SESSION["admin"] = true;
            $this->read();
        }
    }
    function init_file()
    {
        if (!file_exists($this->FILE_PATH))
            $this->del();
    }
    function del()
    {
        $myfile = fopen($this->FILE_PATH, "w");
        $title = "date,user,status\n";
        fwrite($myfile, $title);
        fclose($myfile);
    }
    function read()
    {
        $content = "";
        $num = -1;
        $fp = fopen($this->FILE_PATH, 'r') or die("can't open file");
        while ($csv_line = fgetcsv($fp)) {
            $num += 1;
            if ($num < 1)
                continue;
            $temp = (string)$num;
            $content .= '<tr>';
            $content .= '<th scope="row">' . $temp . '</th>';
            for ($i = 0, $j = count($csv_line); $i < $j; $i++) {
                $content .= '<td>' . htmlentities($csv_line[$i]) . '</td>';
            }
            $content .= '</tr>';
        }
        fclose($fp) or die("can't close file");
        $this->content = $content;
    }
}

?>
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0,user-scalable=1">
    <link rel="icon" type="image/png" sizes="96x96" href="https://www.rainyun.com/img/favicon.png">
    <title><?php echo $html_title ?></title>
    <link href="https://cdn.staticfile.org/bootstrap/5.0.0-beta1/css/bootstrap.min.css" rel='stylesheet'>
</head>

<body style="background-color: rgb(246 246 246);">
    <div class="container">
        <br>
        <a id="a_ctr" style="visilibity:hidden" href="#control"></a>
        <h1 id="top" class="display-5 text-center" onclick="a_ctr.click()"><?php echo $html_title ?></h1>
        <hr>
        <table class="table  table-striped table-hover">
            <thead>
                <tr>
                    <th scope="col">order</th>
                    <th scope="col">date</th>
                    <th scope="col">user</th>
                    <th scope="col">status</th>
                </tr>
            </thead>
            <tbody>
                <?php echo $table ?>
            </tbody>
        </table>
        <hr>
        <div id='control' onsubmit='return tips()' style='text-align:center' class='container'>
            <form style='display:inline-block' action='' method='post'>
                <input name='del' value='true' style='display:none;'>
                <input type='submit' class='btn btn-danger ' value='删除'>
            </form>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <button id='refresh' class='btn btn-success '>刷新</button>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <button id="totop" class="btn btn-secondary" onclick="a_top.click()">回到顶部<a style="display:none;text-decoration:none;color:white;" id="a_top" href="#a_ctr"></a></button>
        </div>
        <hr>
        <script>
            //如果没有记录，则禁用删除
            if (document.querySelectorAll('tr').length == 1) {
                document.querySelector('input[type=submit]').disabled = "true"
            }
            //绑定刷新
            refresh.addEventListener('click', function() {
                location.reload();
            });

            function tips() {
                return confirm("是否确定删除所有日志？")
            }
            let tr = document.querySelectorAll("table > tbody > tr");
            for (let t of tr) {
                if (t.innerText.indexOf('success') == -1) {
                    t.className = "table-danger";
                }
            }
        </script>
        <script src="https://cdn.staticfile.org/bootstrap/5.1.1/js/bootstrap.min.js"></script>
</body>

</html>