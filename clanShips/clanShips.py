from utils.apiWarGaming import ApiWarGaming
from utils.constants import *


def get_ships_table() -> dict:
    """
    Get an empty `dict` divided by ships tier.
    Each tier has an own `dict` divided by type of ships.
    Each type of ships is a `list`.

    Returns:
        `dict`: the empty structure to contains ships.
    """
    return {
        str(int(ShipsTierEnum.ONE)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.TWO)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.THREE)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.FOUR)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.FIVE)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.SIX)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.SEVEN)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.EIGHT)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.NINE)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.TEN)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        ),
        str(int(ShipsTierEnum.ELEVEN)): dict(
            {
                shipsType[ShipsTypeEnum.DESTROYER]: list(),
                shipsType[ShipsTypeEnum.CRUISER]: list(),
                shipsType[ShipsTypeEnum.BATTLESHIP]: list(),
                shipsType[ShipsTypeEnum.AIR_CARRIER]: list()
            }
        )
    }


class ClanShips:
    def __init__(self):
        self.api_wargaming = ApiWarGaming()
        self.ships_by_id = {}
        """
        It's a dictionary that stores all ships by their ID.
        The key is the ship ID and the value is a ship.
        Each ship is a dictionary that contains:
            `name`          (str)\n
            `type`          (ShipsTypeEnum)\n
            `tier`          (ShipsTierEnum)\n
            `nation`        (str)               not used\n
            `is_special`    (bool)              not used\n
            `is_premium`    (bool)              not used\n
        """
        self.ships_by_tier_and_type = get_ships_table()
        """
        It's a dictionary that stores all ships by tier and type.
        The key is the ships tier and the value is a sub-dictionary that keys are the ships' type.
        The sub-dictionary value is a list of ships.
        Each ships is a dictionary that contains:
            `id` (str)\n
            `name` (str)
        """
        self.set_all_ships()

    def set_all_ships(self) -> None:
        """
        Initialize `ships_by_id` and `ships_by_tier_and_type` dictionary.\n
        
        Each ships in `ships_by_tier_and_type` is a dictionary that contains:
            `id`    (str)\n
            `name`  (str)

        Returns:
            None
        """
        response_ships = self.api_wargaming.get_ships()
        if not response_ships:
            return None
        for ship_element in response_ships:
            ship_id = ship_element[0]
            ship_element = ship_element[1]
            if ship_element['tier'] == 1:
                tier = ShipsTierEnum.ONE
            elif ship_element['tier'] == 2:
                tier = ShipsTierEnum.TWO
            elif ship_element['tier'] == 3:
                tier = ShipsTierEnum.THREE
            elif ship_element['tier'] == 4:
                tier = ShipsTierEnum.FOUR
            elif ship_element['tier'] == 5:
                tier = ShipsTierEnum.FIVE
            elif ship_element['tier'] == 6:
                tier = ShipsTierEnum.SIX
            elif ship_element['tier'] == 7:
                tier = ShipsTierEnum.SEVEN
            elif ship_element['tier'] == 8:
                tier = ShipsTierEnum.EIGHT
            elif ship_element['tier'] == 9:
                tier = ShipsTierEnum.NINE
            elif ship_element['tier'] == 10:
                tier = ShipsTierEnum.TEN
            elif ship_element['tier'] == 11:
                tier = ShipsTierEnum.ELEVEN
            else:
                return None

            if ship_element['type'] == 'Destroyer':
                ships_type = ShipsTypeEnum.DESTROYER
            elif ship_element['type'] == 'Cruiser':
                ships_type = ShipsTypeEnum.CRUISER
            elif ship_element['type'] == 'Battleship':
                ships_type = ShipsTypeEnum.BATTLESHIP
            elif ship_element['type'] == 'AirCarrier':
                ships_type = ShipsTypeEnum.AIR_CARRIER
            elif ship_element['type'] == 'Submarine':
                ships_type = ShipsTypeEnum.SUBMARINE
            else:
                return None

            ship = {
                'id': ship_id,
                'name': ship_element['name'],
                'type': ships_type,
                'tier': tier,
                'nation': ship_element['nation'],
                'is_special': ship_element['is_special'],
                'is_premium': ship_element['is_premium']
            }
            # Remove "[ name ]" ship
            if ship_element['name'][0] != '[':
                self.ships_by_id[str(ship_element['ship_id'])] = ship
                self.ships_by_tier_and_type[str(int(ship['tier']))][shipsType[int(ship['type'])]].append(
                    {'id': ship_id, 'name': ship['name']})

        # Sort and clear ships in all_ship_ordered
        for ship_tier in self.ships_by_tier_and_type:
            for ship_type in self.ships_by_tier_and_type[str(ship_tier)]:
                self.ships_by_tier_and_type[str(ship_tier)][ship_type].sort(key=lambda d: d['name'])
                index = 0
                for ship in self.ships_by_tier_and_type[str(ship_tier)][ship_type]:
                    # Map the index of sorted ships in all_ships
                    self.ships_by_id[ship['id']]['index'] = index
                    index = index + 1

    def get_player_table(self) -> dict:
        """
        Returns the `dict` `ships_by_tier_and_type` filled with `False` for each ship.

        Returns:
            the table
        """
        player_table = get_ships_table()
        for tier_index in self.ships_by_tier_and_type:
            for type_index in self.ships_by_tier_and_type[tier_index]:
                for ship_index in range(0, len(self.ships_by_tier_and_type[tier_index][type_index])):
                    player_table[tier_index][type_index].append(False)

        return player_table

    def get_players_ships(self, clanId: int) -> dict:
        """
        Generate a dict where's stored the ships played by each member of the clan passed by ID.
        The key is the player nickname, and the value is a dictionary divided by tier and type, where the final value is a list of a specific tier and specific type.
        This list is a boolean list and means if the player has a specific ships.

        Args:
            clanId: the clan ID.

        Returns:
            the dictionary with all players' ships.
        """
        # returned dict
        mapped_list = {}
        # Request clan's members' ID
        response_clan_details = self.api_wargaming.get_clan_members(clanId)
        if not response_clan_details:
            return mapped_list

        # For each member
        for member_id in response_clan_details:
            try:
                response = self.api_wargaming.get_player_by_id(str(member_id))
                if response is None:
                    continue
                player_nickname = response[1]
                mapped_ships = self.get_player_table()
                # Get member's ships
                response_member_ships = self.api_wargaming.get_player_ships(str(member_id))
                if not response_member_ships:
                    continue
                # For each member's ship
                for shipId in response_member_ships:
                    # Old ship has a member_id but is not in all_ships
                    try:
                        # map the player's ship
                        ship = self.ships_by_id[str(shipId)]
                        mapped_ships[str(int(ship['tier']))][shipsType[int(ship['type'])]][ship['index']] = True
                    except:
                        pass
            except:
                pass

            mapped_list[player_nickname] = mapped_ships
        return mapped_list
