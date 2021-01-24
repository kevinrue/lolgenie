from collections import Counter, OrderedDict
import copy

from . import configuration, other_utils

settings = configuration.settings

colors_to_rgb = {
    "red": "rgb(255, 99, 132)",
    "orange": "rgb(255, 159, 64)",
    "yellow": "rgb(255, 205, 86)",
    "green": "rgb(75, 192, 192)",
    "blue": "rgb(54, 162, 235)",
    "purple": "rgb(153, 102, 255)",
    "grey": "rgb(201, 203, 207)",
}


def most_played_champs_plot_data(last_matches):
    """
    Returns a ChartJS friendly dictionary to use as JSON in template (data)
    """
    # Get most played champions as a Counter object
    champions_counter = Counter()

    for match in last_matches["matches"]:
        champions_counter[match["champion_name"]] += 1

    champions_counter_ordered = OrderedDict(champions_counter.most_common())

    # Populate the data dict for ChartJS
    data = {
        "labels": list(champions_counter_ordered.keys()),
        "datasets": [
            {
                "data": list(champions_counter_ordered.values()),
                "label": "Played",
                "backgroundColor": colors_to_rgb["red"],
                "borderColor": colors_to_rgb["red"],
            }
        ],
    }

    return data


def get_history_tree_champ_data(last_matches):
    """
    Returns a TreantJS friendly dictionnary
    The returned dict can be directly parsed to json and used as input for TreantJS
    Ref: https://fperucic.github.io/treant-js/

    Input
        last_matches: list of matches containing champion data (most recent first)
    """
    # TODO: Use recursion instead of hard coding levels 1, 2 and 3
    # TODO: Add winrate at each level

    # Compute champions data
    champions_played = OrderedDict()
    default_dict = {"count": 0, "next": OrderedDict()}

    for i, match in enumerate(last_matches):
        # First level
        champ_name = match["champion_name"]
        champions_played.setdefault(champ_name, copy.deepcopy(default_dict))
        champions_played[champ_name]["count"] += 1

        # Second level (get check next match)
        if i >= 1:
            l2_match = last_matches[i - 1]
            l2_champ_name = l2_match["champion_name"]
            champions_played[champ_name]["next"].setdefault(
                l2_champ_name, copy.deepcopy(default_dict)
            )
            champions_played[champ_name]["next"][l2_champ_name]["count"] += 1

            # Third level (get check next match again)
            if i >= 2:
                l3_match = last_matches[i - 2]
                l3_champ_name = l3_match["champion_name"]
                champions_played[champ_name]["next"][l2_champ_name]["next"].setdefault(
                    l3_champ_name, copy.deepcopy(default_dict)
                )
                champions_played[champ_name]["next"][l2_champ_name]["next"][
                    l3_champ_name
                ]["count"] += 1

    # Sort data (most played champions on top)
    champions_played = other_utils.sort_ordered_dict(champions_played, "count", True)
    for l1_data in champions_played.values():
        for l2_data in l1_data["next"].values():
            l2_data["next"] = other_utils.sort_ordered_dict(
                l2_data["next"], "count", True
            )
        l1_data["next"] = other_utils.sort_ordered_dict(l1_data["next"], "count", True)

    # Build tree data
    tree_data = {"text": {"name": "Root"}, "children": []}

    # First level
    for champ_name, champ_data in champions_played.items():
        node_data = {
            "text": {
                "name": champ_name,
                "title": f"Played {champ_data['count']} time(s)",
            },
            "image": f"http://ddragon.leagueoflegends.com/cdn/{settings.latest_release}/img/champion/{champ_name}.png",
            "HTMLclass": "node-champion",
            "children": [],
        }
        # Second level
        for l2_champ_name, l2_champ_data in champ_data["next"].items():
            l2_node_data = {
                "text": {
                    "name": l2_champ_name,
                    "title": f"Played {l2_champ_data['count']} time(s)",
                },
                "image": f"http://ddragon.leagueoflegends.com/cdn/{settings.latest_release}/img/champion/{l2_champ_name}.png",
                "HTMLclass": "node-champion",
                "children": [],
            }
            # Third level
            for l3_champ_name, l3_champ_data in l2_champ_data["next"].items():
                l3_node_data = {
                    "text": {
                        "name": l3_champ_name,
                        "title": f"Played {l3_champ_data['count']} time(s)",
                    },
                    "image": f"http://ddragon.leagueoflegends.com/cdn/{settings.latest_release}/img/champion/{l3_champ_name}.png",
                    "HTMLclass": "node-champion",
                    "children": [],
                }
                l2_node_data["children"].append(l3_node_data)

            node_data["children"].append(l2_node_data)

        tree_data["children"].append(node_data)

    return tree_data
