# Custom Inventory Serial Prefix - Odoo 13

## Features

1. Adds `Product Prefix Code` to `product.template`.
2. Adds `Prefix Code` to `stock.location`.
3. Builds a location prefix from the complete parent location path.
4. Generates serial numbers for serial-tracked products on internal transfer validation.
5. Serial format: `<location path prefix><product prefix><4-digit sequence>`.
6. Example: location prefixes N + F + 5 and product prefix x => `NF5x0001`.
7. Provides a Purchase Order Excel import wizard.
8. Provides a downloadable Excel template.
9. Adds a contextual server action `Generate Prefix Serials` on stock pickings.

## Important Odoo 13 behavior

Serial-tracked products normally require a serial number during stock validation. Therefore,
the module generates the missing serial in `stock.picking.button_validate()` before calling
the standard Odoo validation. This is safer than trying to add a lot to a completed move.

The server action is provided for manual repair/processing, but it does not overwrite an
existing serial number.

## Installation

1. Copy `custom_inventory_serial` to the Odoo 13 addons path.
2. Install the Python dependency:

   `pip3 install openpyxl`

3. Restart Odoo.
4. Update Apps list.
5. Install **Custom Inventory Serial Prefix**.

## Configuration

### Product
Open Inventory/Sales/Purchase product and set:

- Tracking = By Unique Serial Number
- Product Prefix Code = e.g. `x`

### Location
Set prefixes on the hierarchy:

- Building N -> `N`
- Floor F -> `F`
- Hall 5 -> `5`

The Hall location's calculated prefix becomes `NF5`.

### Internal transfer
When the internal transfer is validated, missing serials are generated as:

- `NF5x0001`
- `NF5x0002`
- `NF5x0003`

Existing serials are never overwritten.

## PO Excel import

Open a draft/sent Purchase Order and click **Import Excel Lines**.

Columns:

- Product (required)
- Internal Reference (optional)
- Quantity
- UoM
- Unit Price
- Taxes (comma separated tax names)
- Description

Product lookup first uses Internal Reference, then exact product name, then a case-insensitive
name search.

## Production notes

Test the module on a staging database first. Take a database backup before installing on live.
Validate serial tracking, multi-company behavior, routes, reservations, backorders and return
flows against your actual Odoo 13 configuration before production use.
