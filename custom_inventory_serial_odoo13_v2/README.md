# Custom Inventory Serial Prefix - Odoo 13

Separate fields are provided exactly as requested:

Product:
- Product Test Code: x

Location:
- Building Code: N
- Floor Code: F
- Hall Code: 5
- Location Prefix: NF5

Generated serial:
NF5x0001

Important:
- The fields are separate; Location Prefix is computed from Building + Floor + Hall.
- Existing lot/serial values are not overwritten.
- The sample implementation generates a serial after a picking reaches done.
- For production use, the serial allocator should be made concurrency-safe with a dedicated sequence/locking strategy if multiple users can validate transfers simultaneously.
