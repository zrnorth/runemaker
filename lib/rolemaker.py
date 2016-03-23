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

    return winrateSort[:numRoles]

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
        championInternalName = entry['key']
        champion = entry['name']
        
        champ_info = {}
        champ_info['winPercent'] = general['winPercent']
        champ_info['playPercent'] = general['playPercent']
        champ_info['banPercent'] = general['banRate']
        champ_info['overallPosition'] = general['overallPosition']
        champ_info['rank'] = rank_counter
        rank_counter += 1

        # For more complex data, we need to use a diff api call
        advanced_data_list = championgg_api.get_champion_data(championInternalName)

        for item in advanced_data_list:
            if item['role'] == role:
                advanced_data = item
                break
        
        champ_info['pastPatchWinPercent'] = advanced_data['patchWin']
        champ_info['pastPatchPlayPercent'] = advanced_data['patchPlay']
        champ_info['winrateByExperience'] = advanced_data['experienceRate']
       
        adDmg = advanced_data['dmgComposition']['physicalDmg']
        apDmg = advanced_data['dmgComposition']['magicDmg']
        trueDmg = advanced_data['dmgComposition']['trueDmg']

        # Could use tuning? Works for now.
        if (adDmg + trueDmg > 70):
            champ_info['dmgType'] = 'AD'
        elif (apDmg + trueDmg > 70):
            champ_info['dmgType'] = 'AP'
        else:
            champ_info['dmgType'] = 'Hybrid'

        role_stats[champion] = champ_info

    return role_stats

def main():
    role = str(raw_input("Role? "))
    num = int(raw_input("Number of champs? "))
    champ_stats = get_role_stats(role)

    top_five = make_champ_list(champ_stats, num)
    print(top_five)

if __name__ == "__main__":
    main()
    input()
