window.save_alert = function (message, title, callbak) {
    (closeSaveAlert = function () { $('#alert-window').remove(); })();
    var bg = $('<div class="alert-bg"></div>');
    var wnd = $('<div class="alert-wnd"><div class="alert-head"><center>'
                + (title || "")
                + '</center></div><div class="alert-body"><div class="alert-icon"><span></span></div><div class="alert-msg"><p>'
                + (message || '') + '</p></div></div><div class="alert-footer"><a class="btn btn-small" id="alert-confirm">取消</a><a class="btn1 btn-small" onclick="save_info();">确定</a></div></div>');
    window.top.$(document.body).append($('<div id="alert-window"></div>').append(bg).append(wnd).delegate('#alert-confirm', 'click', function () { closeSaveAlert(); callbak && callbak(); }));
};

function save_info() {
    var arr_info = window.location.search;
    window.location.href="/MT_migration"+ arr_info;
}