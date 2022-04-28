import csv
from clanShips.clanShips import ClanShips

CLAN_ID = 500183314

clan_ships = ClanShips()
players_mapped_ships = clan_ships.get_players_ships(CLAN_ID)

# Check CVS header
file_prefix = 'clanShips/T'
for i in range(1, 12):
    file_name = file_prefix + str(i) + '.csv'
    with open(file_name, mode='w') as csv_file:
        # Setup header
        header = ['nickname']
        for ship_type in clan_ships.ships_by_tier_and_type[str(i)]:
            for ship in clan_ships.ships_by_tier_and_type[str(i)][ship_type]:
                header.append(ship['name'])
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)

        # Setup body
        for player in players_mapped_ships:
            row = [player]
            for ship_type in players_mapped_ships[player][str(i)]:
                if players_mapped_ships[player][str(i)][ship_type]:
                    row.extend(players_mapped_ships[player][str(i)][ship_type])
            writer.writerow(row)
