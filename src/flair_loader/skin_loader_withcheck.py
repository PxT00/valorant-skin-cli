import json,os
from InquirerPy.utils import color_print

from ..content.skin_content import Skin_Content
from ..entitlements.entitlement_manager import Entitlement_Manager
from ..utility.logging import Logger
from ..utility.filepath import Filepath
from ..flair_management.skin_manager.skin_manager import Skin_Manager
debug = Logger.debug

class Skin_Loader:

    @staticmethod
    def sanitize_chroma_name(skin, chroma, weapon_name):
        try:
            new = chroma
            new = new.rstrip("\\r\\n")
            new = new.strip(weapon_name)
            new = new[new.find("(") + 1:new.find(")")]
            if new in skin['displayName']:
                new = "Base"
            return new
        except:
            return "Base"

    @staticmethod
    def sanitize_level_name(index, level, skin_name):
        try:
            if not "Standard" in skin_name:
                new = level 
                new = level.replace(skin_name,"").strip()
                if new == "":
                    return "Level 1"
                return new 
            else:
                return f"Level {index+1}"
        except:
            return f"Level {index+1}"

    @staticmethod
    def fetch_content_tier(tiers, uuid):

        # define skin tier indices for sorting skins

        tier_indices = {
            "Standard": 0,
            "Battlepass": 1,
            "Select": 2,
            "Deluxe": 3,
            "Premium": 4,
            "Exclusive": 5,
            "Ultra": 6,
        }

        tier_colors = {
            "Standard": "Grey",
            "Battlepass": "White",
            "Select": "Blue",
            "Deluxe": "Lime",
            "Premium": "Purple",
            "Ultra": "Yellow",
            "Exclusive": "DarkGoldenRod"
        }

        if uuid not in ('standard', 'bp'):
            for tier in tiers:
                if tier["uuid"] == uuid:
                    tier["index"] = tier_indices[tier["devName"]]
                    tier["highlightColor"] = tier_colors[tier["devName"]]
                    return tier
        elif uuid == "standard":
            return {
                "devName": "Standard",
                "highlightColor": tier_colors["Standard"],
                "index": tier_indices["Standard"]
            }
        elif uuid == "bp":
            return {
                "devName": "Battlepass",
                "highlightColor": tier_colors["Battlepass"],
                "index": tier_indices["Battlepass"]
            }

    @staticmethod
    def generate_skin_data(client):
        skin_level_entitlements = Entitlement_Manager.fetch_entitlements(client, "skin_level")
        skin_chroma_entitlements = Entitlement_Manager.fetch_entitlements(client, "skin_chroma")

        debug(f"skin entitlements: {skin_level_entitlements}")
        debug(f"chroma entitlements: {skin_chroma_entitlements}")
        content_tiers = Skin_Content.fetch_content_tiers()
        all_weapon_content = Skin_Content.fetch_weapons_data()

        existing_skin_data = {}
        # check integrity of existing skin data and/or if it exists
        # if not, start new data

        def failed_integrity():
            debug("skin data integrity check failed!")
            color_print( [("Yellow bold", "[!] verificação de integridade dos dados de skin falhou! Criando novo arquivo. ")])
            return Skin_Manager.generate_blank_skin_file()

        try:
            existing_skin_data = Skin_Manager.fetch_skin_data()
        except:
            existing_skin_data = failed_integrity()
        if existing_skin_data == {}:
            existing_skin_data = failed_integrity()

        new_skin_data = {}

        for weapon in all_weapon_content:
            # color_print([((f"[{weapon['displayName']}] generating skin data","green",attrs=["bold"])
            debug(f"generating skin data for {weapon['displayName']} ({weapon['uuid']})")

            weapon_uuid = weapon["uuid"]
            weapon_data = {
                "display_name": weapon["displayName"],
                "weapon_type": weapon["category"].replace('EEquippableCategory::', ''),
                "skins": {}
            }

            for skin in weapon["skins"]:
                debug(
                    f"checking data for {skin['displayName']} ({skin['uuid']})")
                if skin["displayName"] == "Melee":
                    # why is rito so inconsistent
                    skin["displayName"] = "Standard Melee"
                    skin["chromas"][0]["displayName"] = "Melee"
                    skin["levels"][0]["displayName"] = "Melee"

                skin_owned = False
                skin_previously_owned = False
                skin_uuid = skin["uuid"]
                skin_tier_data = Skin_Loader.fetch_content_tier(content_tiers, skin["contentTierUuid"] if skin["contentTierUuid"] is not None else "standard" if "Standard" in skin["displayName"] else "bp")

                for level in skin["levels"]:
                    for entitlement in skin_level_entitlements["Entitlements"]:
                        if level is not None and entitlement["ItemID"] == level["uuid"]:
                            debug(f"{skin['displayName']} is owned (entitlement: {entitlement})")
                            skin_owned = True
                            break

                if "Standard" in skin["displayName"]:
                    # enable if base skin
                    skin_owned = True

                if skin["uuid"] in existing_skin_data[weapon_uuid]["skins"]:
                    # check if there was already skin data in old backup file
                    debug(f"ja temos dados da {skin['displayName']} ({skin['uuid']})")
                    skin_previously_owned = True

                if skin_owned:
                    if not skin_previously_owned:
                        color_print([("Purple", f"[{weapon['displayName']}] nova skin encontrada!-> {skin['displayName']}")])

                    def check_attribute(key,default):
                        if skin_previously_owned:
                            if key in existing_skin_data[weapon_uuid]["skins"][skin_uuid].keys():
                                return existing_skin_data[weapon_uuid]["skins"][skin_uuid][key] 
                        return default

                    weapon_data["skins"][skin_uuid] = {
                        "display_name": skin["displayName"],
                        "enabled": check_attribute("enabled", False),
                        "weight": check_attribute("weight", 1),
                        "tier": {
                            "display_name": skin_tier_data["devName"],
                            "color": skin_tier_data["highlightColor"],
                            "tier_index": skin_tier_data["index"],
                        },
                        "levels": {},
                        "chromas": {},
                    }


                    for index, level in enumerate(skin["levels"]):
                        if level is not None:
                            debug(f"{skin['displayName']}/LEVEL: beginning processing of {level['displayName']} ({level['uuid']}) - {level}")
                            level_already_exists = skin_previously_owned and level["uuid"] in existing_skin_data[weapon_uuid]["skins"][skin_uuid]["levels"]

                            def process_skin_level():
                                debug(f"{skin['displayName']}/LEVEL: {level['displayName']} ({level['uuid']}) foi verificada")
                                if level_already_exists:
                                    weapon_data["skins"][skin_uuid]["levels"][level["uuid"]] = existing_skin_data[weapon_uuid]["skins"][skin_uuid]["levels"][level["uuid"]]

                                else:
                                    weapon_data["skins"][skin_uuid]["levels"][level["uuid"]] = {
                                        "display_name": f"{Skin_Loader.sanitize_level_name(index,level['displayName'],skin['displayName'])}" + (f" ({level['levelItem'].replace('EEquippableSkinLevelItem::', '')})" if level['levelItem'] is not None else "" if level["displayName"] == skin["displayName"].replace("Standard ", "") else " (VFX)" if level['displayName'] != skin['displayName'] else ""),
                                        "enabled": False
                                    }
                                    color_print([("DarkBlue", f"[{skin['displayName']}] encontrado novo dado de nível ({level['displayName']})")])

                            if level is not None and level["displayName"] == skin["displayName"].replace("Standard ", ""):
                                # if skin is standard
                                process_skin_level()
                            elif level_already_exists:
                                process_skin_level()
                            else:
                                for entitlement in skin_level_entitlements["Entitlements"]:
                                    if level is not None and entitlement["ItemID"] == level["uuid"]:
                                        process_skin_level()

                    for index, chroma in enumerate(skin["chromas"]):
                        if chroma is not None:
                            sanitized_chroma_name = Skin_Loader.sanitize_chroma_name(skin, chroma["displayName"], weapon["displayName"])
                            debug(f"{skin['displayName']}/CHROMA: iniciando o process {sanitized_chroma_name} ({chroma['uuid']}) - {chroma}")
                            chroma_already_exists = skin_previously_owned and chroma["uuid"] in existing_skin_data[weapon_uuid]["skins"][skin_uuid]["chromas"]

                            def process_chroma():
                                debug(f"{skin['displayName']}/CHROMA: {sanitized_chroma_name} ({chroma['uuid']}) foi verificada")
                                if chroma_already_exists:
                                    weapon_data["skins"][skin_uuid]["chromas"][chroma["uuid"]] = \
                                        existing_skin_data[weapon_uuid]["skins"][skin_uuid]["chromas"][chroma["uuid"]]
                                else:
                                    weapon_data["skins"][skin_uuid]["chromas"][chroma["uuid"]] = {
                                        "display_name": sanitized_chroma_name,
                                        "enabled": False
                                    }
                                    color_print([("#00b0ff", f"[{skin['displayName']}] encontrado mais dados de variante ({sanitized_chroma_name})")])

                            if chroma["displayName"] == skin["displayName"].replace("Standard ", ""):
                                process_chroma()
                            elif chroma["displayName"] in (skin["displayName"], None):
                                process_chroma()
                            elif len(skin["chromas"]) == 1:
                                process_chroma()
                            elif index == 0:
                                process_chroma()
                            elif chroma_already_exists:
                                process_chroma()
                            else:
                                for entitlement in skin_chroma_entitlements["Entitlements"]:
                                    if chroma is not None and entitlement["ItemID"] == chroma["uuid"]:
                                        process_chroma()

                    # enable base level/chroma
                    # print(weapon_data["skins"][skin_uuid])
                    if len([level["enabled"] for _,level in weapon_data["skins"][skin_uuid]["levels"].items() if level["enabled"]]) == 0:
                        weapon_data["skins"][skin_uuid]["levels"][list(weapon_data["skins"][skin_uuid]["levels"].keys())[-1]]['enabled'] = True
                    if len([chroma["enabled"] for _,chroma in weapon_data["skins"][skin_uuid]["chromas"].items() if chroma["enabled"]]) == 0:
                        weapon_data["skins"][skin_uuid]["chromas"][list(weapon_data["skins"][skin_uuid]["chromas"].keys())[-1]]['enabled'] = True

            # sort skins by tier index
            weapon_data["skins"] = dict(sorted(weapon_data["skins"].items(), key=lambda skin: skin[1]['tier']['tier_index'], reverse=True))
            new_skin_data[weapon_uuid] = weapon_data

        with open(Filepath.get_path(os.path.join(Filepath.get_appdata_folder(), 'skins.json')), 'w') as f:
            json.dump(new_skin_data, f)
            color_print([("Lime", "Skins carregadas!")])

    
    
