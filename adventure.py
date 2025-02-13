'''
Week 4 Coding Assignment: The Inventory and the Dungeon of Choices
'''

import random

def display_player_status(player_health):
    """Displays the player's current health"""
    print(f"Your current health: {player_health}")

def handle_path_choice(player_health):
    """Randomly chooses the left or right path and applies the corresponding health effects"""
    path_choice = random.choice(["left", "right"])
    if path_choice == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_health = player_health + 10
        player_health = min(player_health, 100)
    elif path_choice == "right":
        print("You fall into a pit and lose 15 health points.")
        player_health = player_health - 15
        if player_health < 0:
            player_health = 0
            print("You are barely alive!")
    return player_health

def player_attack(monster_health):
    """Changes the monster's health after the player attacks it"""
    monster_health = monster_health - 15
    print("You strike the monster for 15 damage!")
    return monster_health

def monster_attack(player_health):
    """Changes the player's health based on whether the monster lands a critical hit or not"""
    critical_hit = random.random()
    if critical_hit < 0.5:
        player_health = player_health - 20
        print("The monster lands a critical hit for 20 damage!")
    else:
        player_health = player_health - 10
        print("The monster hits you for 10 damage!")
    return player_health

def acquire_item(inventory, item):
    """Allows for items to be added to the inventory, whether single items or lists of items"""
    if not item:
        print("You found nothing.")
    else:
        inventory.append(item) #Operation 1: "Append" used to add single item to inventory
        print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """Shows the player what is in their inventory or if it is empty"""
    if inventory == [ ]:
        print("Your inventory is empty.")
    else:
        print("Your inventory:") #Prints header once
        for index, item in enumerate(inventory):
            print(f"{index + 1}. {item}") #Prints numbered list of each item on a newline

def use_item(inventory):
    """Allows player to try and fail to use the spell book, then discards it from the inventory"""
    if "spell book" in inventory: #Operation 2:"In" checks if spell book is within the inventory
        inventory.remove("spell book") #Operation 3: "Remove" discards spell book from inventory
        print("You opened the spell book but could not read its language, so you discarded it.")
    return inventory

def combat_encounter(player_health, monster_health, has_treasure):
    """Describes combat encounters: player and then monster take turns attacking
    each other and health values update, a win or loss is determined at the end"""
    if monster_health <= 0:
        return False
    while player_health > 0 and monster_health > 0:
        #Player's turn
        monster_health = player_attack(monster_health)
        display_player_status(player_health)

        #Monster's turn
        player_health = monster_attack(player_health)

    #Win/Loss check
    if player_health <= 0:
        print("Game Over!")
        return False
    if monster_health <= 0:
        print("You defeated the monster!")
        if has_treasure:
            return True
        else:
            return False

def check_for_treasure(has_treasure):
    """Checking if the monster had treasure"""
    if has_treasure:
        print("You found the hidden treasure! You win!")
    else:
        print("The monster did not have the treasure. You continue your journey.")

def enter_dungeon(player_health, inventory, dungeon_rooms):
    """Takes player through each of the dungeon rooms"""
    for room in dungeon_rooms:
        print(f"You enter a {room[0]}!")
        if room[1] is not None:
            print(f"You found a {room[1]} in the room.")
            acquire_item(inventory, room[1])

        if room[2] == "trap": #Path if the player enters the lava trap room
            print("You see a potential trap!")
            trap_choice = input("Disarm or bypass the trap?")
            if trap_choice == "disarm": #If the player attempts to disarm the trap
                success = random.choice([True, False])
                if success:
                    print(f"{room[3][0]}")
                    player_health = player_health + room[3][2]
                    if player_health < 0:
                        player_health = 0
                        print("You are barely alive!")
                else:
                    print(f"{room[3][1]}")
                    player_health = player_health + room[3][2]
                    if player_health <= 0:
                        print("Oh no, you have died!")
                    return player_health, inventory
            else: #If the player chooses to bypass the trap
                success = random.choice([True, False, False])
                if success:
                    print("You gained nothing, move on.")
                else:
                    print(f"{room[3][1]}")
                    player_health = player_health + room[3][2]
                    if player_health <= 0:
                        print("Oh no, you have died!")
                    return player_health, inventory
                display_inventory(inventory)

        elif room[2] == "puzzle": #Path if the player enters the chest puzzle room
            print("You encounter a puzzle!")
            puzzle_choice = input("Solve or skip?")
            if puzzle_choice == "solve": #Path if the player attempts to solve the puzzle
                success = random.choice([True, False])
                if success:
                    print(f"{room[3][0]}")
                    player_health = player_health + room[3][2]
                    if player_health < 0:
                        player_health = 0
                        print("You are barely alive!")
                else:
                    print(f"{room[3][1]}")
                    player_health = player_health + room[3][2]
                    if player_health <= 0:
                        print("Oh no, you have died!")
                        return player_health, inventory
            else: #If the player chooses to skip the puzzle
                success = random.choice([True, False, False])
                if success:
                    print("You gained nothing, move on.")
                else:
                    print(f"{room[3][1]}")
                    player_health = player_health + room[3][2]
                    if player_health <= 0:
                        print("Oh no, you have died!")
                        return player_health, inventory
            display_inventory(inventory)

        else: #Path if the player enters the library with no challenge
            print("There doesn't seem to be a challenge in this room. You move on.")
            display_inventory(inventory)
    display_player_status(player_health)
    return player_health, inventory

def main():
    """Main game logic with initialized variables"""
    player_health = 100
    monster_health = 60 # Hardcoded health value
    has_treasure = False
    inventory = [ ] #Inventory initialized to empty

    dungeon_rooms = [("A room filled with lava", None, "trap",
                      ("You avoided the lava!", "You fell into the lava!", -10)),
                     ("A magnificent library", "spell book", "none", None),
                     ("A dark room with portraits and locked chest", "pile of gold coins", "puzzle",
                      ("You unlocked the chest!", "The chest remains locked.", -5))]

    #Demonstrating tuple immutability: The following line will cause a TypeError
    #because tuples cannot be modified after they are created
    dungeon_rooms[1][1] = "magic potion"

    has_treasure = random.choice([True, False]) # Randomly assigns treasure

    player_health = handle_path_choice(player_health)

    treasure_obtained_in_combat = combat_encounter(player_health, monster_health, has_treasure)

    check_for_treasure(treasure_obtained_in_combat) # Or has_treasure, depending on logic

    if player_health > 0:
        player_health, inventory = enter_dungeon(player_health, inventory, dungeon_rooms)
        #Unpacking tuple of enter_dungeon return statements if the player is still alive

if __name__ == "__main__":
    main()
