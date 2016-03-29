"""
Contains the logic to make a role champ set based on player input.
"""
import championgg_api
import pprint
import statistics
import time
import util

def make_champ_list(role_stats, num):
    """
    Construct a list of champions for a role, based on
    a variety of statistics.

    """
    return sorted(list(role_stats), key=lambda x: (role_stats[x]['score']), reverse=True)[:num]

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

def get_stats_for_field(role_stats, field):
    """
    Calculate some simple stats for a given field in our champ_stats dataset.
    """
    l = []
    for champ in role_stats:
        l.append(role_stats[champ][field])
    
    return {
        "mean": str(statistics.mean(l)),
        "median": str(statistics.median(l)),
        "stddev": str(statistics.stdev(l))
    }

def get_role_stats(role):
    """
    Get the role statistics for each of the champs with the top 
    50 winrate in a role.
    """
    role_stats = {}
    rank_counter = 1

    # Get the top 50 champs by winrate for the role
    response = dict(championgg_api.get_stats_for_role(role))
    # If got empty response, wait a second and try again
    while response is False:
        print("Got empty result. Retrying...")
        time.sleep(1)
        response = dict(championgg_api.get_stats_for_role(role))
    
    if 'error' in response:
        print(response['error']['message'])
        return {}

    data = response['data']
    for entry in data:
        # Fill out the entry with simple data at first.
        general = entry['general']
        championInternalName = entry['key']
        champion = entry['name']

        print(champion + "...")
        
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

        role_stats[champion] = champ_info
    
    # Now that we have iterated all the champ_roles, get some generalized stats
    agg_stats = {}
    agg_stats['winrate'] = get_stats_for_field(role_stats, 'winrate')
    agg_stats['playrate'] = get_stats_for_field(role_stats, 'playrate')
    agg_stats['banrate'] = get_stats_for_field(role_stats, 'banrate')

    # Finally, use these stats to calculate a score for each champ
    for champ in role_stats:
        role_stats[champ]['score'] = calculate_score(role_stats[champ])
        print(champ + " | " + str(role_stats[champ]))

    return (agg_stats, role_stats)

def main():
    role = str(raw_input("Role? "))
    num = int(raw_input("Number of champs? "))
    agg_stats, role_stats = get_role_stats(role)
    champ_list = make_champ_list(role_stats, num)
    print(champ_list)
    print(agg_stats)

if __name__ == "__main__":
    main()
    input()
