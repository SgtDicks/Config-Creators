import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from mcrcon import MCRcon
import tooltip
import requests
import subprocess
import os
import zipfile
import urllib.request
import threading

# GitHub repository details
REPO_OWNER = "SgtDicks"
REPO_NAME = "Config-Creators"
APP_VERSION = "0.7"

# Default configurations
default_game_config = {
    "GameModeType": "PvP",
    "CastleDamageMode": "Always",
    "SiegeWeaponHealth": "Normal",
    "PlayerDamageMode": "Always",
    "CastleHeartDamageMode": "CanBeDestroyedByPlayers",
    "PvPProtectionMode": "Medium",
    "DeathContainerPermission": "Anyone",
    "RelicSpawnType": "Unique",
    "CanLootEnemyContainers": True,
    "BloodBoundEquipment": True,
    "TeleportBoundItems": True,
    "AllowGlobalChat": True,
    "AllWaypointsUnlocked": False,
    "FreeCastleClaim": False,
    "FreeCastleDestroy": False,
    "InactivityKillEnabled": True,
    "InactivityKillTimeMin": 3600,
    "InactivityKillTimeMax": 604800,
    "InactivityKillSafeTimeAddition": 172800,
    "InactivityKillTimerMaxItemLevel": 84,
    "DisableDisconnectedDeadEnabled": True,
    "DisableDisconnectedDeadTimer": 60,
    "InventoryStacksModifier": 1.0,
    "DropTableModifier_General": 1.0,
    "DropTableModifier_Missions": 1.0,
    "MaterialYieldModifier_Global": 1.0,
    "BloodEssenceYieldModifier": 1.0,
    "JournalVBloodSourceUnitMaxDistance": 25.0,
    "PvPVampireRespawnModifier": 1.0,
    "CastleMinimumDistanceInFloors": 2,
    "ClanSize": 4,
    "BloodDrainModifier": 1.0,
    "DurabilityDrainModifier": 1.0,
    "GarlicAreaStrengthModifier": 1.0,
    "HolyAreaStrengthModifier": 1.0,
    "SilverStrengthModifier": 1.0,
    "SunDamageModifier": 1.0,
    "CastleDecayRateModifier": 1.0,
    "CastleBloodEssenceDrainModifier": 1.0,
    "CastleSiegeTimer": 420.0,
    "CastleUnderAttackTimer": 60.0,
    "AnnounceSiegeWeaponSpawn": True,
    "ShowSiegeWeaponMapIcon": True,
    "BuildCostModifier": 1.0,
    "RecipeCostModifier": 1.0,
    "CraftRateModifier": 1.0,
    "ResearchCostModifier": 1.0,
    "RefinementCostModifier": 1.0,
    "RefinementRateModifier": 1.0,
    "ResearchTimeModifier": 1.0,
    "DismantleResourceModifier": 0.75,
    "ServantConvertRateModifier": 1.0,
    "RepairCostModifier": 1.0,
    "Death_DurabilityFactorLoss": 0.25,
    "Death_DurabilityLossFactorAsResources": 1.0,
    "StarterEquipmentId": 0,
    "StarterResourcesId": 0,
    "HeightLimit": 6,
    "FloorLimit": 800,
    "ServantLimit": 20,
    "CastleLimit": 5
}

default_host_config = {
    "Name": "v-rising Server",
    "Description": "Editor by Slanted Corp, enjoy!",
    "Port": 9876,
    "QueryPort": 9877,
    "MaxConnectedUsers": 40,
    "MaxConnectedAdmins": 4,
    "ServerFps": 30,
    "SaveName": "world1",
    "Password": "",
    "Secure": True,
    "ListOnSteam": True,
    "ListOnEOS": True,
    "AutoSaveCount": 20,
    "AutoSaveInterval": 120,
    "CompressSaveFiles": True,
    "GameSettingsPreset": "",
    "GameDifficultyPreset": "",
    "AdminOnlyDebugEvents": True,
    "DisableDebugEvents": False,
    "API": {"Enabled": False},
    "Rcon": {"Enabled": True, "Port": 25575, "Password": "SomeOTHERRandomPassw0rd"}
}

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

# Redirect output to the console
def append_to_console(output_text):
    console_text.config(state=tk.NORMAL)
    console_text.insert(tk.END, output_text)
    console_text.see(tk.END)
    console_text.config(state=tk.DISABLED)

# SteamCMD functions
def run_steamcmd_command(command):
    try:
        append_to_console(f"Running command: {command}\n")
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        append_to_console(result.stdout)
        if result.stderr:
            append_to_console(result.stderr)
    except Exception as e:
        append_to_console(f"Error: {e}\n")

def download_and_extract_steamcmd():
    url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    local_zip_path = "steamcmd.zip"
    extract_path = "steamcmd"

    try:
        append_to_console(f"Downloading SteamCMD from {url}...\n")
        urllib.request.urlretrieve(url, local_zip_path)
        append_to_console("Extracting SteamCMD...\n")
        with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        os.remove(local_zip_path)
        append_to_console("SteamCMD downloaded and extracted.\n")
        return os.path.join(extract_path, "steamcmd.exe")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download and extract SteamCMD: {e}")
        return None

def install_server():
    def _install_server():
        steamcmd_path = steamcmd_path_var.get()
        if not os.path.isfile(steamcmd_path):
            steamcmd_path = download_and_extract_steamcmd()
            steamcmd_path_var.set(steamcmd_path)
        app_id = app_id_var.get()
        if not steamcmd_path or not app_id:
            messagebox.showerror("Error", "SteamCMD path and App ID are required.")
            return
        command = f'"{steamcmd_path}" +login anonymous +force_install_dir "{install_dir_var.get()}" +app_update {app_id} validate +quit'
        run_steamcmd_command(command)
    
    threading.Thread(target=_install_server).start()

def update_server():
    def _update_server():
        steamcmd_path = steamcmd_path_var.get()
        if not os.path.isfile(steamcmd_path):
            steamcmd_path = download_and_extract_steamcmd()
            steamcmd_path_var.set(steamcmd_path)
        app_id = app_id_var.get()
        if not steamcmd_path or not app_id:
            messagebox.showerror("Error", "SteamCMD path and App ID are required.")
            return
        command = f'"{steamcmd_path}" +login anonymous +force_install_dir "{install_dir_var.get()}" +app_update {app_id} +quit'
        run_steamcmd_command(command)
    
    threading.Thread(target=_update_server).start()

server_process = None

def start_server():
    global server_process
    def _start_server():
        global server_process
        server_executable_path = os.path.join(install_dir_var.get(), "VRisingServer.exe")
        if not os.path.isfile(server_executable_path):
            append_to_console(f"Server executable not found at {server_executable_path}\n")
            return
        append_to_console("Starting server...\n")
        server_process = subprocess.Popen([server_executable_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for stdout_line in iter(server_process.stdout.readline, ""):
            append_to_console(stdout_line)
        server_process.stdout.close()
    threading.Thread(target=_start_server).start()

def stop_server():
    global server_process
    if server_process:
        server_process.terminate()
        server_process = None
        append_to_console("Server stopped successfully.\n")
    else:
        messagebox.showerror("Error", "No server is currently running.")

# RCON client functions
def connect_rcon():
    global rcon_client
    rcon_host = rcon_host_var.get()
    rcon_port = int(rcon_port_var.get())
    rcon_password = rcon_password_var.get()
    try:
        rcon_client = MCRcon(rcon_host, rcon_password, port=rcon_port)
        rcon_client.connect()
        messagebox.showinfo("Success", "RCON connected successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to RCON: {e}")

def send_rcon_command():
    global rcon_client
    command = rcon_command_var.get()
    try:
        response = rcon_client.command(command)
        rcon_output_text.insert(tk.END, response + '\n')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send RCON command: {e}")

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
        game_settings_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if game_settings_file:
            update_game_settings()

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
    else:
        set_default_game_config()

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
        config['Rcon'] = {
            'Enabled': bool(host_config_vars['RconEnabled'].get()),
            'Port': int(host_config_vars['RconPort'].get()),
            'Password': host_config_vars['RconPassword'].get()
        }
        config['API'] = {
            'Enabled': bool(host_config_vars['APIEnabled'].get())
        }
        save_config(config, host_settings_file)
        messagebox.showinfo("Success", "Configuration saved successfully!")
    else:
        host_settings_file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if host_settings_file:
            update_host_settings()

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
    else:
        set_default_host_config()

def set_default_game_config():
    for key, value in default_game_config.items():
        if key in game_config_vars:
            if isinstance(game_config_vars[key], tk.BooleanVar):
                game_config_vars[key].set(int(value))
            else:
                game_config_vars[key].set(str(value))

def set_default_host_config():
    for key, value in default_host_config.items():
        if key in host_config_vars:
            if isinstance(host_config_vars[key], tk.BooleanVar):
                host_config_vars[key].set(int(value))
            else:
                host_config_vars[key].set(str(value))

def check_for_updates():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
    try:
        response = requests.get(url)
        response.raise_for_status()
        latest_release = response.json()
        latest_version = latest_release["tag_name"]
        release_notes = latest_release["body"]
        
        if float(latest_version[1:]) <= float(APP_VERSION):
            messagebox.showinfo("Up-to-date", f"Your application is up-to-date (version {APP_VERSION}).")
        else:
            messagebox.showinfo("Update Available", f"Version {latest_version} is available.\n\nRelease notes:\n{release_notes}")
    except requests.RequestException as e:
        messagebox.showerror("Update Check Failed", f"Could not check for updates: {e}")

# Create the main window
root = tk.Tk()
root.title(f"vRising Server Manager V{APP_VERSION}")
game_settings_file = None
host_settings_file = None
rcon_client = None  # RCON client variable

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill="both")

# Create frames for each tab
game_settings_frame = ttk.Frame(notebook)
host_settings_frame = ttk.Frame(notebook)
rcon_frame = ttk.Frame(notebook)
steamcmd_frame = ttk.Frame(notebook)

notebook.add(game_settings_frame, text='ServerGameSettings')
notebook.add(host_settings_frame, text='ServerHostSettings')
notebook.add(rcon_frame, text='RCON Client')
notebook.add(steamcmd_frame, text='SteamCMD')

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
    "StarterResourcesId": tk.StringVar(),
    "HeightLimit": tk.StringVar(),
    "FloorLimit": tk.StringVar(),
    "ServantLimit": tk.StringVar(),
    "CastleLimit": tk.StringVar()
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
    "StarterResourcesId": ("Starter Resources Id", [], "Instead of straight giving the players gear it gives them a lot of resources instead."),
    "HeightLimit": ("Height Limit", [], "Height limit for the castle (1-6)."),
    "FloorLimit": ("Floor Limit", [], "Determines how many floors can be placed at that castle level (9-800)."),
    "ServantLimit": ("Servant Limit", [], "Changes how many servants are allowed per castle level (max 20)."),
    "CastleLimit": ("Castle Limit", [], "Sets the limit of Castle Hearts that can be placed for each player (max 5).")
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
    "Description": tk.StringVar(value="Editor by Slanted Corp, enjoy!"),
    "Port": tk.StringVar(value="9876"),
    "QueryPort": tk.StringVar(value="9877"),
    "MaxConnectedUsers": tk.StringVar(value="40"),
    "MaxConnectedAdmins": tk.StringVar(value="4"),
    "ServerFps": tk.StringVar(value="30"),
    "SaveName": tk.StringVar(value="world1"),
    "Password": tk.StringVar(value=""),
    "Secure": tk.BooleanVar(value=True),
    "ListOnSteam": tk.BooleanVar(value=True),
    "ListOnEOS": tk.BooleanVar(value=True),
    "AutoSaveCount": tk.StringVar(value="20"),
    "AutoSaveInterval": tk.StringVar(value="120"),
    "CompressSaveFiles": tk.BooleanVar(value=True),
    "GameSettingsPreset": tk.StringVar(value=""),
    "GameDifficultyPreset": tk.StringVar(value=""),
    "AdminOnlyDebugEvents": tk.BooleanVar(value=True),
    "DisableDebugEvents": tk.BooleanVar(value=False),
    "APIEnabled": tk.BooleanVar(value=False),
    "RconEnabled": tk.BooleanVar(value=True),
    "RconPort": tk.StringVar(value="25575"),
    "RconPassword": tk.StringVar(value="SomeOTHERRandomPassw0rd")
}

# Define labels for each ServerHostSettings.json config option
host_config_options = {
    "Name": ("Server Name", "Name of server"),
    "Description": ("Server Description", "Short description of server purpose, rules, message of the day"),
    "Port": ("Port", "UDP port for game traffic"),
    "QueryPort": ("Query Port", "UDP port for Steam server list features"),
    "MaxConnectedUsers": ("Max Connected Users", "Max number of concurrent players on server"),
    "MaxConnectedAdmins": ("Max Connected Admins", "Max number of admins to allow connect even when server is full"),
    "ServerFps": ("Server FPS", "Server frame rate"),
    "SaveName": ("Save Name", "Name of save file/directory"),
    "Password": ("Password", "Set a password or leave empty"),
    "Secure": ("Secure", "Use secure connections"),
    "ListOnSteam": ("List On Steam", "Set to true to list on Steam server list, else set to false"),
    "ListOnEOS": ("List On EOS", "Set to true to list on EOS server list, else set to false"),
    "AutoSaveCount": ("Auto Save Count", "Number of autosaves to keep"),
    "AutoSaveInterval": ("Auto Save Interval", "Interval in seconds between each auto save"),
    "CompressSaveFiles": ("Compress Save Files", "Set to true to compress save files"),
    "GameSettingsPreset": ("Game Settings Preset", "Name of a GameSettings preset found in the GameSettingPresets folder"),
    "GameDifficultyPreset": ("Game Difficulty Preset", "Name of a GameDifficulty preset found in the GameDifficultyPresets folder"),
    "AdminOnlyDebugEvents": ("Admin Only Debug Events", "Enable debug events for admins only"),
    "DisableDebugEvents": ("Disable Debug Events", "Disable all debug events"),
    "APIEnabled": ("API Enabled", "Enable or disable the API"),
    "RconEnabled": ("RCON Enabled", "Enable or disable RCON"),
    "RconPort": ("RCON Port", "Port for RCON"),
    "RconPassword": ("RCON Password", "Password for RCON")
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
    create_row(host_settings_frame, label, host_config_vars[key], [], row, column, tooltip_text)
    if row > 30:  # Adjust number of rows before moving to the next column
        row = 0
        column += 2
    row += 1

# Adjust the window size dynamically based on the number of rows and columns
def adjust_window_size():
    game_rows = len(game_config_options)
    host_rows = len(host_config_options)
    max_columns = max(game_rows // 20, host_rows // 30) + 1
    root.geometry(f"{max_columns * 380}x{350 + max(game_rows, host_rows) * 5}")

# RCON Client GUI
tk.Label(rcon_frame, text="RCON Host:").grid(row=0, column=0, sticky='e')
rcon_host_var = tk.StringVar(value="127.0.0.1")
tk.Entry(rcon_frame, textvariable=rcon_host_var, width=40).grid(row=0, column=1, sticky='w')

tk.Label(rcon_frame, text="RCON Port:").grid(row=1, column=0, sticky='e')
rcon_port_var = tk.StringVar(value="25575")
tk.Entry(rcon_frame, textvariable=rcon_port_var, width=40).grid(row=1, column=1, sticky='w')

tk.Label(rcon_frame, text="RCON Password:").grid(row=2, column=0, sticky='e')
rcon_password_var = tk.StringVar(value="")
tk.Entry(rcon_frame, textvariable=rcon_password_var, width=40, show="*").grid(row=2, column=1, sticky='w')

tk.Button(rcon_frame, text="Connect", command=connect_rcon).grid(row=3, column=1, sticky='w')

tk.Label(rcon_frame, text="RCON Command:").grid(row=4, column=0, sticky='e')
rcon_command_var = tk.StringVar(value="")
tk.Entry(rcon_frame, textvariable=rcon_command_var, width=40).grid(row=4, column=1, sticky='w')

tk.Button(rcon_frame, text="Send Command", command=send_rcon_command).grid(row=5, column=1, sticky='w')

rcon_output_text = tk.Text(rcon_frame, height=10, width=80)
rcon_output_text.grid(row=6, column=0, columnspan=2)

# SteamCMD GUI
tk.Label(steamcmd_frame, text="SteamCMD Path:").grid(row=0, column=0, sticky='e')
steamcmd_path_var = tk.StringVar(value="C:/steamcmd/steamcmd.exe")
tk.Entry(steamcmd_frame, textvariable=steamcmd_path_var, width=40).grid(row=0, column=1, sticky='w')

tk.Label(steamcmd_frame, text="App ID:").grid(row=1, column=0, sticky='e')
app_id_var = tk.StringVar(value="1829350")  # Replace with V Rising's actual App ID
tk.Entry(steamcmd_frame, textvariable=app_id_var, width=40).grid(row=1, column=1, sticky='w')

tk.Label(steamcmd_frame, text="Install Directory:").grid(row=2, column=0, sticky='e')
install_dir_var = tk.StringVar(value="C:/steamcmd/steamapps/common/VRisingDedicatedServer")
tk.Entry(steamcmd_frame, textvariable=install_dir_var, width=40).grid(row=2, column=1, sticky='w')

tk.Button(steamcmd_frame, text="Install Server", command=install_server).grid(row=3, column=1, sticky='w')
tk.Button(steamcmd_frame, text="Update Server", command=update_server).grid(row=4, column=1, sticky='w')

# Add start and stop server buttons
tk.Button(steamcmd_frame, text="Start Server", command=start_server).grid(row=5, column=1, sticky='w')
tk.Button(steamcmd_frame, text="Stop Server", command=stop_server).grid(row=6, column=1, sticky='w')

instructions = """
1. Ensure you have a stable internet connection.
2. Click "Install Server" to download and install SteamCMD and the V Rising server.
3. If SteamCMD is not already installed, the tool will download and set it up for you.
4. Once SteamCMD is set up, the tool will automatically download the V Rising server files.
5. Click "Update Server" to update the server files to the latest version.
6. Use the "Start Server" and "Stop Server" buttons to control the server.
7. Check the console output for progress and any potential issues.
"""

tk.Label(steamcmd_frame, text=instructions, justify="left", wraplength=500).grid(row=7, column=0, columnspan=2, sticky='w')

# Console output
console_frame = ttk.Frame(root)
console_frame.pack(expand=1, fill="both")

console_text = tk.Text(console_frame, height=10, state=tk.DISABLED)
console_text.pack(expand=1, fill="both")

# Add a menu for loading and saving
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Load Game Settings", command=load_game_settings)
file_menu.add_command(label="Save Game Settings", command=update_game_settings)
file_menu.add_command(label="Load Host Settings", command=load_host_settings)
file_menu.add_command(label="Save Host Settings", command=update_host_settings)
file_menu.add_command(label="Check for Updates", command=check_for_updates)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Adjust the window size based on the content
adjust_window_size()

# Start the GUI event loop
root.mainloop()

