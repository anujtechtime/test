
odoo.define('contact_autocomplete_search.autocomplete', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    document.addEventListener("keyup", function (ev) {
        if (!ev.target.classList.contains("o_searchview_input")) {
            return;
        }

        var value = ev.target.value;
        if (value.length < 2){
            return;
        }

        ajax.jsonRpc('/contact_autocomplete/search', 'call', {
            term: value
        }).then(function (data) {

            var existing = document.getElementById("contact-autocomplete-dropdown");
            if (existing){
                existing.remove();
            }

            var box = document.createElement("div");
            box.id = "contact-autocomplete-dropdown";
            box.style.position = "absolute";
            box.style.background = "white";
            box.style.border = "1px solid #ddd";
            box.style.zIndex = "9999";
            box.style.padding = "5px";
            box.style.width = "300px";

            data.forEach(function (item) {
                var el = document.createElement("div");
                el.innerText = item.name;
                el.style.padding = "4px";
                el.style.cursor = "pointer";

                el.onclick = function () {
                    window.location.href = "/web#id=" + item.id + "&model=res.partner&view_type=form";
                };

                box.appendChild(el);
            });

            ev.target.parentNode.appendChild(box);
        });
    });
});
