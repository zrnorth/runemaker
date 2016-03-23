"""
Contains the logic to make a role champ set based on player input.
"""
import championgg_api
import pprint

def make_champ_list(champ_stats, numRoles):
    """
    Construct a list of champions for a role, based on
    a variety of statistics.

    """
    # Basic: just get the top 5 by winrate.
    winrateSort = sorted(list(champ_stats), key=lambda x: (champ_stats[x]['winPercent']), reverse=True)

    return winrateSort[:5]

def get_role_stats(role):
    """
    Get the role statistics for each of the champs with the top 
    50 winrate in a role.
    """
    role_stats = {}
    rank_counter = 1
    # Get the top 50 champs by winrate for the role
    data = dict(championgg_api.get_stats_for_role(role))['data']
    for entry in data:
        # Fill out the entry with simple data at first.
        general = entry['general']
        champion = entry['key']
        
        champ_info = {}
        champ_info['winPercent'] = general['winPercent']
        champ_info['playPercent'] = general['playPercent']
        champ_info['banPercent'] = general['banRate']
        champ_info['overallPosition'] = general['overallPosition']
        champ_info['rank'] = rank_counter
        rank_counter += 1

        # For more complex data, we need to use a diff api call
        advanced_data_list = championgg_api.get_champion_data(champion)
        for item in advanced_data_list:
            if item['role'] == role:
                advanced_data = item
                break
        
        champ_info['pastPatchWinPercent'] = advanced_data['patchWin']
        champ_info['pastPatchPlayPercent'] = advanced_data['patchPlay']
        champ_info['winrateByExperience'] = advanced_data['experienceRate']
        champ_info['dmgComposition'] = advanced_data['dmgComposition']
        
        role_stats[champion] = champ_info


    return role_stats

def main():
    role = str(raw_input("Role? "))
    champ_stats = get_role_stats(role)

    top_five = make_champ_list(champ_stats, 5)
    print(top_five)

if __name__ == "__main__":
    main()
    input()
