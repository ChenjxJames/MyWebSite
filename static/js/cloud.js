$(document).ready(function () {
    var path = [];
    var opt_file_id_list = [];//被选中的文件（夹）id列表，用于文件移动
    getFlist(0, "全部");
    getUserInfo();


    function showUserInfo(data) {
        $("#username").text(data.username);
        $("#loading").hide();
    }

    //在搜索框激活时按下键盘按键
    $("#keyword").keydown(function (event) {
        //按下的按键是回车键
        if (event.which === 13) {
            alert("keyword:" + $("#keyword").val() + "  搜索模块待开发");
        }
    });

    //键盘时间监听
    $(document).keydown(function (event) {
        //ctrl+A
        if (event.ctrlKey && event.which === 65) {
            var fileItems = $(".file-item");
            if ($(".file-opt").length === fileItems.length) {
               fileItems.each(function () {
                    $(this).removeClass('file-opt');
                });
            } else {
                fileItems.each(function () {
                    $(this).addClass('file-opt');
                });
            }
            showOtherMenu();
        }
    });

    //鼠标点击左侧导航条
    $(".menu").click(function () {
        $(".menu").each(function () {
            $(this).removeClass("menu-opt");
        });
        $(this).addClass("menu-opt");
        if ($(this).attr("id") === "all_file") {
            $("#main_right_file_nav").css("display", "inline");
            $("#main_right_share_nav").css("display", "none");
            path = [];
            getFlist(0, "全部");
        } else if ($(this).attr("id") === "my_share") {
            $("#main_right_file_nav").css("display", "none");
            $("#main_right_share_nav").css("display", "inline");
            getShareList();
        } else if ($(this).attr("id") === "about") {
            $("#main_right_file_nav").css("display", "none");
            $("#main_right_share_nav").css("display", "none");
            getAbout();
        }
    });

    //鼠标点击文件项
    $("#main_right_content").click(function () {
        showOtherMenu();
    });

    //有文件对象被选中，显示其他选项
    function showOtherMenu() {
        if ($(".file-opt").length > 0) {
            $("#optBtns").css("display", "inline");
        } else {
            $("#optBtns").hide();
        }
    }


    //上传按钮单击____打开模态框，等待用户输入文件名及选择文件
    $("#btnUpload").click(function () {
        $("#filename").val("");
        $("#inputfile").val("");
        $("#uploadModal").modal('show');
    });

    //新建按钮单击____打开模态框，等待用户输入文件夹名
    $("#btnNewFile").click(function () {
        $("#foldername").val("");
        $("#setFolderInfoModal").modal('show');
    });

    //下载按钮单击
    $("#btnDownload").click(function () {
        $(".file-opt").each(function (i) {
            if ($(this).children("[name='fIsFolder']").val() === "true") {


                //文件夹下载待开发


                alert("download folder " + $(this).children("[name='fId']").val() + "文件夹下载待开发");
            } else {
                //多文件下载待开发
                downloadFile($(this).children("[name='fId']").val());
            }
        });
    });

    //粘贴按钮单击
    $("#btnPaste").click(function () {
        var f = path[path.length - 1];
        moveFile(f.id, opt_file_id_list);
        opt_file_id_list = [];
        $("#btnPaste").hide();
    });

    //文件上传模态框提交按钮单击____ajax上传数据
    $("#btnUploadSubmit").click(function () {
        var data = new FormData($('#uploadForm')[0]);
        var f = path[path.length - 1];
        data.append("fFolderId", f.id);
        data.append("fIsFolder", "");//这里的空字符串在python后端转化为bool型False
        uploadFile(data);
        $("#uploadModal").modal('hide');
    });

    //新建文件夹模态框提交按钮单击____ajax上传数据
    $("#btnNewFolderSubmit").click(function () {
        var f = path[path.length - 1];
        var data = new FormData();
        data.append("filename", $("#foldername").val());
        data.append("fFolderId", f.id);
        data.append("fIsFolder", "Ture");
        uploadFile(data);
        $("#setFolderInfoModal").modal('hide');
    });

    //更多操作下拉菜单中  重命名按钮  单击
    $("#other_menu_set_name").click(function () {
        if ($(".file-opt").length === 1) {
            var fId = $(".file-opt").children("[name='fId']").val();
            var fName = prompt("请输入文件（夹）名称：");
            setFileName(fId, fName);
        } else if ($(".file-opt").length === 0) {
            alert("请选中需要重命名的文件（夹）。");
        } else {
            alert("无法对多个文件（夹）同时重命名。");
        }
    });

    //更多操作下拉菜单中  移动按钮  单击
    $("#other_menu_move_file").click(function () {
        $(".file-opt").each(function () {
            opt_file_id_list.push($(this).children("[name='fId']").val());
        });
        $("#btnPaste").css("display", "inline");
    });

    //更多操作下拉菜单中  详情按钮  单击
    $("#other_menu_get_info").click(function () {
        if ($(".file-opt").length === 1) {
            var fId = $(".file-opt").children("[name='fId']").val();
            getInfo(fId);
        } else if ($(".file-opt").length === 0) {
            alert("请选中需要查看详情的文件（夹）。");
        } else {
            alert("无法同时查看多个文件（夹）详情。");
        }
    });

    //删除按钮单击
    $("#other_menu_del_file").click(function () {
        if (confirm("确定要永久删除选中的文件？")) {
            $(".file-opt").each(function (i) {
                delFile($(this).children("[name='fId']").val());
            });
        }
    });

    //返回按钮单击
    $("#btnReverse").click(function () {
        if (path.length > 1) {
            path.pop();
            var f = path.pop();
            getFlist(f.id, f.name);
        }
    });

    //鼠标点击文件路径中的一项
    $("#file_path_inner").on("click", "a", function () {
        var id = $(this).attr("name");
        while (true) {
            var f = path.pop();
            if (f.id === id) {
                break;
            }
            if (path.length < 1) {
                break;
            }
        }
        getFlist(id, $(this).text());
    });

    //鼠标单击文件项
    $("#main_right_content").on("click", ".file-item", function () {
        $(this).toggleClass("file-opt");
    });

    //鼠标双击文件项
    $("#main_right_content").on("dblclick", ".file-item", function () {
        if ($(this).children().eq(1).val() === "true") {
            getFlist($(this).children().eq(0).val(), $(this).children().eq(-1).text());
        } else {
            alert("不能在云端打开文件。");
        }
    });

    //鼠标移至文件项上方
    $("#main_right_content").on("mouseover", ".file-item", function () {
        $(this).addClass("file-focus");
    });

    //鼠标离开文件项上方
    $("#main_right_content").on("mouseout", ".file-item", function () {
        $(this).removeClass("file-focus");
    });

    //设置文件路径
    function setFilePath() {
        $("#file_path_inner").empty();
        $.each(path, function (i, item) {
            var htmlStr = "<a class='folder-a' name='" + item.id + "'>" + item.name + "</a><sapn class='fa fa-angle-right'></sapn>";
            $("#file_path_inner").append(htmlStr);
        });
    }

    //设置文件目录
    function setFileList(data) {
        setFilePath();
        var htmlStr = "<div>";
        $.each(data, function (i, item) {
            var fname = item.fName;
            if (item.fExtension) {
                fname += "." + item.fExtension;
            }
            htmlStr += "<div class='file-item text-center' title='" + fname + "'>";
            if (item.fIsFolder) {
                htmlStr += "<input type='hidden' value='" + item.fId + "' name='fId'><input type='hidden' value='" + item.fIsFolder + "' name='fIsFolder'><span class='fa fa-folder folder-icon'></span>";
            } else if (item.fType) {
                htmlStr += "<input type='hidden' value='" + item.fId + "' name='fId'><input type='hidden' value='" + item.fIsFolder + "' name='fIsFolder'><span class='fa fa-file-" + item.fType + "-o file-icon'></span>";
            } else {
                htmlStr += "<input type='hidden' value='" + item.fId + "' name='fId'><input type='hidden' value='" + item.fIsFolder + "' name='fIsFolder'><span class='fa fa-file-o file-icon'></span>";
            }
            htmlStr += "<p>" + fname + "</p></div>";
        });
        htmlStr += "</div>";
        $("#main_right_content").append(htmlStr);
    }

    //获取文件目录
    function getFlist(fFolderId, fName) {
        $("#loading").show();
        path.push(newFloder(fFolderId, fName));
        $.ajax({
            url: "/cloud/flist",
            data: {
                fFolderId: fFolderId
            },
            type: "post",
            dataType: "json",
            async: true,
            success: function (data) {
                if (data[0].state === '0') {
                    $("#main_right_content").empty();
                    setFileList(data[1]);
                } else if (data[0].state === '1') {
                    $("#main_right_content").empty();
                    setFilePath();
                    $("#main_right_content").append("<div class='text-center'><h4>" + data[0].info + "</h4></div>");
                } else {
                    alert(data[0].info + '   [' + data[0].state + ']');
                }
                $("#loading").hide();
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    //获取分享列表
    function getShareList() {
        $("#main_right_content").empty();
        $("#main_right_content").append("<div class='text-center'><h4>此功能尚未开放，敬请期待！</h4></div>");
    }

    //获取关于信息
    function getAbout() {
        $("#main_right_content").empty();
        $("#main_right_content").load("/cloud/about");
    }

    //上传文件
    function uploadFile(data) {
        $("#loading").show();
        $.ajax({
            url: "/cloud/upload",
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            type: "post",
            async: true,
            success: function (data) {
                if (data.state === '0') {
                    var f = path.pop();
                    getFlist(f.id, f.name);
                } else {
                    alert(data.info + '   [' + data.state + ']');
                    $("#loading").hide();
                }
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    //下载文件
    function downloadFile(fId) {
        var url = "/cloud/download";
        var form = $("<form>");
        form.attr("style", "display:none");
        form.attr("id", "download_file_form_" + fId);
        form.attr("method", "get");
        form.attr("action", url);
        $("body").append(form);
        var input1 = $("<input>");
        input1.attr("type", "hidden");
        input1.attr("name", "fId");
        input1.attr("value", fId);
        form.append(input1);
        form.submit();
        // window.location = "/cloud/download?fId=" + fId;
    }

    //重命名
    function setFileName(fId, fName) {
        $("#loading").show();
        $.ajax({
            url: "/cloud/setfilename",
            data: {
                fId: fId,
                fName: fName
            },
            type: "post",
            dataType: "json",
            async: true,
            success: function (data) {
                if (data.state === '0') {
                    var f = path.pop();
                    getFlist(f.id, f.name);
                } else {
                    alert(data.info + '   [' + data.state + ']');
                    $("#loading").hide();
                }
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    //删除文件（夹）（fId）
    function delFile(fId) {
        $("#loading").show();
        $.ajax({
            url: "/cloud/del",
            data: {
                fId: fId
            },
            type: "post",
            dataType: "json",
            async: true,
            success: function (data) {
                if (data.state === '0') {
                    var f = path.pop();
                    getFlist(f.id, f.name);
                } else {
                    alert(data.info + '   [' + data.state + ']');
                    $("#loading").hide();
                }
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    //移动文件（fFolderId,opt_file_id_list）目的文件夹Id，及移动文件（夹）序列
    function moveFile(fFolderId, file_id_list) {
        $("#loading").show();
        $.ajax({
            url: "/cloud/movefile",
            data: {
                fFolderId: fFolderId,
                fIdList: file_id_list
            },
            type: "post",
            dataType: "json",
            async: true,
            traditional: true,
            success: function (data) {
                if (data.state === '0') {
                    var f = path.pop();
                    getFlist(f.id, f.name);
                } else {
                    alert(data.info + '   [' + data.state + ']');
                    $("#loading").hide();
                }
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    //获取文件信息（fId）
    function getInfo(fId) {
        $("#loading").show();
        $.ajax({
            url: "/cloud/getinfo",
            data: {
                fId: fId
            },
            type: "post",
            dataType: "json",
            async: true,
            success: function (data) {
                if (data[0].state === '0') {
                    showInfo(data[1]);
                } else {
                    alert(data[0].info + '   [' + data[0].state + ']');
                }
                $("#loading").hide();
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    function showInfo(data) {
        var htmlStr = "<tr><td style='width: 80px;'>";
        if (data.isFolder) {
            htmlStr += "<span class='fa fa-folder folder-icon' style='margin-right: 10px;'></span>";
        } else if (data.type) {
            htmlStr += "<span class='fa fa-file-" + data.type + "-o file-icon' style='margin-right: 10px;'></span>";
        } else {
            htmlStr += "<span class='fa fa-file-o file-icon' style='margin-right: 10px;'></span>";
        }
        var fname = data.name;
        if (data.extension) {
            fname += "." + data.extension;
        }
        htmlStr += "</td><td><h4>" + fname + "</h4></td></tr>";
        htmlStr += "<tr><td><b>创建时间:</b></td><td>" + data.uploadTime + "</td></tr>";
        htmlStr += "<tr><td><b>所有者:</b></td><td>" + data.username + "</td></tr>";
        htmlStr += "<tr><td><b>md5:</b></td><td>" + data.md5 + "</td></tr>";
        $("#file_info").append(htmlStr);
        $("#showInfoModal").modal('show');
    }

    function getUserInfo() {
        $("#loading").show();
        $.ajax({
            url: "/user/getuserinfo",
            data: {},
            dataType: "json",
            async: true,
            success: function (data) {
                showUserInfo(data);
            },
            error: function () {
                $("#loading").hide();
                alert("ajax error")
            }
        });
    }

    //构建文件夹对象
    function newFloder(id, name) {
        var folder = {};
        folder.id = id;
        folder.name = name;
        return folder
    }
});

//关闭模态框
function modalHide() {
    $("#uploadModal").modal('hide');
    $("#setFolderInfoModal").modal('hide');
    $("#showInfoModal").modal('hide');
    $("#file_info").empty();
}