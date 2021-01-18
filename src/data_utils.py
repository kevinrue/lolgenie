from collections import Counter, OrderedDict


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
