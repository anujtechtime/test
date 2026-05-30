odoo.define('contact_autocomplete_custom_search.custom_contact_search', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    function removeDropdown() {
        $("#contact-autocomplete-dropdown").remove();
    }

    $(document).on('keyup', '.o_contact_search_input', function (ev) {

        var value = ev.target.value;

        removeDropdown();

        if (!value || value.length < 3) {
            return;
        }

        clearTimeout(window.contactSearchTimeout);

        window.contactSearchTimeout = setTimeout(function () {

            ajax.jsonRpc('/contact_autocomplete/search', 'call', {
                term: value
            }).then(function (data) {

                if (!data.length) {
                    return;
                }

                var rect = ev.target.getBoundingClientRect();

                var $dropdown = $('<div id="contact-autocomplete-dropdown"></div>');

                $dropdown.css({
                    position: 'absolute',
                    top: rect.bottom + window.scrollY,
                    left: rect.left + window.scrollX,
                    width: rect.width,
                    background: 'white',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    zIndex: 9999,
                    maxHeight: '300px',
                    overflowY: 'auto',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
                });

                data.forEach(function (item) {

                    var $item = $('<div class="contact-item">' +
                        '<div><strong>' + item.name + '</strong></div>' +
                        '<div style="font-size:11px;color:#777;">' +
                        (item.email || '') +
                        '</div></div>');

                    $item.css({
                        padding: '10px',
                        cursor: 'pointer',
                        borderBottom: '1px solid #eee',
                    });

                    $item.hover(
                        function () {
                            $(this).css('background', '#f5f5f5');
                        },
                        function () {
                            $(this).css('background', 'white');
                        }
                    );

                    $item.on('click', function () {
                        window.location.href =
                            '/web#id=' + item.id + '&model=res.partner&view_type=form';
                    });

                    $dropdown.append($item);
                });

                $('body').append($dropdown);

            });

        }, 300);

    });

    $(document).on('click', function (ev) {

        if (
            !$(ev.target).closest('#contact-autocomplete-dropdown').length &&
            !$(ev.target).closest('.o_contact_search_input').length
        ) {
            removeDropdown();
        }

    });

});
