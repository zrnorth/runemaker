"""
Utility / helpers
"""
import os
import json
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
import riot_api

# Globals
SETUP = False
RUNE_DICT = {}
WEIGHTS = {}

def setup():
    """
    Get setup for calls, getting the api keys from the config file.
    """
    global SETUP, RUNE_DICT, WEIGHTS
    if not SETUP:
        data_location = os.path.realpath(os.path.join(__location__, "../data"))

        with open(os.path.join(data_location, 'rune_info.json'), 'r') as f:
            try:
                rune_list = json.load(f)
                convert_rune_list_to_dict(rune_list)
            except ValueError:
                RUNE_DICT = {}

        with open(os.path.join(data_location, 'weight_config.json'), 'r') as f:
            try:
                WEIGHTS = dict(json.load(f))
            except ValueError:
                WEIGHTS = {}

        SETUP = True

    
def convert_rune_list_to_dict(rune_list):
    """
    We want to take our list of all types of runes, and change it to a 
    dict with the rune id as a key.
    """
    for rune_type in rune_list:
        key = rune_type['id']
        del rune_type['id']
        value = rune_type
        RUNE_DICT[key] = value
    
def rune_group_shorthand(runeGroup):
    """
    Helper to put the runes into shorthand.
    input: json, ex: 
    {   'id': 5273,
        'description': '+0.87 magic penetration', 
        'name': 'Greater Mark of Magic Penetration', 
        'number': 9  }
        
    output: "9x Magic Pen Reds"
    
    """
    setup()
        
    id = runeGroup['id']
    num = runeGroup['number']
        
    str = "{0}x {1} {2}".format(num, RUNE_DICT[id]['stat'], RUNE_DICT[id]['type'])
    if num > 1:
        str += "s"
    return str

def get_defined_champ_role_weights():
    """
    Helper to get the defined score weights from the weight_config file.
    """
    setup()
    return WEIGHTS

