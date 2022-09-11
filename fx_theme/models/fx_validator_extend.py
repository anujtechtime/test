# -*- coding: utf-8 -*-

from odoo import tools
from odoo.tools import view_validation
from odoo.tools.view_validation import validate
from lxml import etree
import logging

_relaxng_cache = view_validation._relaxng_cache

_logger = logging.getLogger(__name__)

_relaxng_cache['tree'] = None
with tools.file_open('addons/base/rng/tree_view.rng') as frng:
    try:
        text = frng.read()
        with tools.file_open('addons/base/rng/common.rng') as common_rng:
            common_txt = common_rng.read()
            start_pos = common_txt.find('<rng:grammar')
            start_pos = common_txt.find('>', start_pos)
            end_pos = common_txt.find('</rng:grammar>')
            common_content = common_txt[start_pos + 1: end_pos]
            common_include = '<rng:include href=\"common.rng\"/>'
            import_pos = text.find(common_include)
            if import_pos != -1:
                text = text.replace(common_include, common_content + '''
                    <rng:define name="widget">
                        <rng:element name="widget">
                            <rng:attribute name="name" />
                            <rng:attribute name="options"/>
                        </rng:element>
                    </rng:define>
                ''')
            text = text.replace('<rng:ref name=\"html\"/>',
                                '<rng:ref name=\"widget\"/><rng:ref name=\"html\"/>')
        tmp_doc = etree.fromstring(text.encode('utf-8'))
        _relaxng_cache['tree'] = etree.RelaxNG(tmp_doc)
    except Exception as error:
        _logger.exception('Failed to load RelaxNG XML schema for views validation, {error}'.format(
            error=error))
        _relaxng_cache['tree'] = None

# remove the old validation
for index, pred in enumerate(view_validation._validators['tree']):
    if pred.__name__ == 'valid_field_in_tree':
        view_validation._validators['tree'].pop(index)
        break

@validate('tree')
def valid_field_in_tree_extend(arch, **kwargs):
    """ Children of ``tree`` view must be ``field`` or ``button`` or ``control``."""
    return all(
        child.tag in ('field', 'button', 'control', 'widget')
        for child in arch.xpath('/tree/*')
    )
