====================================
Odoo 13 template_widget, user widget in tree view
====================================

This Module will support widget in tree view and form view

Installation
==============================

To install this module, you need to:

Download the module and add it to your Odoo addons folder. Afterward, log on to
your Odoo server and go to the Apps menu. Trigger the debug mode and update the
list by clicking on the "Update Apps List" link. Now install the module by
clicking on the install button.

Upgrade
==============================

To upgrade this module, you need to:

Download the module and add it to your Odoo addons folder. Restart the server
and log on to your Odoo server. Select the Apps menu and upgrade the module by
clicking on the upgrade button.


Configuration
=============
use the fx_template_widget in tree view like this:
::

    <record model="ir.ui.view" id="template_widget.list">
        <field name="name">template_widget</field>
        <field name="model">template_widget.template_widget</field>
        <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <widget name="fx_template_widget"
                    options="{'template': 'example_buttons'}"/>
        </tree>
        </field>
    </record>

and yu must define the qweb template:
:: 

    <?xml version="1.0" encoding="UTF-8"?>
    <templates id="template" xml:space="preserve">
        <t t-name="example_buttons">
            <div>
                <span>here, define what yu like, and user the record data</span>
                <button name="change_name" type="object" class="btn btn-sm btn-success">
                    change_name
                </button>
                <button name="context_test" type="object" context="{'test_id':'123'}" class="btn btn-sm btn-warning">
                    context_test
                </button>
            </div>
        </t>
    </templates>

Credits
=======

Contributors
------------

* xun dao <2243879204@qq.com>


Author & Maintainer
-------------------

This module is maintained by the xun dao