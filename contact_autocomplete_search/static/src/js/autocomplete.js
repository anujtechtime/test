odoo.define('contact_autocomplete_search.autocomplete', function (require) {
"use strict";

var ajax = require('web.ajax');

function removeDropdown(){
    var existing = document.getElementById("contact-autocomplete-dropdown");
    if (existing){
        existing.remove();
    }
}

document.addEventListener("keyup", function (ev) {

    if (!ev.target.classList.contains("o_searchview_input")){
        return;
    }

    var value = ev.target.value;

    // Remove dropdown if empty or less than 2 chars
    if (!value || value.length < 2){
        removeDropdown();
        return;
    }

    ajax.jsonRpc('/contact_autocomplete/search', 'call', {
        term: value
    }).then(function (data) {

        removeDropdown();

        if (!data.length){
            return;
        }

        var box = document.createElement("div");
        box.id = "contact-autocomplete-dropdown";

        box.style.position = "absolute";
        box.style.background = "white";
        box.style.border = "1px solid #ddd";
        box.style.zIndex = "9999";
        box.style.width = ev.target.offsetWidth + "px";
        box.style.maxHeight = "250px";
        box.style.overflowY = "auto";

        // position under search bar
        var rect = ev.target.getBoundingClientRect();
        box.style.top = rect.bottom + window.scrollY + "px";
        box.style.left = rect.left + window.scrollX + "px";

        data.forEach(function (item) {

            var el = document.createElement("div");
            el.innerText = item.name;

            el.style.padding = "6px";
            el.style.cursor = "pointer";

            el.onmouseenter = function(){
                el.style.background = "#f5f5f5";
            };

            el.onmouseleave = function(){
                el.style.background = "white";
            };

            el.onclick = function () {
                window.location.href = "/web#id=" + item.id + "&model=res.partner&view_type=form";
            };

            box.appendChild(el);
        });

        document.body.appendChild(box);
    });

});

// hide dropdown when clicking anywhere
document.addEventListener("click", function () {
    removeDropdown();
});

});