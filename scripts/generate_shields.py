#!/usr/bin/env python

# generate highway shields

from __future__ import print_function
import copy, lxml.etree, os

def main():

  namespace = 'http://www.w3.org/2000/svg'
  svgns = '{' + namespace + '}'
  svgnsmap = {None: namespace}

  config = {}
  config['base'] = {}

  config['base']['rounded_corners'] = 2
  config['base']['font_height'] = 9
  config['base']['font_width'] = 7
  config['base']['padding_x'] = 3
  config['base']['padding_y'] = 2
  config['base']['fill'] = '#ddd'
  config['base']['stroke_width'] = 1
  config['base']['stroke_fill'] = '#000'

  config['global'] = {}

  config['global']['types'] = ['motorway', 'trunk', 'primary', 'secondary', 'tertiary']
  config['global']['max_width'] = 11
  config['global']['max_height'] = 4
  config['global']['output_dir'] = '../symbols/shields/' # specified relative to the script location

  # specific values overwrite config['base'] ones
  config['motorway'] = {}
  config['motorway']['fill'] = '#cc7887' # Lch(60,35,10) based on Lch(70,35,10)
  config['motorway']['stroke_fill'] = '#b05f6e' # Lch(50,35,10)

  config['trunk'] = {}
  config['trunk']['fill'] = '#df9782' # Lch(69,33,42) based on Lch(79,33,42)
  config['trunk']['stroke_fill'] = '#c27d69' # Lch(59,33,42)

  config['primary'] = {}
  config['primary']['fill'] = '#d5ac7d' # Lch(73,31,74) based on Lch(88,31,74)
  config['primary']['stroke_fill'] = '#b89264' # Lch(63,31,74)

  config['secondary'] = {}
  config['secondary']['fill'] = '#d1cf97' # Lch(82,29,106) based on Lch(97,29,106)
  config['secondary']['stroke_fill'] = '#b5b37d' # Lch(72,29,106)

  config['tertiary'] = {}
  config['tertiary']['fill'] = '#c6c6c6' # Lch(80,0,0) based on Lch(100,0,0)
  config['tertiary']['stroke_fill'] = '#ababab' # Lch(70,0,0)


  if not os.path.exists(os.path.dirname(config['global']['output_dir'])):
    os.makedirs(os.path.dirname(config['global']['output_dir']))

  for height in range(1, config['global']['max_height'] + 1):
    for width in range(1, config['global']['max_width'] + 1):
      for shield_type in config['global']['types']:

        # merge base config and specific styles
        vars = copy.deepcopy(config['base'])
        if shield_type in config:
          for option in config[shield_type]:
            vars[option] = config[shield_type][option]

        shield_width = 2 * vars['padding_x'] + vars['font_width'] * width
        shield_height = 2 * vars['padding_y'] + vars['font_height'] * height

        svg = lxml.etree.Element('svg', nsmap=svgnsmap)
        svg.set('width', '100%')
        svg.set('height', '100%')
        svg.set('viewBox', '0 0 ' + str(shield_width  + vars['stroke_width']) + ' ' + str(shield_height + vars['stroke_width']))

        if vars['stroke_width'] > 0:
          offset_x = vars['stroke_width'] / 2.0
          offset_y = vars['stroke_width'] / 2.0
        else:
          offset_x = 0
          offset_y = 0

        shield = lxml.etree.Element(svgns + 'rect')
        shield.set('x', str(offset_x))
        shield.set('y', str(offset_y))
        shield.set('width', str(shield_width))
        shield.set('height', str(shield_height))
        if vars['rounded_corners'] > 0:
          shield.set('rx', str(vars['rounded_corners']))
          shield.set('ry', str(vars['rounded_corners']))
        shield.set('id', 'shield')

        stroke = ''
        if vars['stroke_width'] > 0:
          stroke = 'stroke:' + vars['stroke_fill'] + ';stroke-width:' + str(vars['stroke_width']) + ';'

        shield.set('style', 'fill:' + vars['fill'] + ';' + stroke)

        svg.append(shield)

        filename = shield_type + '_' + str(width) + 'x' + str(height) + '.svg'

        # save file
        try:
          shieldfile = open(os.path.join(os.path.dirname(__file__), config['global']['output_dir'] + filename), 'w')
          shieldfile.write(lxml.etree.tostring(svg, encoding='utf-8', xml_declaration=True, pretty_print=True))
          shieldfile.close()
        except IOError:
          print('Could not save file ' + filename + '.')
          continue

if __name__ == "__main__": main()
