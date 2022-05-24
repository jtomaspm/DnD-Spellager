


ImmutableMultiDict(
    [
        ('name', 'dfghdghd'), 
        ('level', 'dghgf'), 
        ('school', 'dfghdgfh'), 
        ('casting_time', 'dfghdfhdf'), 
        ('range', 'dghdgfhdf'), 
        ('components', 'dgfhdfh'), 
        ('duration', 'dgfhdfh'), 
        ('ritual', 'on'), 
        ('concentration', 'on'), 
        ('damage', 'dghd'), 
        ('damage_type', 'dghdgf'), 
        ('heal_at_slot_level', 'dghgdfhhf'),
        ('dc', 'dgfhfhdgfh'), 
        ('aoe_size', 'dfhgdfh'), 
        ('aoe_type', 'dfghdfgh'), 
        ('material', 'dfhgdfhd'), 
        ('classes', 'dghdfghf'), 
        ('desc', 'hfdghdfh'), 
        ('higher_level', 'dgfhdfhdf')
        ]
        )

        
"""
'dc': {
    'dc_type': {
        'index': 'str', 
        'name': 'STR', 
        'url': '/api/ability-scores/str'
        }, 
    'dc_success': 'none'
} 
'area_of_effect': {
    'type': 'cube', 
    'size': 20
},
"""




{
    'damage': 
    {
        'damage_type': 
        {
            'index': 'fire', 
            'name': 'Fire', 
            'url': '/api/damage-types/fire'
        }, 
        'damage_at_slot_level':
        {
            '2': '3d6', 
            '4': '4d6', 
            '6': '5d6', 
            '8': '6d6'
        }
    }
}

template = {
        '_id': '626eb50cb264cb21bf5070a1', 
        'higher_level': [

            ], 
        'index': 'shillelagh', 
        'name': 'Shillelagh', 
        'desc': [
            "The wood of a club or a quarterstaff you are holding is imbued with nature's power. For the duration, you can use your spellcasting ability instead of Strength for the attack and damage rolls of melee attacks using that weapon, and the weapon's damage die becomes a d8. The weapon also becomes magical, if it isn't already. The spell ends if you cast it again or if you let go of the weapon."
            ], 
        'range': 'Touch', 
        'components': [
            'V', 
            'S', 
            'M'
            ], 
        'material': 'Mistletoe, a shamrock leaf, and a club or quarterstaff.', 
        'ritual': False, 
        'duration': '1 minute', 
        'concentration': False, 
        'casting_time': '1 bonus action', 
        'level': 0, 
        'school': {
            'index': 'transmutation', 
            'name': 'Transmutation', 
            'url': '/api/magic-schools/transmutation'
            }, 
        'classes': [
            {
                'index': 'druid',
                'name': 'Druid',
                'url': '/api/classes/druid'
                }
            ],
            'subclasses': [
                {
                    'index': 'lore',
                    'name': 'Lore',
                    'url': '/api/subclasses/lore'
                    }
                ], 
            'url': '/api/spells/shillelagh'
            }



"""
Shillelagh
Druidcraft
Guidance
Burning Hands
Cure Wounds
Silvery Barbs
Speak with Animals
Healing Word
Entangle
Goodberry
Faerie Fire
Absorb Elements
Detect Magic
Detect Poison and Disease
Flaming Sphere
Scorching Ray
Misty Step
Enhance Ability
Moonbeam
Spike Growth
Pass without Trace
Healing Spirit
Enlarge/Reduce
Flame Blade
Aid
Plant Growth
Speak with Plants
"""