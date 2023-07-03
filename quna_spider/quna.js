{
                key: "getRandomKey",
                value: function (t) {
                    var n = "";
                    var r = ("" + t).substr(4);
                    r.split("").forEach(function(e) {
                        n += e.charCodeAt()
                    });
                    var i = (0,
                    f.default)(n).toString();
                    return i.substr(-6)
                }
            }, {
                key: "getToken",
                value: function() {
                    var t = {};
                    t[this.getRandomKey(this.getQtTime((0,
                    s.default)(this.dencryptCode(this.qtTime))))] = this.encrypt();
                    return t
                }
            }, {
                key: "encryptFunction",
                value: function() {
                    return [function(e) {
                        var t = (0,
                        u.default)(e).toString();
                        return (0,
                        f.default)(t).toString()
                    }
                    , function(e) {
                        var t = (0,
                        f.default)(e).toString();
                        return (0,
                        u.default)(t).toString()
                    }
                    ]
                }
            }, {
                key: "dencryptCode",
                value: function(t) {
                    return t.map(function(e) {
                        return String.fromCharCode(e - 2)
                    }).join("")
                }
            }, {
                key: "getQtTime",
                value: function(t) {
                    return t ? Number(t.split(",").map(function(e) {
                        return String.fromCharCode(e - 2)
                    }).join("")) : 0
                }
            }, {
                key: "getTokenStr",
                value: function() {
                    var t = this.dencryptCode(this.tokenStr);
                    var n = document.getElementById(t).innerHTML;
                    return n ? n : (0,
                    s.default)(this.dencryptCode(this.cookieToken))
                }
            },


//参数生成方法
{
    key: "encrypt",
    value: function() {
        var t = this.getTokenStr()
          , n = this.getQtTime((0,
        s.default)(this.dencryptCode(this.qtTime)))
          , r = n % 2;
        return this.encryptFunction()[r](t + n)
                }
            },


{
    key: "encryptToken",
    value: function(t) {
        return (0,
        f.default)(t).toString()
                }
            }