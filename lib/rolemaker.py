"""
Contains the logic to make a role champ set based on player input.
"""
import championgg_api
import util
import pprint

def make_champ_list(champ_stats, num):
    """
    Construct a list of champions for a role, based on
    a variety of statistics.

    """
    sort = sorted(list(champ_stats), key=lambda x: (champ_stats[x]['score']), reverse=True)

    return sort[:num]

def calculate_score(champ_info):
    """
    Calculate the 'score' for this champion, based on our weighting score system
    """
    weights = util.get_defined_champ_role_weights()

    score = 0
    score += champ_info['winrate'] * weights['winrate']
    score += champ_info['banrate'] * weights['banrate']
    score += champ_info['playrate'] * weights['playrate']

    return score

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
        champ_info['winrate'] = general['winPercent']
        champ_info['playrate'] = general['playPercent']
        champ_info['banrate'] = general['banRate']
        champ_info['overallPosition'] = general['overallPosition']
        champ_info['rank'] = rank_counter
        rank_counter += 1

        # For more complex data, we need to use a diff api call
        advanced_data_list = championgg_api.get_champion_data(championInternalName)

        for item in advanced_data_list:
            if item['role'] == role:
                advanced_data = item
                break
        
        champ_info['pastPatchWinrate'] = advanced_data['patchWin']
        champ_info['pastPatchPlayrate'] = advanced_data['patchPlay']
        champ_info['winrateByExperience'] = advanced_data['experienceRate']
       
        ad_dmg = advanced_data['dmgComposition']['physicalDmg']
        ap_dmg = advanced_data['dmgComposition']['magicDmg']
        true_dmg = advanced_data['dmgComposition']['trueDmg']

        # Could use tuning? Works for now.
        if (ad_dmg + true_dmg > 70):
            champ_info['dmgType'] = 'AD'
        elif (ap_dmg + true_dmg > 70):
            champ_info['dmgType'] = 'AP'
        else:
            champ_info['dmgType'] = 'Hybrid'
        
        champ_info['score'] = calculate_score(champ_info)

        print(champion + " | " + str(champ_info['score']))

        role_stats[champion] = champ_info

    return role_stats

def main():
    role = str(raw_input("Role? "))
    num = int(raw_input("Number of champs? "))
    champ_stats = get_role_stats(role)

    champ_list = make_champ_list(champ_stats, num)
    print(champ_list)

if __name__ == "__main__":
    main()
    input()
