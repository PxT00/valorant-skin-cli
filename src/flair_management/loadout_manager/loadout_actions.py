from json import load
from InquirerPy.utils import color_print
from InquirerPy import inquirer 

from .loadouts_manager import Loadouts_Manager
from ..loadout_grid import Loadout_Grid

class Loadout_Actions:

    @staticmethod 
    def print_loadout(client,loadout_override=None):
        table, width = Loadout_Grid.fetch_loadout_grid(client,loadout_override)
        print()
        for row in table:
            color_print([weapon for weapon in row])

    @staticmethod
    def create_loadout(client):          

        color_print([("Blue bold","\nfaça um loadout!")])
        all_loadouts = Loadouts_Manager.fetch_all_loadouts()
        loadout_names = [loadout["name"] for loadout in all_loadouts]
        equipped_loadout = client.fetch_player_loadout()

        loadout_name = inquirer.text(
            message="Nomeie esse loadout:",
            validate=lambda response: isinstance(response, str) and not response in loadout_names and not response == "" and response is not None,
            invalid_message="Nome inválido! (Já existe ou nome vazio)"
        ).execute()

        color_print([("Blue bold", "\nPré-visualização:")])
        Loadout_Actions.print_loadout(client)

        confirm = inquirer.confirm(message=f"Você quer salvar esse loadout como: '{loadout_name}'?", default=True).execute()
        if confirm:
            loadout = {
                "name": loadout_name,
                "enabled": True,
                "Guns": equipped_loadout["Guns"],
                "Sprays": equipped_loadout["Sprays"],
                "Identity": {
                    "PlayerCardID": equipped_loadout["Identity"]["PlayerCardID"],
                    "PlayerTitleID": equipped_loadout["Identity"]["PlayerTitleID"],
                }
            }

            Loadouts_Manager.add_loadout(loadout)
            color_print([("LimeGreen",f"Loadout '{loadout_name}' salvo!"),("Blue","\ndigite "),("White",f"loadout equip {loadout_name.replace(' ', '-')}"),("Blue", " para equipá-lo")]) 

    @staticmethod 
    def equip_loadout(loadout_name, client):
        loadouts = Loadouts_Manager.fetch_all_loadouts()
        for loadout in loadouts:
            if loadout["name"] == loadout_name:
                new_loadout = client.fetch_player_loadout()
                new_loadout["Guns"] = loadout["Guns"]
                new_loadout["Sprays"] = loadout["Sprays"]
                new_loadout["Identity"]["PlayerCardID"] = loadout["Identity"]["PlayerCardID"]
                new_loadout["Identity"]["PlayerTitleID"] = loadout["Identity"]["PlayerTitleID"]
                client.put_player_loadout(new_loadout)
                color_print([("LimeGreen bold",f"Equipado com sucesso! {loadout_name}!")])

    @staticmethod 
    def delete_loadout(loadout_name):
        all_loadouts = Loadouts_Manager.remove_loadout(loadout_name)
        new_loadout_names = [loadout["name"] for loadout in all_loadouts]
        color_print([("LimeGreen",f"Deletado com sucesso! {loadout_name}!")])
        if len(new_loadout_names) > 0:
            color_print([("LimeGreen","\nSua lista de loadouts:\n"),("Blue","\n".join(f"- {name}" for name in new_loadout_names))])
