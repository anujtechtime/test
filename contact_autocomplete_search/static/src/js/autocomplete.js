// odoo.define('contact_autocomplete_search.autocomplete', function (require) {
// "use strict";

// var ajax = require('web.ajax');

// function removeDropdown(){
//     var existing = document.getElementById("contact-autocomplete-dropdown");
//     if (existing){
//         existing.remove();
//     }
// }

// document.addEventListener("keyup", function (ev) {

//     if (!ev.target.classList.contains("o_searchview_input")){
//         return;
//     }

//     var value = ev.target.value;

//     // Remove dropdown if empty or less than 2 chars
//     if (!value || value.length < 2){
//         removeDropdown();
//         return;
//     }

//     ajax.jsonRpc('/contact_autocomplete/search', 'call', {
//         term: value
//     }).then(function (data) {

//         removeDropdown();

//         if (!data.length){
//             return;
//         }

//         var box = document.createElement("div");
//         box.id = "contact-autocomplete-dropdown";

//         box.style.position = "absolute";
//         box.style.background = "white";
//         box.style.border = "1px solid #ddd";
//         box.style.zIndex = "9999";
//         box.style.width = ev.target.offsetWidth + "px";
//         box.style.maxHeight = "250px";
//         box.style.overflowY = "auto";

//         // position under search bar
//         var rect = ev.target.getBoundingClientRect();
//         box.style.top = rect.bottom + window.scrollY + "px";
//         box.style.left = rect.left + window.scrollX + "px";

//         data.forEach(function (item) {

//             var el = document.createElement("div");
//             el.innerText = item.name;

//             el.style.padding = "6px";
//             el.style.cursor = "pointer";

//             el.onmouseenter = function(){
//                 el.style.background = "#f5f5f5";
//             };

//             el.onmouseleave = function(){
//                 el.style.background = "white";
//             };

//             el.onclick = function () {
//                 window.location.href = "/web#id=" + item.id + "&model=res.partner&view_type=form";
//             };

//             box.appendChild(el);
//         });

//         document.body.appendChild(box);
//     });

// });

// // hide dropdown when clicking anywhere
// document.addEventListener("click", function () {
//     removeDropdown();
// });

// });

odoo.define('contact_autocomplete_search.autocomplete', function (require) {
"use strict";

var ajax = require('web.ajax');
var core = require('web.core');

function removeDropdown(){
    var existing = document.getElementById("contact-autocomplete-dropdown");
    if (existing){
        existing.remove();
    }
}

function isContactSearch(inputElement) {
    // For Odoo 13 - Check if we're on a contact view by examining the DOM and Odoo's context
    
    // Method 1: Check the search view's model by looking at parent elements
    var searchView = inputElement.closest('.o_searchview');
    if (searchView) {
        // Check for hidden model input or data attribute
        var modelInput = searchView.querySelector('input[name="model"]');
        if (modelInput && modelInput.value === 'res.partner') {
            return true;
        }
    }
    
    // Method 2: Check the main content view for res.partner
    var contentView = document.querySelector('.o_content');
    if (contentView) {
        var modelData = contentView.getAttribute('data-model');
        if (modelData === 'res.partner') {
            return true;
        }
    }
    
    // Method 3: Check URL hash for res.partner model (Odoo 13 uses hash navigation)
    var hash = window.location.hash;
    if (hash && hash.indexOf('model=res.partner') !== -1) {
        return true;
    }
    
    // Method 4: Check action ID or view context in Odoo 13
    var actionManager = document.querySelector('.o_action_manager');
    if (actionManager) {
        try {
            // Check if any data attribute contains partner info
            var attributes = actionManager.querySelectorAll('[data-model]');
            for (var i = 0; i < attributes.length; i++) {
                if (attributes[i].getAttribute('data-model') === 'res.partner') {
                    return true;
                }
            }
        } catch(e) {}
    }
    
    // Method 5: Check if we're in Contacts from visible UI elements
    var breadcrumb = document.querySelector('.o_breadcrumb');
    if (breadcrumb && breadcrumb.innerText.toLowerCase().indexOf('contact') !== -1) {
        return true;
    }
    
    // Method 6: Check active menu item for Contacts
    var activeMenus = document.querySelectorAll('.active .oe_menu_text, .o_menu_active');
    for (var i = 0; i < activeMenus.length; i++) {
        var menuText = activeMenus[i].innerText.toLowerCase();
        if (menuText === 'contacts' || menuText === 'contact') {
            return true;
        }
    }
    
    return false;
}

// Debounce function to avoid too many requests
function debounce(func, wait) {
    var timeout;
    return function executedFunction() {
        var later = function() {
            clearTimeout(timeout);
            func();
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

document.addEventListener("keyup", function (ev) {
    // Only trigger on search input (Odoo 13 specific class)
    if (!ev.target.classList.contains("o_searchview_input")){
        return;
    }
    
    // ONLY process for contact searches
    if (!isContactSearch(ev.target)) {
        removeDropdown();
        return;
    }

    var value = ev.target.value;

    // Remove dropdown if empty or less than 3 chars (Odoo 13 optimization)
    if (!value || value.length < 3){
        removeDropdown();
        return;
    }

    // Debounce the search request
    clearTimeout(window.contactAutocompleteTimeout);
    window.contactAutocompleteTimeout = setTimeout(function() {
        
        ajax.jsonRpc('/contact_autocomplete/search', 'call', {
            term: value
        }).then(function (data) {
            removeDropdown();

            if (!data || !data.length){
                return;
            }

            var box = document.createElement("div");
            box.id = "contact-autocomplete-dropdown";

            box.style.position = "absolute";
            box.style.background = "white";
            box.style.border = "1px solid #ddd";
            box.style.borderRadius = "3px";
            box.style.zIndex = "9999";
            box.style.width = ev.target.offsetWidth + "px";
            box.style.maxHeight = "250px";
            box.style.overflowY = "auto";
            box.style.boxShadow = "0 2px 6px rgba(0,0,0,0.2)";
            box.style.fontFamily = "'Lucida Grande', 'Ubuntu', Arial, sans-serif";

            // Position under search bar - Odoo 13 specific positioning
            var rect = ev.target.getBoundingClientRect();
            var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            box.style.top = rect.bottom + scrollTop + "px";
            box.style.left = rect.left + window.pageXOffset + "px";

            data.forEach(function (item) {
                var el = document.createElement("div");
                
                // Better formatting for Odoo 13
                var displayText = item.name || item.display_name || item.text || 'Contact';
                el.innerText = displayText;
                
                // Add email if available
                if (item.email) {
                    var emailSpan = document.createElement("span");
                    emailSpan.innerText = ' - ' + item.email;
                    emailSpan.style.color = "#666";
                    emailSpan.style.fontSize = "11px";
                    el.appendChild(emailSpan);
                }

                el.style.padding = "8px 12px";
                el.style.cursor = "pointer";
                el.style.borderBottom = "1px solid #e0e0e0";
                el.style.fontSize = "12px";
                el.style.transition = "background 0.2s";

                el.onmouseenter = function(){
                    el.style.background = "#eaedf2";
                };

                el.onmouseleave = function(){
                    el.style.background = "white";
                };

                // Odoo 13 compatible URL opening
                el.onclick = function (ev) {
                    ev.stopPropagation();
                    var partnerId = item.id;
                    var actionId = 0; // You can set specific action ID if needed
                    
                    // Odoo 13 standard URL format
                    var url = `/web#id=${partnerId}&model=res.partner&view_type=form`;
                    
                    // If you have a specific action ID:
                    // var url = `/web#id=${partnerId}&action=${actionId}&model=res.partner&view_type=form`;
                    
                    window.location.href = url;
                };

                box.appendChild(el);
            });

            document.body.appendChild(box);
        }).catch(function(error) {
            console.error("Contact autocomplete error:", error);
            removeDropdown();
        });
    }, 300); // 300ms debounce delay
});

// Close dropdown on escape key
document.addEventListener("keydown", function(ev) {
    if (ev.key === "Escape") {
        removeDropdown();
    }
});

// Hide dropdown when clicking outside
document.addEventListener("click", function (ev) {
    var dropdown = document.getElementById("contact-autocomplete-dropdown");
    var searchInput = ev.target.closest('.o_searchview_input');
    
    // Don't remove if clicking inside the dropdown or on the search input
    if (dropdown && dropdown.contains(ev.target)) {
        return;
    }
    if (searchInput) {
        return;
    }
    removeDropdown();
});

// Also handle scroll events to reposition or hide dropdown
var scrollTimeout;
window.addEventListener('scroll', function() {
    if (scrollTimeout) {
        clearTimeout(scrollTimeout);
    }
    scrollTimeout = setTimeout(function() {
        removeDropdown();
    }, 100);
});

});