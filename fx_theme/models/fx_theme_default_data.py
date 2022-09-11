# -*- coding: utf-8 -*-

version = "1.0.0.14"

default_settings = {
    "menu_type": 'vertical',
    "font_type": "sans-serif",
    "fixed_footer": True,
    "fixed_header": True,
    "show_pager_header": True,
    "theme_style": "normal",
    "favorite_mode": False,
}

normal_mode = {
    "name": "normal",
    "theme_styles": [{
        "name": "style1",
        "deletable": False,
        "style_items": [{
            "name": "side bar",
            "group": "side_bar",
            "identity": "side_bar_color",
            "css_info": [{
                "selector": ".navigation .side_bar",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "side bar text color",
            "group": "side_bar",
            "identity": "side_bar_txt_color",
            "css_info": [{
                "selector": ".navigation .side_bar .navigation-menu-tab .fx_side_bar_app_name",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "side bar footer",
            "group": "side_bar",
            "css_info": [{
                "selector": ".navigation .side_bar .fx-nav-footer",
                "key": "background"
            }],
            "val": "#12549e"
        },  {
            "name": "navigation",
            "group": "navigation",
            "identity": ".navigation .secondary_nav .navigation_background_color",
            "css_info": [{
                "selector": ".navigation",
                "key": "background"
            }],
            "val": "#f8f9fa"
        }, {
            "name": "border",
            "group": "border",
            "identity": "border_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "border-color"
            }, {
                "selector": ".header",
                "key": "border-bottom-color"
            }, {
                "selector": ".navigation-logo",
                "key": "border-bottom-color"
            }, {
                "selector": "hr",
                "key": "border-color"
            }, {
                "selector": ".page-header",
                "key": "border-bottom-color"
            }, {
                "selector": ".customizer .customizer-footer",
                "key": "border-color"
            }],
            "val": "#EBEBEB"
        },  {
            "name": "header",
            "group": "header",
            "identity": "header_background_color",
            "css_info": [{
                "selector": ".header",
                "key": "background"
            }],
            "val": "#fff"
        }, {
            "name": "header text color",
            "group": "header",
            "identity": "header_text_color",
            "css_info": [{
                "selector": ".header",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "header background color (horizontal mode)",
            "group": "header",
            "identity": "header_background_color",
            "css_info": [{
                "selector": "body.hz_menu .header",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "header text color (horizontal mode)",
            "group": "header",
            "identity": "header_text_color",
            "css_info": [{
                "selector": "body.hz_menu .hz_app_menu .app_item",
                "key": "color"
            }, {
                "selector": "body.hz_menu .header .navbar-nav a:not(.dropdown-item)",
                "key": "color"
            }],
            "val": "#fff"
        },  {
            "name": "page header",
            "group": "page_header",
            "identity": "page_header",
            "css_info": [{
                "selector": ".page-header",
                "key": "background"
            }],
            "val": "#f8f9fa"
        }, {
            "name": "body background color",
            "group": "body",
            "identity": 'body_background_color',
            "css_info": [{
                "selector": ".body",
                "key": "background"
            }, {
                "selector": ".o_action_manager",
                "key": "background"
            }],
            "val": "#fff"
        }, {
            "name": "footer background color",
            "group": "footer",
            "identity": "footer_background_color",
            "css_info": [{
                "selector": ".page-footer",
                "key": "background"
            }],
            "val": "#ffffff"
        },  {
            "name": "button primary",
            "group": "button_primary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "button border color",
            "group": "button_primary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "border"
            }],
            "val": "#1565c0"
        }, {
            "name": "text color",
            "group": "button_primary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "color"
            }],
            "val": "#1565c0"
        }, {
            "name": "hover color",
            "group": "button_primary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "color"
            }],
            "val": "#1565c0"
        }, {
            "name": "back ground color",
            "group": "button_secondary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "button border color",
            "group": "button_secondary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "border"
            }],
            "val": "#1565c0"
        }, {
            "name": "text color",
            "group": "button_secondary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "color"
            }],
            "val": "#1565c0"
        }, {
            "name": "hover color",
            "group": "button_secondary",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "color"
            }],
            "val": "#1565c0"
        }, {
            "name": "customizer",
            "group": "customizer",
            "css_info": [{
                "selector": ".customizer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "drop down",
            "group": "drop_down",
            "css_info": [{
                "selector": ".dropdown-menu",
                "key": "background"
            }, {
                "selector": ".fx_search_options",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "hover color",
            "group": "hover",
            "css_info": [{
                "selector": ".dropdown-menu .dropdown-item:hover",
                "key": "background"
            }],
            "val": "#5A6169"
        }, {
            "name": "tab pane",
            "group": "hover",
            "css_info": [{
                "selector": ".tab-pane",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }]
    }, {
        "name": "style2",
        "deletable": False,
        "style_items": [{
            "name": "side bar",
            "group": "navigation",
            "identity": "side_bar_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "background"
            }],
            "val": "#42389d"
        }, {
            "name": "navigation",
            "group": "navigation",
            "identity": "navigation_color",
            "css_info": [{
                "selector": ".navigation",
                "key": "background"
            }],
            "val": "#f8f9fa"
        }, {
            "name": "side bar footer",
            "group": "navigation",
            "css_info": [{
                "selector": ".navigation .fx-nav-footer",
                "key": "background"
            }],
            "val": "#30296f"
        }, {
            "name": "border",
            "group": "border",
            "identity": "border_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "border-color"
            }, {
                "selector": ".header",
                "key": "border-bottom-color"
            }, {
                "selector": ".navigation-logo",
                "key": "border-bottom-color"
            }, {
                "selector": "hr",
                "key": "border-color"
            }, {
                "selector": ".page-header",
                "key": "border-bottom-color"
            }, {
                "selector": ".customizer .customizer-footer",
                "key": "border-color"
            }],
            "val": "#EBEBEB"
        }, {
            "name": "text color",
            "group": "text_color",
            "identity": "text_color",
            "css_info": [{
                "selector": ".header",
                "key": "color"
            }, {
                "selector": ".table",
                "key": "color"
            }],
            "val": "#5A6169"
        }, {
            "name": "header",
            "group": "header",
            "identity": "header_color",
            "css_info": [{
                "selector": ".header",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "horizontal header",
            "group": "header",
            "identity": "horizontal_header_color",
            "css_info": [{
                "selector": "body.hz_menu .header",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "horizontal header text color",
            "group": "header",
            "identity": "horizontal_header_text_color",
            "css_info": [{
                "selector": "body.hz_menu .hz_app_menu .app_item",
                "key": "color"
            }, {
                "selector": "body.hz_menu .header .navbar-nav a:not(.dropdown-item)",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "page header",
            "group": "page_header",
            "identity": "page_header",
            "css_info": [{
                "selector": ".page-header",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "body",
            "group": "body",
            "identity": "body_color",
            "css_info": [{
                "selector": ".body",
                "key": "background"
            }, {
                "selector": ".o_action_manager",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "footer",
            "group": "footer",
            "identity": "footer_color",
            "keys": "background",
            "css_info": [{
                "selector": ".page-footer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        },  {
            "name": "button primary",
            "group": "button",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "background"
            }],
            "val": "#1565C0"
        }, {
            "name": "button secondary",
            "group": "button",
            "css_info": [{
                "selector": ".btn-secondary",
                "key": "background"
            }],
            "val": "#717d8a"
        }, {
            "name": "customizer",
            "group": "customizer",
            "css_info": [{
                "selector": ".customizer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "drop down",
            "group": "drop_down",
            "css_info": [{
                "selector": ".dropdown-menu",
                "key": "background"
            }, {
                "selector": ".fx_search_options",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "hover color",
            "group": "hover",
            "css_info": [{
                "selector": ".dropdown-menu .dropdown-item:hover",
                "key": "background"
            }],
            "val": "#5A6169"
        }, {
            "name": "tab pane",
            "group": "hover",
            "css_info": [{
                "selector": ".tab-pane",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }]
    }, {
        "name": "style3",
        "deletable": False,
        "style_items": [{
            "name": "side bar",
            "group": "navigation",
            "identity": "side_bar_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "background"
            }],
            "val": "rgb(203, 48, 102)"
        }, {
            "name": "navigation",
            "group": "navigation",
            "identity": "navigation_color",
            "css_info": [{
                "selector": ".navigation",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "side bar footer",
            "group": "navigation",
            "css_info": [{
                "selector": ".navigation .fx-nav-footer",
                "key": "background"
            }],
            "val": "rgb(141, 29, 68)"
        }, {
            "name": "border",
            "group": "border",
            "identity": "border_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "border-color"
            }, {
                "selector": ".header",
                "key": "border-bottom-color"
            }, {
                "selector": ".navigation-logo",
                "key": "border-bottom-color"
            }, {
                "selector": "hr",
                "key": "border-color"
            }, {
                "selector": ".page-header",
                "key": "border-bottom-color"
            }, {
                "selector": ".customizer .customizer-footer",
                "key": "border-color"
            }],
            "val": "#EBEBEB"
        }, {
            "name": "text color",
            "group": "text_color",
            "identity": "text_color",
            "css_info": [{
                "selector": ".header",
                "key": "color"
            }, {
                "selector": ".table",
                "key": "color"
            }],
            "val": "#5A6169"
        }, {
            "name": "header",
            "group": "header",
            "identity": "header_color",
            "css_info": [{
                "selector": ".header",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "horizontal header",
            "group": "header",
            "identity": "horizontal_header_color",
            "css_info": [{
                "selector": "body.hz_menu .header",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "horizontal header text color",
            "group": "header",
            "identity": "horizontal_header_text_color",
            "css_info": [{
                "selector": "body.hz_menu .hz_app_menu .app_item",
                "key": "color"
            }, {
                "selector": "body.hz_menu .header .navbar-nav a:not(.dropdown-item)",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "page header",
            "group": "page_header",
            "identity": "page_header",
            "css_info": [{
                "selector": ".page-header",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "body",
            "group": "body",
            "identity": 'body_color',
            "css_info": [{
                "selector": ".body",
                "key": "background"
            }, {
                "selector": ".o_action_manager",
                "key": "background"
            }],
            "val": "#f5f6fa"
        }, {
            "name": "footer",
            "group": "footer",
            "identity": "footer_color",
            "keys": "background",
            "css_info": [{
                "selector": ".page-footer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        },  {
            "name": "button primary",
            "group": "button",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "background"
            }],
            "val": "#1565C0"
        }, {
            "name": "button secondary",
            "group": "button",
            "css_info": [{
                "selector": ".btn-secondary",
                "key": "background"
            }],
            "val": "#717d8a"
        }, {
            "name": "customizer",
            "group": "customizer",
            "css_info": [{
                "selector": ".customizer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "drop down",
            "group": "drop_down",
            "css_info": [{
                "selector": ".dropdown-menu",
                "key": "background"
            }, {
                "selector": ".fx_search_options",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "hover color",
            "group": "hover",
            "css_info": [{
                "selector": ".dropdown-menu .dropdown-item:hover",
                "key": "background"
            }],
            "val": "#5A6169"
        }, {
            "name": "tab pane",
            "group": "hover",
            "css_info": [{
                "selector": ".tab-pane",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }]
    },  {
        "name": "style4",
        "deletable": False,
        "style_items": [{
            "name": "side bar",
            "group": "navigation",
            "identity": "side_bar_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "background"
            }],
            "val": "rgb(244, 67, 54)"
        }, {
            "name": "navigation",
            "group": "navigation",
            "identity": "navigation_color",
            "css_info": [{
                "selector": ".navigation",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "side bar footer",
            "group": "navigation",
            "css_info": [{
                "selector": ".navigation .fx-nav-footer",
                "key": "background"
            }],
            "val": "rgb(197, 39, 27)"
        }, {
            "name": "border",
            "group": "border",
            "identity": "border_color",
            "css_info": [{
                "selector": ".navigation .navigation-menu-tab",
                "key": "border-color"
            }, {
                "selector": ".header",
                "key": "border-bottom-color"
            }, {
                "selector": ".navigation-logo",
                "key": "border-bottom-color"
            }, {
                "selector": "hr",
                "key": "border-color"
            }, {
                "selector": ".page-header",
                "key": "border-bottom-color"
            }, {
                "selector": ".customizer .customizer-footer",
                "key": "border-color"
            }],
            "val": "#EBEBEB"
        }, {
            "name": "text color",
            "group": "text_color",
            "identity": "text_color",
            "css_info": [{
                "selector": ".header",
                "key": "color"
            }, {
                "selector": ".table",
                "key": "color"
            }],
            "val": "#5A6169"
        }, {
            "name": "header",
            "group": "header",
            "identity": "header_color",
            "css_info": [{
                "selector": ".header",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "horizontal header",
            "group": "header",
            "identity": "horizontal_header_text_color",
            "css_info": [{
                "selector": "body.hz_menu .header",
                "key": "background"
            }],
            "val": "#1565c0"
        }, {
            "name": "horizontal header text color",
            "group": "header",
            "identity": "horizontal_header_text_color",
            "css_info": [{
                "selector": "body.hz_menu .hz_app_menu .app_item",
                "key": "color"
            }, {
                "selector": "body.hz_menu .header .navbar-nav a:not(.dropdown-item)",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "page header",
            "group": "page_header",
            "identity": "page_header",
            "css_info": [{
                "selector": ".page-header",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "body",
            "group": "body",
            "identity": 'body_color',
            "css_info": [{
                "selector": ".body",
                "key": "background"
            }, {
                "selector": ".o_action_manager",
                "key": "background"
            }],
            "val": "#f5f6fa"
        }, {
            "name": "footer",
            "group": "footer",
            "identity": "footer_color",
            "keys": "background",
            "css_info": [{
                "selector": ".page-footer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        },  {
            "name": "button primary",
            "group": "button",
            "css_info": [{
                "selector": ".btn-primary",
                "key": "background"
            }],
            "val": "#1565C0"
        }, {
            "name": "button secondary",
            "group": "button",
            "css_info": [{
                "selector": ".btn-secondary",
                "key": "background"
            }],
            "val": "#717d8a"
        }, {
            "name": "customizer",
            "group": "customizer",
            "css_info": [{
                "selector": ".customizer",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "drop down",
            "group": "drop_down",
            "css_info": [{
                "selector": ".dropdown-menu",
                "key": "background"
            }, {
                "selector": ".fx_search_options",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }, {
            "name": "hover color",
            "group": "hover",
            "css_info": [{
                "selector": ".dropdown-menu .dropdown-item:hover",
                "key": "background"
            }],
            "val": "#5A6169"
        }, {
            "name": "tab pane",
            "group": "hover",
            "css_info": [{
                "selector": ".tab-pane",
                "key": "background"
            }],
            "val": "#FFFFFF"
        }]
    }]
}

dark_mode = {
    "name": "dark",
    "theme_styles": [{
        "name": "style1",
        "deletable": False,
        "style_items": [{
            "name": "side bar",
            "group": "navigation",
            "identity": "side_bar_color",
            "css_info": [{
                "selector": "body.dark .navigation .navigation-menu-tab",
                "key": "background"
            }],
            "val": "#454c66"
        }, {
            "name": "navigation",
            "group": "navigation",
            "identity": "navigation_color",
            "css_info": [{
                "selector": ".navigation",
                "key": "background"
            }],
            "val": "#454c66"
        }, {
            "name": "side bar footer",
            "group": "navigation",
            "css_info": [{
                "selector": "body.dark .navigation .fx-nav-footer",
                "key": "background"
            }],
            "val": "#394263"
        }, {
            "name": "border",
            "group": "border",
            "identity": "border_color",
            "css_info": [{
                "selector": "body.dark .navigation .navigation-menu-tab",
                "key": "border-color"
            }, {
                "selector": "body.dark .header",
                "key": "border-bottom-color"
            }, {
                "selector": "body.dark .navigation-logo",
                "key": "border-bottom-color"
            }, {
                "selector": "body.dark hr",
                "key": "border-color"
            }, {
                "selector": "body.dark .page-header",
                "key": "border-bottom-color"
            }, {
                "selector": "body.dark .customizer .customizer-footer",
                "key": "border-color"
            }],
            "val": "#454c66"
        }, {
            "name": "text color",
            "group": "text_color",
            "identity": "text_color",
            "css_info": [{
                "selector": "body.dark .header",
                "key": "color"
            }, {
                "selector": ".table",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "header",
            "group": "header",
            "identity": "header_color",
            "css_info": [{
                "selector": "body.dark .header",
                "key": "background"
            }],
            "val": "#313852"
        }, {
            "name": "horizontal header",
            "group": "header",
            "identity": "horizontal_header_color",
            "css_info": [{
                "selector": "body.dark.hz_menu .header",
                "key": "background"
            }],
            "val": "#313852"
        }, {
            "name": "horizontal header text color",
            "group": "header",
            "identity": "horizontal_header_text_color",
            "css_info": [{
                "selector": "body.dark.hz_menu .hz_app_menu .app_item",
                "key": "color"
            }, {
                "selector": "body.dark.hz_menu .header .navbar-nav a",
                "key": "color"
            }],
            "val": "#fff"
        }, {
            "name": "horizon header",
            "group": "header",
            "identity": "header_color",
            "css_info": [{
                "selector": "body.dark.hz_menu .header",
                "key": "background"
            }],
            "val": "#313852"
        }, {
            "name": "page header",
            "group": "page_header",
            "identity": "page_header",
            "css_info": [{
                "selector": "body.dark page-header",
                "key": "background"
            }],
            "val": "#313852"
        }, {
            "name": "body",
            "group": "body",
            "identity": "body_color",
            "css_info": [{
                "selector": "body.dark",
                "key": "background"
            }, {
                "selector": "body.dark .o_action_manager",
                "key": "background"
            }],
            "val": "#1A233A"
        }, {
            "name": "footer",
            "group": "footer",
            "identity": "footer_color",
            "keys": "background",
            "css_info": [{
                "selector": "body.dark .page-footer",
                "key": "background"
            }],
            "val": "#313852"
        },  {
            "name": "button primary",
            "group": "button",
            "css_info": [{
                "selector": "body.dark .btn-primary",
                "key": "background"
            }],
            "val": "#273658"
        }, {
            "name": "button secondary",
            "group": "button",
            "css_info": [{
                "selector": "body.dark .btn-secondary",
                "key": "background"
            }],
            "val": "#4e545b"
        }, {
            "name": "customizer",
            "group": "customizer",
            "css_info": [{
                "selector": "body.dark .customizer",
                "key": "background"
            }],
            "val": "#272E48"
        }, {
            "name": "drop down",
            "group": "drop_down",
            "css_info": [{
                "selector": "body.dark .dropdown-menu",
                "key": "background"
            }, {
                "selector": "body.dark .fx_search_options",
                "key": "background"
            }],
            "val": "rgb(49, 56, 82)"
        }, {
            "name": "hover color",
            "group": "hover",
            "css_info": [{
                "selector": "body.dark .dropdown-menu .dropdown-item:hover",
                "key": "background"
            }],
            "val": "#313852"
        }, {
            "name": "tab pane",
            "group": "hover",
            "css_info": [{
                "selector": "body.dark .tab-pane",
                "key": "background"
            }],
            "val": "#313852"
        }]
    }]
}

default_modes = {
    "normal": normal_mode,
    "dark": dark_mode
}
