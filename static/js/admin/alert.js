window.alert = function (message, title, callbak) {
    (closeAlert = function () { $('#alert-window').remove(); })();
    var bg = $('<div class="alert-bg"></div>');
    var wnd = $('<div class="alert-wnd"><div class="alert-head"><center>'
                + (title || "")
                + '</center></div><div class="alert-body"><div class="alert-icon"><span></span></div><div class="alert-msg"><p>'
                + (message || '') + '</p></div></div><div class="alert-footer"><a class="btn btn-small" id="alert-confirm">取消</a><a class="btn1 btn-small" onclick="close_info();">关闭</a></div></div>');
    window.top.$(document.body).append($('<div id="alert-window"></div>').append(bg).append(wnd).delegate('#alert-confirm', 'click', function () { closeAlert(); callbak && callbak(); }));
};

function close_info() {
    var close_tool_data_json={"mod":"close_tool"};
    close_tool_data_json.ip="tasks"
    $.ajax({
        async:true,
        type: 'post',
        dataType: 'json',
        url: 'MT_close_tool',
        data: $.toJSON(close_tool_data_json),
        success: function(res) {
        }
    });
}