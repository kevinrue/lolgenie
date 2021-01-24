
var basic_history_chart = {
    hideRootNode: true,
    levelSeparation: 60,
    siblingSeparation: 6,
    subTeeSeparation: 12,
    animateOnInit: false,
    rootOrientation: "WEST",
    nodeAlign: "BOTTOM",
    connectors: {
        type: "step",
        style: {
            "stroke-width": 1,
            "arrow-end": "classic-wide-long",
        }
    },
    node: {
        HTMLclass: "node-class",
        collapsable: false
    }
}

function get_history_chart(container) {
    var chart = basic_history_chart;
    chart.container = container;
    return chart
}
