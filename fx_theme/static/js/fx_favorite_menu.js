odoo.define('fx_theme.favorite_menu', function (require) {
    "use strict";

    var core = require('web.core');
    var Menu = require('fx_theme.menu')
    var session = require('web.session');

    Menu.include({
        favorites: [],

        /**
         * load the favorite
         */
        // willStart: function () {
        //     var self = this
        //     return this._rpc({
        //         "model": "fx.favorite_menu",
        //         "method": "search_read",
        //         args: [[['user_id', '=', session.uid]]],
        //         kwargs: { fields: ['id', 'menu_id', 'user_id', 'sequence'] }
        //     }).then(function (favorites) {
        //         self.favorites = favorites
        //         // change the _apps and sort it
        //         self._apps = _.filter(self._apps, function (app) {
        //             var favorite = _.find(self.favorites, function (tmpFavorite) {
        //                 return parseInt(tmpFavorite.menu_id[0]) == app.menuID;
        //             })
        //             if (!favorite) return false;
        //             app['sequence'] = favorite.sequence
        //             return true;
        //         });
        //         // sort the apps
        //         self._apps.sort(function (app1, app2) { return app1.sequence - app2.sequence });
        //     })
        // },

        get_favorite_apps: function() {
            return this._apps;
        }
    });
});
