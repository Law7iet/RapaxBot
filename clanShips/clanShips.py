from utils.apiWarGaming import ApiWarGaming
from utils.constants import *
from utils.functions import *

class ClanShips:
    def __init__(self):
        self.apiWarGaming = ApiWarGaming()
        self.shipsById = {}
        """
        It's a dictionary that stores all ships by their ID.
        The key is the ship ID and the value is a ship.
        Each ship is a dictionary that contains:
            `name` (str)\n
            `type` (ShipsTypeEnum)\n
            `tier` (ShipsTierEnum)\n
            `nation` (str)              not used\n
            `is_special` (bool)         not used\n
            `is_premium` (bool)         not used\n
        """        
        self.shipsByTierAndType = self.getShipsTable()
        """
        It's a dictionary that stores all ships by tier and type.
        The key is the ships tier and the value is a sub-dictionary that keys are the ships' type.
        The sub-dictionary value is a list of ships.
        Each ships is a dictionary that contains:
            `id` (str)\n
            `name` (str)
        """        
        self.setAllShips() 

    def getShipsTable(self) -> dict:
        '''
        Get an empty `dict` divided by ships tier.
        Each tier has a own `dict` divided by type of ships.
        Each type of ships is a `list`.

        Returns:
            `dict`: the empty structure to contains ships.
        '''        
        return  {
            str(int(ShipsTierEnum.ONE))     : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.TWO))     : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.THREE))   : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.FOUR))    : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.FIVE))    : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.SIX))     : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.SEVEN))   : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.EIGHT))   : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.NINE))    : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.TEN))     : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() }),
            str(int(ShipsTierEnum.ELEVEN))  : dict({ shipsType[ShipsTypeEnum.DESTROYER]: list(), shipsType[ShipsTypeEnum.CRUISER]: list(), shipsType[ShipsTypeEnum.BATTLESHIP]: list(), shipsType[ShipsTypeEnum.AIR_CARRIER]: list() })
        }

    def setAllShips(self) -> None:
        """
        Initialize `shipsById` and `shipsByTierAndType` dictionary.\n
        
        Each ships in `shipsByTierAndType` is a dictionary that contains:
            `id` (str)\n
            `name` (str)

        Returns:
            `None`
        """
        responseShips = self.apiWarGaming.getShips()
        if responseShips == []:
            return None
        for shipElement in responseShips:
            shipId = shipElement[0]
            shipElement = shipElement[1]
            if shipElement['tier'] == 1:
                tier = ShipsTierEnum.ONE
            elif shipElement['tier'] == 2:
                tier = ShipsTierEnum.TWO
            elif shipElement['tier'] == 3:
                tier = ShipsTierEnum.THREE
            elif shipElement['tier'] == 4:
                tier = ShipsTierEnum.FOUR
            elif shipElement['tier'] == 5:
                tier = ShipsTierEnum.FIVE
            elif shipElement['tier'] == 6:
                tier = ShipsTierEnum.SIX
            elif shipElement['tier'] == 7:
                tier = ShipsTierEnum.SEVEN
            elif shipElement['tier'] == 8:
                tier = ShipsTierEnum.EIGHT
            elif shipElement['tier'] == 9:
                tier = ShipsTierEnum.NINE
            elif shipElement['tier'] == 10:
                tier = ShipsTierEnum.TEN
            elif shipElement['tier'] == 11:
                tier = ShipsTierEnum.ELEVEN
            else:
                return None
                
            if shipElement['type'] == 'Destroyer':
                type = ShipsTypeEnum.DESTROYER
            elif shipElement['type'] == 'Cruiser':
                type = ShipsTypeEnum.CRUISER
            elif shipElement['type'] == 'Battleship':
                type = ShipsTypeEnum.BATTLESHIP
            elif shipElement['type'] == 'AirCarrier':
                type = ShipsTypeEnum.AIR_CARRIER
            elif shipElement['type'] == 'Submarine':
                type = ShipsTypeEnum.SUBMARINE
            else:
                return None
            
            ship = {
                'id': shipId,
                'name': shipElement['name'],
                'type': type,
                'tier': tier,
                'nation': shipElement['nation'],
                'is_special': shipElement['is_special'],
                'is_premium': shipElement['is_premium']
            }
            # Remove "[ name ]" ship
            if shipElement['name'][0] != '[':
                self.shipsById[str(shipElement['ship_id'])] = ship
                self.shipsByTierAndType[str(int(ship['tier']))][shipsType[int(ship['type'])]].append({ 'id': shipId, 'name': ship['name'] })

        # Sort and clear ships in all_ship_ordered
        for shipTier in self.shipsByTierAndType:
            for shipType in self.shipsByTierAndType[str(shipTier)]:
                self.shipsByTierAndType[str(shipTier)][shipType].sort(key=lambda d: d['name'])
                index = 0
                for ship in self.shipsByTierAndType[str(shipTier)][shipType]:
                    # Map the index of sorted ships in all_ships
                    self.shipsById[ship['id']]['index'] = index
                    index = index + 1

    def getPlayerTable(self) -> dict:
        """
        Returns the `dict` `shipsByTierAndType` filled with `False` for each ship.

        Returns:
            `dict`: the table
        """        
        playerTable = self.getShipsTable()
        for tierIndex in self.shipsByTierAndType:
            for typeIndex in self.shipsByTierAndType[tierIndex]:
                for shipIndex in range(0, len(self.shipsByTierAndType[tierIndex][typeIndex])):
                    playerTable[tierIndex][typeIndex].append(False)

        return playerTable

    def getPlayersShips(self, clanId: int) -> dict:
        """
        Generate a dict where's stored the ships played by each member of the clan passed by ID.
        The key is the player nickname, and the value is a dictionary divided by tier and type, where the final value is a list of a specific tier and specific type.
        This list is a boolean list and means if the player has a specific ships.

        Args:
            clanId (int): the clan ID.

        Returns:
            `dict`: the dictionary with all players' ships.
        """        
        # returned dict
        mappedList = {}
        # Request clan's members' ID
        responseClanDetails = self.apiWarGaming.getClanMembers(clanId)
        if responseClanDetails == []:
            return mappedList

        # For each member
        for id in responseClanDetails:
            try:
                response = self.apiWarGaming.getPlayerById(str(id))
                if response == None:
                    continue
                playerNickname = response[1]
                mappedShips = self.getPlayerTable()
                # Get member's ships
                responseMemberShips = self.apiWarGaming.getPlayerShips(str(id))
                if responseMemberShips == []:
                    continue
                # For each member's ship
                for shipId in responseMemberShips:
                    # Old ship has an id but is not in all_ships
                    try:
                        # map the player's ship
                        ship = self.shipsById[str(shipId)]
                        mappedShips[str(int(ship['tier']))][shipsType[int(ship['type'])]][ship['index']] = True
                    except:
                        pass
            except:
                pass
            
            mappedList[playerNickname] = mappedShips
        return mappedList