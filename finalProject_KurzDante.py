import json
import random
import time
import os

# ---------- GLOBALS ----------
SAVE_FILE = "savegame.json"
side_quest_completed = False

def slow(text):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(0.015)
    print()

# ---------- SAVE / LOAD ----------
def save_game(player, level):
    data = {
        "name": player.name,
        "role": player.role,
        "hp": player.hp,
        "attack": player.attack,
        "level": player.level,
        "exp": player.exp,
        "gold": player.gold,
        "story_level": level,
        "weapon": player.weapon if hasattr(player, "weapon") else None,
        "spells": player.spells if hasattr(player, "spells") else None
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    slow("\nGame saved!\n")

def load_game():
    if not os.path.exists(SAVE_FILE):
        slow("No save file found.")
        return None, None

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    player = Player(data["name"], data["role"])
    player.hp = data["hp"]
    player.attack = data["attack"]
    player.level = data["level"]
    player.exp = data["exp"]
    player.gold = data["gold"]

    if data["weapon"]:
        player.weapon = data["weapon"]
    if data["spells"]:
        player.spells = data["spells"]

    slow("\nSave loaded successfully!\n")
    return player, data["story_level"]

# ---------- CLASSES ----------
class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.weapon = None

        if role == "Knight":
            self.hp = 120
            self.attack = 15
        elif role == "Wizard":
            self.hp = 80
            self.attack = 8
            self.spells = ["Firebolt", "Arcane Blast", "Lightning Spark"]
        elif role == "Goblin":
            self.hp = 100
            self.attack = 12
            self.gold = 20

    def level_up(self):
        self.level += 1
        self.hp += 20
        self.attack += 3
        slow(f"\n*** LEVEL UP! You are now Level {self.level}! ***\n")

class Enemy:
    def __init__(self, name, hp, attack, gold_drop):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.gold_drop = gold_drop

# ---------- WORLD MAP ----------
def world_map(level):
    slow("\n=== WORLD MAP ===")

    locations = [
        "Dark Forest (Start)",
        "Forest Edge",
        "Old Bridge",
        "Mountain Foot",
        "Mountain Pass",
        "High Cliffs",
        "Shadow Caverns Entrance",
        "Deep Shadow Caverns",
        "Abyss Gate",
        "Dragon’s Dungeon (Final)"
    ]

    for i, loc in enumerate(locations):
        if i < level:
            slow(f"[✔] {loc}")
        elif i == level:
            slow(f"[YOU ARE HERE] {loc}")
        else:
            slow(f"[ ] {loc}")

    progress = int((level / 9) * 100)
    slow(f"\nProgress toward saving the Princess: {progress}%\n")

# ---------- COMBAT ----------
def combat(player, enemy):
    slow(f"\nA {enemy.name} appears!")

    while enemy.hp > 0 and player.hp > 0:
        slow(f"\nYour HP: {player.hp} | {enemy.name} HP: {enemy.hp}")
        slow("1. Attack")
        if player.role == "Wizard":
            slow("2. Cast Spell")
        if player.role == "Goblin":
            slow("3. Bribe Enemy")

        choice = input("> ")

        if choice == "1":
            dmg = player.attack
            if player.role == "Knight" and player.weapon:
                dmg += player.weapon["power"]
            slow(f"You hit the {enemy.name} for {dmg} damage!")
            enemy.hp -= dmg

        elif choice == "2" and player.role == "Wizard":
            spell = random.choice(player.spells)
            dmg = random.randint(15, 30)
            slow(f"You cast {spell} for {dmg} damage!")
            enemy.hp -= dmg

        elif choice == "3" and player.role == "Goblin":
            cost = random.randint(10, 25)
            if player.gold >= cost:
                slow(f"You bribe the {enemy.name} with {cost} gold. It leaves!")
                player.gold -= cost
                return True
            else:
                slow("Not enough gold!")

        else:
            slow("Invalid choice.")
            continue

        if enemy.hp > 0:
            slow(f"The {enemy.name} hits you for {enemy.attack} damage!")
            player.hp -= enemy.attack

    if player.hp <= 0:
        slow("\nYou have fallen...")
        exit()

    slow(f"\nYou defeated the {enemy.name}!")
    player.exp += 20
    player.gold += enemy.gold_drop
    slow(f"You gained 20 EXP and {enemy.gold_drop} gold!")

    if player.exp >= player.level * 30:
        player.level_up()

    if player.role == "Knight" and random.random() < 0.4:
        weapon = {"name": "Steel Sword", "power": random.randint(5, 12)}
        player.weapon = weapon
        slow(f"You found a weapon: {weapon['name']} (+{weapon['power']} attack)")

    return True

# ---------- SIDE QUESTS ----------
def side_quest(player):
    global side_quest_completed

    slow("\nA side quest opportunity appears on your journey...")

    quests = [
        {
            "name": "Lost Child",
            "desc": "A villager begs you to find their missing child in the woods.",
            "enemy": Enemy("Forest Beast", 50, 10, 15),
            "reward": "gold",
            "amount": 30
        },
        {
            "name": "Cursed Shrine",
            "desc": "A dark shrine radiates evil energy. Destroy the spirit guarding it.",
            "enemy": Enemy("Cursed Spirit", 60, 12, 20),
            "reward": "xp",
            "amount": 40
        },
        {
            "name": "Merchant Caravan",
            "desc": "Bandits are attacking a merchant caravan. Help defend it.",
            "enemy": Enemy("Bandit Leader", 70, 14, 25),
            "reward": "heal",
            "amount": 40
        },
        {
            "name": "Ancient Ruins",
            "desc": "You discover ruins containing a magical artifact.",
            "enemy": Enemy("Stone Guardian", 80, 15, 30),
            "reward": "item",
            "amount": None
        }
    ]

    quest = random.choice(quests)

    slow(f"\nSide Quest: {quest['name']}")
    slow(quest["desc"])
    slow("Do you accept the quest? (y/n)")

    choice = input("> ").lower()
    if choice != "y":
        slow("You ignore the side quest and continue your journey.")
        return

    slow("\nYou accept the quest!")
    combat(player, quest["enemy"])

    side_quest_completed = True

    if quest["reward"] == "gold":
        player.gold += quest["amount"]
        slow(f"You earned {quest['amount']} gold!")
    elif quest["reward"] == "xp":
        player.exp += quest["amount"]
        slow(f"You gained {quest['amount']} XP!")
        if player.exp >= player.level * 30:
            player.level_up()
    elif quest["reward"] == "heal":
        player.hp += quest["amount"]
        slow(f"You recovered {quest['amount']} HP!")
    elif quest["reward"] == "item":
        if player.role == "Knight":
            weapon = {"name": "Ancient Blade", "power": random.randint(10, 18)}
            player.weapon = weapon
            slow(f"You found a weapon: {weapon['name']} (+{weapon['power']} attack)")
        elif player.role == "Wizard":
            new_spell = "Celestial Burst"
            player.spells.append(new_spell)
            slow(f"You learned a new spell: {new_spell}!")
        elif player.role == "Goblin":
            gold_reward = 50
            player.gold += gold_reward
            slow(f"You found hidden treasure worth {gold_reward} gold!")

    slow("Side quest complete!\n")

# ---------- TREASURE ROOMS ----------
def treasure_room(player):
    global side_quest_completed
    side_quest_completed = False

    slow("\nYou discover a hidden TREASURE ROOM!")

    loot_table = [
        {"type": "weapon", "name": "Silver Sword", "power": 10},
        {"type": "weapon", "name": "Dragonbone Blade", "power": 18},
        {"type": "armor", "name": "Iron Armor", "defense": 10},
        {"type": "armor", "name": "Elven Cloak", "defense": 15},
        {"type": "potion", "name": "Healing Potion", "heal": 40},
        {"type": "potion", "name": "Mega Healing Potion", "heal": 80},
        {"type": "jewel", "name": "Ruby", "value": 50},
        {"type": "jewel", "name": "Emerald", "value": 75},
        {"type": "jewel", "name": "Diamond", "value": 120}
    ]

    loot = random.choice(loot_table)
    slow(f"You found: {loot['name']}!")

    if loot["type"] == "weapon" and player.role == "Knight":
        player.weapon = {"name": loot["name"], "power": loot["power"]}
        slow(f"Knight equips {loot['name']} (+{loot['power']} attack)")
    elif loot["type"] == "weapon":
        slow("Only Knights can use weapons. You sell it for 30 gold.")
        player.gold += 30
    elif loot["type"] == "armor":
        slow(f"You equip the {loot['name']}! You gain +{loot['defense']} HP.")
        player.hp += loot["defense"]
    elif loot["type"] == "potion":
        slow(f"You drink the potion and recover {loot['heal']} HP!")
        player.hp += loot["heal"]
    elif loot["type"] == "jewel":
        slow(f"You sell the {loot['name']} for {loot['value']} gold!")
        player.gold += loot["value"]

    slow("You leave the treasure room.\n")

# ---------- STORY PATH ----------
def story_path(player, start_level=1):
    slow("\nYour journey begins in the DARK FOREST...")
    slow("You must choose your path wisely to reach the Dragon’s Dungeon.\n")

    forest_enemies = [
        Enemy("Goblin", 40, 8, 10),
        Enemy("Wolf", 45, 9, 12),
        Enemy("Bandit", 50, 10, 15)
    ]

    mountain_enemies = [
        Enemy("Orc", 60, 12, 18),
        Enemy("Troll", 75, 15, 22),
        Enemy("Warlock", 80, 16, 25)
    ]

    cavern_enemies = [
        Enemy("Assassin", 85, 20, 30),
        Enemy("Demon", 100, 22, 35),
        Enemy("Shadow Beast", 110, 24, 40)
    ]

    for level in range(start_level, 10):
        slow(f"\n--- LEVEL {level} ---")

        world_map(level)

        if random.random() < 0.3:
            side_quest(player)

        if side_quest_completed:
            treasure_room(player)

        slow("\nChoose your path:")
        slow("1. Left Path (Forest – easier enemies)")
        slow("2. Right Path (Mountains – medium enemies)")
        slow("3. Forward Path (Caverns – hard enemies)")

        choice = input("> ")

        if choice == "1":
            enemy = random.choice(forest_enemies)
            slow("\nYou walk deeper into the Dark Forest...")
        elif choice == "2":
            enemy = random.choice(mountain_enemies)
            slow("\nYou climb the rocky mountain trail...")
        else:
            enemy = random.choice(cavern_enemies)
            slow("\nYou descend into the dark caverns...")

        combat(player, enemy)
        save_game(player, level + 1)

    final_boss(player)

# ---------- FINAL BOSS ----------
def final_boss(player):
    slow("\nYou reach the Dark Castle...")
    slow("The Princess is trapped inside...")
    slow("A massive DRAGON descends from the sky!")

    boss = Enemy("Dragon", 200, 25, 100)
    combat(player, boss)

    slow("\nYou defeated the Dragon and saved the Princess!")

    if player.role == "Knight":
        slow("The Princess marries you. You become a legendary king.")
    elif player.role == "Wizard":
        slow("The Princess gifts you an ancient staff of immense power.")
    elif player.role == "Goblin":
        slow("The Princess rewards you with a mountain of gold.")

    slow("\n*** THE END ***")
    exit()

# ---------- MAIN ----------
def main():
    slow("Welcome to the RPG Adventure!")
    slow("1. New Game")
    slow("2. Load Game")

    choice = input("> ")

    if choice == "2":
        player, level = load_game()
        if player:
            story_path(player, level)
            return

    name = input("Enter your name: ")
    slow("Choose your class:")
    slow("1. Knight")
    slow("2. Wizard")
    slow("3. Goblin")

    role_choice = input("> ")
    role = "Knight" if role_choice == "1" else "Wizard" if role_choice == "2" else "Goblin"

    player = Player(name, role)
    story_path(player)

if __name__ == "__main__":
    main()


