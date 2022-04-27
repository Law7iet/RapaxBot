import csv
from clanShips.clanShips import ClanShips

CLAN_ID = 500183314

clanShips = ClanShips()
playersMappedShips = clanShips.getPlayersShips(CLAN_ID)

# Check CVS header
filePrefix = 'clanShips/T'
for i in range(1, 12):
    fileName = filePrefix + str(i) + '.csv'
    with open(fileName, mode='w') as csv_file:
        # Setup header
        header = ['nickname']
        for ship_type in clanShips.ships_by_tier_and_type[str(i)]:
            for ship in clanShips.ships_by_tier_and_type[str(i)][ship_type]:
                header.append(ship['name'])
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)

        # Setup body
        for player in playersMappedShips:
            row = [player]
            for ship_type in playersMappedShips[player][str(i)]:
                if playersMappedShips[player][str(i)][ship_type] != []:
                    row.extend(playersMappedShips[player][str(i)][ship_type])         
            writer.writerow(row)