import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tooltip  # Import the tooltip library

# Save the configuration to a JSON file
def save_config(config, filename):
    with open(filename, 'w') as file:
        json.dump(config, file, indent=4)

# Load the configuration from a JSON file
def load_config(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Update ServerGameSettings.json configuration values from the GUI
def update_game_settings():
    global game_settings_file
    if game_settings_file:
        config = {key: var.get() if not isinstance(var, tk.BooleanVar) else bool(var.get()) for key, var in game_config_vars.items()}
        # Ensure specific fields are correctly cast
        config['InactivityKillTimeMin'] = int(game_config_vars['InactivityKillTimeMin'].get())
        config['InactivityKillTimeMax'] = int(game_config_vars['InactivityKillTimeMax'].get())
        config['InactivityKillSafeTimeAddition'] = int(game_config_vars['InactivityKillSafeTimeAddition'].get())
        config['InactivityKillTimerMaxItemLevel'] = int(game_config_vars['InactivityKillTimerMaxItemLevel'].get())
        config['DisableDisconnectedDeadTimer'] = int(game_config_vars['DisableDisconnectedDeadTimer'].get())
        config['InventoryStacksModifier'] = float(game_config_vars['InventoryStacksModifier'].get())
        config['DropTableModifier_General'] = float(game_config_vars['DropTableModifier_General'].get())
        config['DropTableModifier_Missions'] = float(game_config_vars['DropTableModifier_Missions'].get())
        config['MaterialYieldModifier_Global'] = float(game_config_vars['MaterialYieldModifier_Global'].get())
        config['BloodEssenceYieldModifier'] = float(game_config_vars['BloodEssenceYieldModifier'].get())
        config['JournalVBloodSourceUnitMaxDistance'] = float(game_config_vars['JournalVBloodSourceUnitMaxDistance'].get())
        config['PvPVampireRespawnModifier'] = float(game_config_vars['PvPVampireRespawnModifier'].get())
        config['CastleMinimumDistanceInFloors'] = int(game_config_vars['CastleMinimumDistanceInFloors'].get())
        config['ClanSize'] = int(game_config_vars['ClanSize'].get())
        config['BloodDrainModifier'] = float(game_config_vars['BloodDrainModifier'].get())
        config['DurabilityDrainModifier'] = float(game_config_vars['DurabilityDrainModifier'].get())
        config['GarlicAreaStrengthModifier'] = float(game_config_vars['GarlicAreaStrengthModifier'].get())
        config['HolyAreaStrengthModifier'] = float(game_config_vars['HolyAreaStrengthModifier'].get())
        config['SilverStrengthModifier'] = float(game_config_vars['SilverStrengthModifier'].get())
        config['SunDamageModifier'] = float(game_config_vars['SunDamageModifier'].get())
        config['CastleDecayRateModifier'] = float(game_config_vars['CastleDecayRateModifier'].get())
        config['CastleBloodEssenceDrainModifier'] = float(game_config_vars['CastleBloodEssenceDrainModifier'].get())
        config['CastleSiegeTimer'] = float(game_config_vars['CastleSiegeTimer'].get())
        config['CastleUnderAttackTimer'] = float(game_config_vars['CastleUnderAttackTimer'].get())
        config['BuildCostModifier'] = float(game_config_vars['BuildCostModifier'].get())
        config['RecipeCostModifier'] = float(game_config_vars['RecipeCostModifier'].get())
        config['CraftRateModifier'] = float(game_config_vars['CraftRateModifier'].get())
        config['ResearchCostModifier'] = float(game_config_vars['ResearchCostModifier'].get())
        config['RefinementCostModifier'] = float(game_config_vars['RefinementCostModifier'].get())
        config['RefinementRateModifier'] = float(game_config_vars['RefinementRateModifier'].get())
        config['ResearchTimeModifier'] = float(game_config_vars['ResearchTimeModifier'].get())
        config['DismantleResourceModifier'] = float(game_config_vars['DismantleResourceModifier'].get())
        config['ServantConvertRateModifier'] = float(game_config_vars['ServantConvertRateModifier'].get())
        config['RepairCostModifier'] = float(game_config_vars['RepairCostModifier'].get())
        config['Death_DurabilityFactorLoss'] = float(game_config_vars['Death_DurabilityFactorLoss'].get())
        config['Death_DurabilityLossFactorAsResources'] = float(game_config_vars['Death_DurabilityLossFactorAsResources'].get())
        config['StarterEquipmentId'] = int(game_config_vars['StarterEquipmentId'].get())
        config['StarterResourcesId'] = int(game_config_vars['StarterResourcesId'].get())
        save_config(config, game_settings_file)
        messagebox.showinfo("Success", "Configuration saved successfully!")
    else:
        messagebox.showerror("Error", "No file loaded!")

# Load ServerGameSettings.json configuration from a selected file
def load_game_settings():
    global game_settings_file
    game_settings_file = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if game_settings_file:
        config_data = load_config(game_settings_file)
        for key, value in config_data.items():
            if key in game_config_vars:
                if isinstance(game_config_vars[key], tk.BooleanVar):
                    game_config_vars[key].set(int(value))
                else:
                    game_config_vars[key].set(str(value))
        messagebox.showinfo("Success", f"Configuration loaded from {game_settings_file}")

# Update ServerHostSettings.json configuration values from the GUI
def update_host_settings():
    global host_settings_file
    if host_settings_file:
        config = {key: var.get() if not isinstance(var, tk.BooleanVar) else bool(var.get()) for key, var in host_config_vars.items()}
        # Ensure specific fields are correctly cast
        config['Port'] = int(host_config_vars['Port'].get())
        config['QueryPort'] = int(host_config_vars['QueryPort'].get())
        config['MaxConnectedUsers'] = int(host_config_vars['MaxConnectedUsers'].get())
        config['MaxConnectedAdmins'] = int(host_config_vars['MaxConnectedAdmins'].get())
        config['AutoSaveCount'] = int(host_config_vars['AutoSaveCount'].get())
        config['AutoSaveInterval'] = int(host_config_vars['AutoSaveInterval'].get())
        save_config(config, host_settings_file)
        messagebox.showinfo("Success", "Configuration saved successfully!")
    else:
        messagebox.showerror("Error", "No file loaded!")

# Load ServerHostSettings.json configuration from a selected file
def load_host_settings():
    global host_settings_file
    host_settings_file = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if host_settings_file:
        config_data = load_config(host_settings_file)
        for key, value in config_data.items():
            if key in host_config_vars:
                if isinstance(host_config_vars[key], tk.BooleanVar):
                    host_config_vars[key].set(int(value))
                else:
                    host_config_vars[key].set(str(value))
        messagebox.showinfo("Success", f"Configuration loaded from {host_settings_file}")

# Create the main window
root = tk.Tk()
root.title("vRising Config Editor")
game_settings_file = None
host_settings_file = None

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# Create frames for each tab
game_settings_frame = ttk.Frame(notebook)
host_settings_frame = ttk.Frame(notebook)

notebook.add(game_settings_frame, text='ServerGameSettings')
notebook.add(host_settings_frame, text='ServerHostSettings')

# Define tkinter variables for each ServerGameSettings.json config option
game_config_vars = {
    "GameModeType": tk.StringVar(),
    "CastleDamageMode": tk.StringVar(),
    "SiegeWeaponHealth": tk.StringVar(),
    "PlayerDamageMode": tk.StringVar(),
    "CastleHeartDamageMode": tk.StringVar(),
    "PvPProtectionMode": tk.StringVar(),
    "DeathContainerPermission": tk.StringVar(),
    "RelicSpawnType": tk.StringVar(),
    "CanLootEnemyContainers": tk.BooleanVar(),
    "BloodBoundEquipment": tk.BooleanVar(),
    "TeleportBoundItems": tk.BooleanVar(),
    "AllowGlobalChat": tk.BooleanVar(),
    "AllWaypointsUnlocked": tk.BooleanVar(),
    "FreeCastleClaim": tk.BooleanVar(),
    "FreeCastleDestroy": tk.BooleanVar(),
    "InactivityKillEnabled": tk.BooleanVar(),
    "InactivityKillTimeMin": tk.StringVar(),
    "InactivityKillTimeMax": tk.StringVar(),
    "InactivityKillSafeTimeAddition": tk.StringVar(),
    "InactivityKillTimerMaxItemLevel": tk.StringVar(),
    "DisableDisconnectedDeadEnabled": tk.BooleanVar(),
    "DisableDisconnectedDeadTimer": tk.StringVar(),
    "InventoryStacksModifier": tk.StringVar(),
    "DropTableModifier_General": tk.StringVar(),
    "DropTableModifier_Missions": tk.StringVar(),
    "MaterialYieldModifier_Global": tk.StringVar(),
    "BloodEssenceYieldModifier": tk.StringVar(),
    "JournalVBloodSourceUnitMaxDistance": tk.StringVar(),
    "PvPVampireRespawnModifier": tk.StringVar(),
    "CastleMinimumDistanceInFloors": tk.StringVar(),
    "ClanSize": tk.StringVar(),
    "BloodDrainModifier": tk.StringVar(),
    "DurabilityDrainModifier": tk.StringVar(),
    "GarlicAreaStrengthModifier": tk.StringVar(),
    "HolyAreaStrengthModifier": tk.StringVar(),
    "SilverStrengthModifier": tk.StringVar(),
    "SunDamageModifier": tk.StringVar(),
    "CastleDecayRateModifier": tk.StringVar(),
    "CastleBloodEssenceDrainModifier": tk.StringVar(),
    "CastleSiegeTimer": tk.StringVar(),
    "CastleUnderAttackTimer": tk.StringVar(),
    "AnnounceSiegeWeaponSpawn": tk.BooleanVar(),
    "ShowSiegeWeaponMapIcon": tk.BooleanVar(),
    "BuildCostModifier": tk.StringVar(),
    "RecipeCostModifier": tk.StringVar(),
    "CraftRateModifier": tk.StringVar(),
    "ResearchCostModifier": tk.StringVar(),
    "RefinementCostModifier": tk.StringVar(),
    "RefinementRateModifier": tk.StringVar(),
    "ResearchTimeModifier": tk.StringVar(),
    "DismantleResourceModifier": tk.StringVar(),
    "ServantConvertRateModifier": tk.StringVar(),
    "RepairCostModifier": tk.StringVar(),
    "Death_DurabilityFactorLoss": tk.StringVar(),
    "Death_DurabilityLossFactorAsResources": tk.StringVar(),
    "StarterEquipmentId": tk.StringVar(),
    "StarterResourcesId": tk.StringVar()
}

# Define labels and choices for each ServerGameSettings.json config option
game_config_options = {
    "GameModeType": ("Game Mode Type", ["PvP", "PvE"], "Sets the game mode."),
    "CastleDamageMode": ("Castle Damage Mode", ["Always", "Never", "TimeRestricted"], "Sets when Castles can be damaged. 'TimeRestricted' uses VSCastle times."),
    "SiegeWeaponHealth": ("Siege Weapon Health", [], "Determines the health of Siege Weapons."),
    "PlayerDamageMode": ("Player Damage Mode", ["Always", "TimeRestricted"], "Determines whether or not other players can be damaged. 'TimeRestricted' uses Vs Player times."),
    "CastleHeartDamageMode": ("Castle Heart Damage Mode", ["CanBeDestroyedOnlyWhenDecaying", "CanBeDestroyedByPlayers", "CanBeSeizedOrDestroyedByPlayers"], "Determines how and when Castle Hearts can be destroyed or seized."),
    "PvPProtectionMode": ("PvP Protection Mode", ["Short", "Medium", "Long"], "Protection you get when you first make your character that prevents newbies from being slaughtered in PvP."),
    "DeathContainerPermission": ("Death Container Permission", ["Anyone", "ClanMembers"], "Defines who can loot your dropped items after you die."),
    "RelicSpawnType": ("Relic Spawn Type", ["Unique", "Plentiful"], "Determines whether there is only one of each Soul Shard in the world or whether there can be more than one of each type."),
    "CanLootEnemyContainers": ("Can Loot Enemy Containers", ["true", "false"], "Determines whether or not a random person sneaking into your base can access your chests and other containers."),
    "BloodBoundEquipment": ("Blood Bound Equipment", ["true", "false"], "Lose or keep your equipment upon death."),
    "TeleportBoundItems": ("Teleport Bound Items", ["true", "false"], "When using a Vampire Waygate you can turn this on or off to determine if your items travel with you."),
    "AllowGlobalChat": ("Allow Global Chat", ["true", "false"], "Turns Global Chat on or off."),
    "AllWaypointsUnlocked": ("All Waypoints Unlocked", ["true", "false"], "Reveals or conceals Vampire Waygates."),
    "FreeCastleClaim": ("Free Castle Claim", ["true", "false"], "Allows people to claim a castle without paying a resource cost."),
    "FreeCastleDestroy": ("Free Castle Destroy", ["true", "false"], "Determines whether or not Castles can be destroyed at no resource cost."),
    "InactivityKillEnabled": ("Inactivity Kill Enabled", ["true", "false"], ""),
    "InactivityKillTimeMin": ("Inactivity Kill Time Min", [], ""),
    "InactivityKillTimeMax": ("Inactivity Kill Time Max", [], ""),
    "InactivityKillSafeTimeAddition": ("Inactivity Kill Safe Time Addition", [], ""),
    "InactivityKillTimerMaxItemLevel": ("Inactivity Kill Timer Max Item Level", [], ""),
    "DisableDisconnectedDeadEnabled": ("Disable Disconnected Dead Enabled", ["true", "false"], ""),
    "DisableDisconnectedDeadTimer": ("Disable Disconnected Dead Timer", [], ""),
    "InventoryStacksModifier": ("Inventory Stacks Modifier", [], "The size of your inventory stacks."),
    "DropTableModifier_General": ("Drop Table Modifier General", [], "Increase or decrease the amount of loot that drops from enemies."),
    "DropTableModifier_Missions": ("Drop Table Modifier Missions", [], "Increase or decrease the amount of loot that drops from missions."),
    "MaterialYieldModifier_Global": ("Material Yield Modifier Global", [], "This modifies the amount you get from a resource node like a stone or copper."),
    "BloodEssenceYieldModifier": ("Blood Essence Yield Modifier", [], "This changes how much Blood Essence you gain from killing enemies."),
    "JournalVBloodSourceUnitMaxDistance": ("Journal VBlood Source Unit Max Distance", [], "Increase tracking for a more accurate trail."),
    "PvPVampireRespawnModifier": ("PvP Vampire Respawn Modifier", [], "This is how long it takes you to respawn after being killed in PvP."),
    "CastleMinimumDistanceInFloors": ("Castle Minimum Distance In Floors", [], "This is how far away someone else’s boundaries must be. I suggest increasing this to prevent base trapping."),
    "ClanSize": ("Clan Size", [], "Determines the maximum size of a Clan."),
    "BloodDrainModifier": ("Blood Drain Modifier", [], "How much your blood level drains."),
    "DurabilityDrainModifier": ("Durability Drain Modifier", [], "This determines how much the durability drains."),
    "GarlicAreaStrengthModifier": ("Garlic Area Strength Modifier", [], "Modifies the strength of Garlic areas."),
    "HolyAreaStrengthModifier": ("Holy Area Strength Modifier", [], "Modifies the strength of Holy areas."),
    "SilverStrengthModifier": ("Silver Strength Modifier", [], "Modifies the strength of the Silver debuff."),
    "SunDamageModifier": ("Sun Damage Modifier", [], "Modifies the strength of the Sun debuff."),
    "CastleDecayRateModifier": ("Castle Decay Rate Modifier", [], "Modifies the rate at which Castles decay."),
    "CastleBloodEssenceDrainModifier": ("Castle Blood Essence Drain Modifier", [], "Modifies the rate at which Castles drain stored Blood Essence."),
    "CastleSiegeTimer": ("Castle Siege Timer", [], "How long a Castle can be sieged by another player."),
    "CastleUnderAttackTimer": ("Castle Under Attack Timer", [], "How long a castle can be under attack."),
    "AnnounceSiegeWeaponSpawn": ("Announce Siege Weapon Spawn", ["true", "false"], "Announces the deployment of a Siege Weapon on the server."),
    "ShowSiegeWeaponMapIcon": ("Show Siege Weapon Map Icon", ["true", "false"], "This will display the Siege Weapon on the map."),
    "BuildCostModifier": ("Build Cost Modifier", [], "Modifies the cost for buildings."),
    "RecipeCostModifier": ("Recipe Cost Modifier", [], "Modifies the cost for Crafting."),
    "CraftRateModifier": ("Craft Rate Modifier", [], "Modifies the speed of Crafting."),
    "ResearchCostModifier": ("Research Cost Modifier", [], "Modifies the cost of Research."),
    "RefinementCostModifier": ("Refinement Cost Modifier", [], "Modifies the cost of Refining."),
    "RefinementRateModifier": ("Refinement Rate Modifier", [], "Modifies the speed of Refining."),
    "ResearchTimeModifier": ("Research Time Modifier", [], "Modifies the speed of Research."),
    "DismantleResourceModifier": ("Dismantle Resource Modifier", [], "This is how much you get back after dismantling something like a wall."),
    "ServantConvertRateModifier": ("Servant Convert Rate Modifier", [], "Time it takes to convert a Servant."),
    "RepairCostModifier": ("Repair Cost Modifier", [], "Increases or decreases the repair costs for buildings."),
    "Death_DurabilityFactorLoss": ("Death Durability Factor Loss", [], "Durability loss when killed."),
    "Death_DurabilityLossFactorAsResources": ("Death Durability Loss Factor As Resources", [], "This factors in your current durability into how much resources you lose."),
    "StarterEquipmentId": ("Starter Equipment Id", [], "This is what equipment you start with."),
    "StarterResourcesId": ("Starter Resources Id", [], "Instead of straight giving the players gear it gives them a lot of resources instead.")
}

# Game Settings Presets
game_settings_presets = [
    "StandardPvP",
    "StandardPvP_Easy",
    "StandardPvP_Hard",
    "Level30PvP",
    "Level50PvP",
    "Level70PvP",
    "SoloPvP",
    "DuoPvP",
    "HardcorePvP",
    "StandardPvE",
    "StandardPvE_Easy",
    "StandardPvE_Hard",
    "Level30PvE",
    "Level50PvE",
    "Level70PvE"
]

# Define tkinter variables for each ServerHostSettings.json config option with default values
host_config_vars = {
    "Name": tk.StringVar(value="v-rising Server"),
    "Description": tk.StringVar(value="Editor by slanted corp, enjoy!"),
    "Port": tk.StringVar(value="9876"),
    "QueryPort": tk.StringVar(value="9877"),
    "MaxConnectedUsers": tk.StringVar(value="10"),
    "MaxConnectedAdmins": tk.StringVar(value="1"),
    "SaveName": tk.StringVar(value="world1"),
    "Password": tk.StringVar(value=""),
    "ListOnMasterServer": tk.BooleanVar(value=True),
    "Secure": tk.BooleanVar(value=True),
    "AdminOnlyDebugEvents": tk.BooleanVar(value=True),
    "DisableDebugEvents": tk.BooleanVar(value=False),
    "AutoSaveCount": tk.StringVar(value="40"),
    "AutoSaveInterval": tk.StringVar(value="120"),
    "GameSettingsPreset": tk.StringVar(value="")
}

# Define labels for each ServerHostSettings.json config option
host_config_options = {
    "Name": ("Server Name", "Name of server"),
    "Description": ("Server Description", "Short description of server purpose, rules, message of the day"),
    "Port": ("Port", "UDP port for game traffic"),
    "QueryPort": ("Query Port", "UDP port for Steam server list features"),
    "MaxConnectedUsers": ("Max Connected Users", "Max number of concurrent players on server"),
    "MaxConnectedAdmins": ("Max Connected Admins", "Max number of admins to allow connect even when server is full"),
    "SaveName": ("Save Name", "Name of save file/directory"),
    "Password": ("Password", "Set a password or leave empty"),
    "ListOnMasterServer": ("List On Master Server", "Set to true to list on server list, else set to false"),
    "Secure": ("Secure", "Use secure connections"),
    "AdminOnlyDebugEvents": ("Admin Only Debug Events", "Enable debug events for admins only"),
    "DisableDebugEvents": ("Disable Debug Events", "Disable all debug events"),
    "AutoSaveCount": ("Auto Save Count", "Number of autosaves to keep"),
    "AutoSaveInterval": ("Auto Save Interval", "Interval in seconds between each auto save"),
    "GameSettingsPreset": ("Game Settings Preset", "Name of a GameSettings preset found in the GameSettingPresets folder")
}

# Define a function to create a row in the GUI
def create_row(parent, label_text, var, choices, row, col=0, tooltip_text=None):
    label = tk.Label(parent, text=label_text)
    label.grid(row=row, column=col, sticky='e')
    width = 40 if parent == host_settings_frame else 20  # Increase the width only for host settings
    if choices:
        entry = ttk.Combobox(parent, textvariable=var, values=choices)
    else:
        entry = tk.Entry(parent, textvariable=var, width=width)
    entry.grid(row=row, column=col + 1, sticky='w')
    if tooltip_text:
        tooltip.ToolTip(label, tooltip_text)

# Create rows for each ServerGameSettings.json config option
row = 0
column = 0
for key, (label, choices, tooltip_text) in game_config_options.items():
    if row > 20:  # Adjust number of rows before moving to the next column
        row = 0
        column += 2
    create_row(game_settings_frame, label, game_config_vars[key], choices, row, column, tooltip_text)
    row += 1

# Create rows for each ServerHostSettings.json config option
row = 0
column = 0
for key, (label, tooltip_text) in host_config_options.items():
    if key == "GameSettingsPreset":
        create_row(host_settings_frame, label, host_config_vars[key], game_settings_presets, row, column, tooltip_text)
    else:
        create_row(host_settings_frame, label, host_config_vars[key], [], row, column, tooltip_text)
    if row > 20:  # Adjust number of rows before moving to the next column
        row = 0
        column += 2
    row += 1

# Add a menu for loading and saving
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Load Game Settings", command=load_game_settings)
file_menu.add_command(label="Save Game Settings", command=update_game_settings)
file_menu.add_command(label="Load Host Settings", command=load_host_settings)
file_menu.add_command(label="Save Host Settings", command=update_host_settings)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Start the GUI event loop
root.mainloop()

