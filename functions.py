import requests
import json

api_url = 'https://www.dnd5eapi.co/api/spells/'

def get_json_from_api(id):
    r = requests.get(api_url + id)

    if r.status_code == 200:
        res = r.json()
        print(res)
        return res
    else:
        print('Error fetching from api '+id)
        return None

def id_to_name(id):
    return id.replace('-', ' ').title()

def name_to_id(name):
    return name.lower().replace(' ', '-')

def query_for_spells(Spell, db, spell_names, username, Assoc):
    not_found = []
    found = []
    for spell_name in spell_names:
        #check db
        index = name_to_id(spell_name)
        spell = Spell.query.filter_by(index=index).first()
        if not spell:
            #check 5e api
            spell_json = get_json_from_api(index)
            if spell_json:
                spell = Spell(index=index, name=spell_json['name'], json=json.dumps(spell_json))
                db.session.add(spell)
                db.session.commit()
        if spell:
            found.append(spell.index)
            if not Assoc.query.filter_by(username=username, index=index).first():
                new_assoc = Assoc(username=username, index=index)
                db.session.add(new_assoc)
                db.session.commit()
        else:
            not_found.append(index)
    return {
        'found' : found,
        'not_found' : not_found
    }


def new_manual_spell(Spell, Assoc, db, form, username):
    spell_json = {}

    if form.get('name'):
        spell_json['name'] = id_to_name(form.get('name'))

    if form.get('name'):
        spell_json['index'] = name_to_id(form.get('name'))

    if form.get('level'):
        spell_json['level'] = form.get('level')

    if form.get('school'):
        spell_json['school'] = {
            'index': form.get('school').lower(), 
            'name': form.get('school').title(), 
            'url': '/api/magic-schools/' + form.get('school').lower()
        }

    if form.get('casting_time'):
        spell_json['casting_time'] = form.get('casting_time')

    if form.get('range'):
        spell_json['range'] = form.get('range')

    if form.get('components'):
        spell_json['components'] = [c.strip() for c in form.get('components').split(',')]

    if form.get('duration'):
        spell_json['duration'] = form.get('duration')

    if form.get('ritual'):
        spell_json['ritual'] = True

    if form.get('concentration'):
        spell_json['concentration'] = True

    if form.get('damage') or form.get('damage_type'):
        spell_json['damage'] = {}

    if form.get('damage'):
        spell_json['damage']['damage_at_slot_level'] = {spell_json['level'] : form.get('damage')}

    if form.get('damage_type'):
        spell_json['damage']['damage_type'] = {'index' : form.get('damage_type').lower(), 'name' : form.get('damage_type').title(), 'url': '/api/damage-types/'+form.get('damage_type').lower()}

    if form.get('heal_at_slot_level'):
        spell_json['heal_at_slot_level'] = form.get('heal_at_slot_level')

    if form.get('dc'):
        spell_json['dc'] = {
                            'dc_type': {
                                'index': form.get('dc').lower(), 
                                'name': form.get('dc'), 
                                'url': '/api/ability-scores/'+form.get('dc').lower(),
                                }, 
                            'dc_success': 'none'
                            } 

    if form.get('aoe_size') or form.get('aoe_type'):
        spell_json['area_of_effect'] = {}

    if form.get('aoe_size'):
        spell_json['area_of_effect']['size'] = form.get('aoe_size')

    if form.get('aoe_type'):
        spell_json['area_of_effect']['type'] = form.get('aoe_type')

    if form.get('material'):
        spell_json['material'] = form.get('material')

    if form.get('classes'):
        spell_json['classes'] = [
            {'index': c.strip().lower(),
            'name': c.strip().title(),
            'url': '/api/classes/'+c.strip().lower()} for c in form.get('classes').split(',') 
            ]

    if form.get('desc'):
        spell_json['desc'] = [form.get('desc')]

    if form.get('higher_level'):
        spell_json['higher_level'] = form.get('higher_level')

    print('------------------ SPELL JSON ----------------------')
    print(spell_json)

    new_spell = Spell(index=spell_json['index'], name=spell_json['name'], json=json.dumps(spell_json))
    db.session.add(new_spell)
    db.session.commit()

    new_assoc = Assoc(username=username, index=spell_json['index'])
    db.session.add(new_assoc)
    db.session.commit()

    return new_spell



#SORTING
