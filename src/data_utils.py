from collections import Counter, OrderedDict
import copy

from . import configuration, other_utils, riot

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


def get_history_tree_data(last_matches, match_key):
    """
    Returns a TreantJS friendly dictionnary
    The returned dict can be directly parsed to json and used as input for TreantJS
    Ref: https://fperucic.github.io/treant-js/

    Input
        last_matches: list of matches containing the match_key (most recent first)
        match_key: key used for each node of the tree (ex: champion_name)
    """
    # TODO: Use recursion instead of hard coding levels 1, 2 and 3
    # TODO: Add winrate at each level

    # Compute data by entity (according to match_key; champions, lanes, ...)
    data = OrderedDict()
    default_dict = {"count": 0, "next": OrderedDict()}

    for i, match in enumerate(last_matches):
        # First level
        match_value = match.get(match_key, None)
        if match_value in [None, "NONE"]:
            # That can happen, for example if match_key = "lane", there are matches with no lane
            continue
        data.setdefault(match_value, copy.deepcopy(default_dict))
        data[match_value]["count"] += 1

        # Second level (get check next match)
        if i >= 1:
            l2_match = last_matches[i - 1]
            l2_match_value = l2_match.get(match_key, None)
            if l2_match_value in [None, "NONE"]:
                continue
            data[match_value]["next"].setdefault(
                l2_match_value, copy.deepcopy(default_dict)
            )
            data[match_value]["next"][l2_match_value]["count"] += 1

            # Third level (get check next match again)
            if i >= 2:
                l3_match = last_matches[i - 2]
                l3_match_value = l3_match.get(match_key, None)
                if l3_match_value in [None, "NONE"]:
                    continue
                data[match_value]["next"][l2_match_value]["next"].setdefault(
                    l3_match_value, copy.deepcopy(default_dict)
                )
                data[match_value]["next"][l2_match_value]["next"][l3_match_value][
                    "count"
                ] += 1

    # Sort data (most played champions on top)
    data = other_utils.sort_ordered_dict(data, "count", True)
    for l1_data in data.values():
        for l2_data in l1_data["next"].values():
            l2_data["next"] = other_utils.sort_ordered_dict(
                l2_data["next"], "count", True
            )
        l1_data["next"] = other_utils.sort_ordered_dict(l1_data["next"], "count", True)

    # Build tree data
    tree_data = {"text": {"name": "Root"}, "children": []}

    # First level
    for match_value, data in data.items():
        node_data = {
            "text": {
                "name": match_value,
                "title": f"Played {data['count']} time(s)",
            },
            "HTMLclass": "node-custom",
            "children": [],
        }
        image = riot.get_image_url(key=match_key, value=match_value)
        if image is not None:
            node_data["image"] = image
        # Second level
        for l2_match_value, l2_data in data["next"].items():
            l2_node_data = {
                "text": {
                    "name": l2_match_value,
                    "title": f"Played {l2_data['count']} time(s)",
                },
                "HTMLclass": "node-custom",
                "children": [],
            }
            image = riot.get_image_url(key=match_key, value=l2_match_value)
            if image is not None:
                l2_node_data["image"] = image
            # Third level
            for l3_match_value, l3_data in l2_data["next"].items():
                l3_node_data = {
                    "text": {
                        "name": l3_match_value,
                        "title": f"Played {l3_data['count']} time(s)",
                    },
                    "HTMLclass": "node-custom",
                    "children": [],
                }
                image = riot.get_image_url(key=match_key, value=l3_match_value)
                if image is not None:
                    l3_node_data["image"] = image
                l2_node_data["children"].append(l3_node_data)

            node_data["children"].append(l2_node_data)

        tree_data["children"].append(node_data)

    return tree_data
