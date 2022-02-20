import config
from utils import *
import csv

def get_ships_filter():
    return  {
        '1': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '2': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '3': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '4': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '5': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '6': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '7': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '8': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '9': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '10': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() }),
        '11': dict({ 'Destroyer': list(), 'Cruiser': list(), 'Battleship': list(), 'AirCarrier': list() })
    }

# Get all ships
def get_all_ships():
    # HashMap of all ships (hashed by ship_id)
    all_ships = {}
    # Object that contains all ships, divided by tier and type
    all_ships_ordered = get_ships_filter()
    # Number of page of the request
    page = 1
    while True:
        response_ships = check_data(URL_SHIPS + str(page))
        if response_ships['status'] != 'ok':
            break

        for ship_id in response_ships['data']:
            ship = {
                # 'id': ship_id,
                'name': response_ships['data'][str(ship_id)]['name'],
                'type': response_ships['data'][str(ship_id)]['type'],
                'tier': response_ships['data'][str(ship_id)]['tier'],
                'nation': response_ships['data'][str(ship_id)]['nation'],
                'is_special': response_ships['data'][str(ship_id)]['is_special'],
                'is_premium': response_ships['data'][str(ship_id)]['is_premium'],
                'index': None
            }
            # Remove "[ name ]" ship
            if response_ships['data'][str(ship_id)]['name'][0] != '[':
                all_ships[str(ship_id)] = ship
                all_ships_ordered[str(ship['tier'])][ship['type']].append({ 'id': ship_id , 'name': ship['name'] })

        page = page + 1
        if page > response_ships['meta']['page_total']:
            break
    
    # Sort and clear ships in all_ship_ordered
    for ship_tier in all_ships_ordered:
        for ship_type in all_ships_ordered[str(ship_tier)]:
            all_ships_ordered[str(ship_tier)][ship_type].sort(key=lambda d: d['name'])
            index = 0
            for ship in all_ships_ordered[str(ship_tier)][ship_type]:
                # Map the index of sorted ships in all_ships
                all_ships[ship['id']]['index'] = index
                index = index + 1
    
    return (all_ships, all_ships_ordered)

def get_player_filter(all_ships_ordered):
    all_ships_player = get_ships_filter()
    for tier_index in all_ships_ordered:
        for type_index in all_ships_ordered[tier_index]:
            for shipIndex in range(0, len(all_ships_ordered[tier_index][type_index])):
                all_ships_player[tier_index][type_index].append(False)
    return all_ships_player

def get_player_ships(all_ships_ordered):
    
    # returned dict
    mapped_list = {}
    # Request clan's members' ID
    response_clan_data = check_data(URL_CLAN_NAME + str(RAPAX_ID))

    # For each member
    for id in response_clan_data['data'][str(RAPAX_ID)]['members_ids']:
        try:
            response_nickname = check_data(URL_PLAYER_NICKNAME + str(id))
            player_nickname = response_nickname['data'][str(id)]['nickname']
            mapped_ships = get_player_filter(all_ships_ordered)
            # Get member's ships
            response_member_data = check_data(URL_PLAYER_SHIPS + str(id))
            # For each member's ship
            for element in response_member_data['data'][str(id)]:
                # Old ship has an id but is not in all_ships
                try:
                    # map the player's ship
                    ship = all_ships[str(element['ship_id'])]
                    mapped_ships[str(ship['tier'])][ship['type']][ship['index']] = True
                except:
                    pass
        except:
            pass
        
        mapped_list[player_nickname] = mapped_ships
    return mapped_list

# MAIN

(all_ships, all_ships_ordered) = get_all_ships()
players_mapped_ships = get_player_ships(all_ships_ordered)

# Check CVS header
filePrefix = 'stats/T'
for i in range(1, 12):
    fileName = filePrefix + str(i) + '.csv'
    with open(fileName, mode='w') as csv_file:
        # Setup header
        header = ['nickname']
        for ship_type in all_ships_ordered[str(i)]:
            for ship in all_ships_ordered[str(i)][ship_type]:
                header.append(ship['name'])
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)

        # Setup body
        
        for player in players_mapped_ships:
            row = [player]
            for ship_type in players_mapped_ships[player][str(i)]:
                if players_mapped_ships[player][str(i)][ship_type] != []:
                    row.extend(players_mapped_ships[player][str(i)][ship_type])         
            writer.writerow(row)
        