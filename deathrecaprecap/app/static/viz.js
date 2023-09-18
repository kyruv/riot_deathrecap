resizeTimeout = false;

function loadNewMatch(new_data) {
    persisted_data = {
        all_death_data: new_data["all_deaths"],
        aggregate_placeholder: new_data["aggregate_placeholder"],
        focus: "overview",
        game_end_time: new_data["meta_data"]["end_time"],
        start: 0,
        end: new_data["meta_data"]["end_time"],
        damage_breakdown: "type",
        dimensions: {
            margin: { top: 150, right: 100, bottom: 20, left: 100 },
            width: $(window).width() - 300,
            height: Math.max(700, $(window).height() - 170),
        },
    };

    reload(persisted_data);
}

function reload(persisted_data) {
    // Stick the resize callback here so it has access to the most recent persisted_data
    $(window).resize(function () {
        if (resizeTimeout !== false) {
            clearTimeout(resizeTimeout);
        }
        resizeTimeout = setTimeout(function () {
            persisted_data["dimensions"] = {
                margin: { top: 150, right: 100, bottom: 20, left: 100 },
                width: Math.max(500, $(window).width() - 300),
                height: Math.max(700, $(window).height() - 170),
            };
            reload(persisted_data);
        }, 150);
    });


    // Extract variables from persisted_data for easier use
    var all_death_data = persisted_data["all_death_data"];
    var aggregate_placeholder = persisted_data["aggregate_placeholder"];
    var focus = persisted_data["focus"];
    var start = persisted_data["start"];
    var end = persisted_data["end"];
    var margin = persisted_data["dimensions"]["margin"];
    var width = persisted_data["dimensions"]["width"];
    var height = persisted_data["dimensions"]["height"];

    // Other extra variables
    var foreground_color = "white";

    // ---- Data Preparation ----
    var data = aggregate_death_data(all_death_data, aggregate_placeholder, start, end);
    var draw_data = prepare_data(data, focus);

    // ---- D3 Drawing Below ----
    // 1. Clear SVG
    d3.selectAll("svg").remove();
    d3.select("#tooltip").remove();

    // 2. Create base SVG + tooltip
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);
    var tooltip = d3.select("#my_dataviz")
        .append("div")
        .attr("id", "tooltip")
        .attr("style", "outline: thin solid white;")
        .style("position", "absolute")
        .style("background", "rgb(30, 32, 39)")
        .style("padding", "5px")
        .style("visibility", "hidden");

    // 3. Draw static dividing lines
    svg.append('line')
        .style("stroke", foreground_color)
        .style("stroke-width", 5)
        .attr("x1", margin.left / 2)
        .attr("y1", 115)
        .attr("x2", width + 1.5 * margin.right)
        .attr("y2", 115);
    svg.append('line')
        .style("stroke", foreground_color)
        .style("stroke-width", 2)
        .attr("x1", margin.left + width / 2)
        .attr("y1", 115)
        .attr("x2", margin.left + width / 2)
        .attr("y2", .75 * height + margin.top - margin.bottom);

    // 4. Draw the header
    d3_drawHeader(svg, focus, foreground_color, persisted_data);

    // 5. Setup where we will primarily draw the data
    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // 6. setup the shared domain for the bars
    var xdomain = [0, d3.max(draw_data, function (d) {
        return d.total;
    })];

    // 7. Draw the blue team data
    data_blue = draw_data.slice(6);
    d3_drawDeathBars(data_blue, g, tooltip, persisted_data, xdomain, is_left = true);

    // 8. Draw the red team data
    data_red = draw_data.slice(0, 6);
    d3_drawDeathBars(data_red, g, tooltip, persisted_data, xdomain, is_left = false);

    // 9. Draw the timeline
    d3_drawTimeline(svg, foreground_color, tooltip, persisted_data);
}





// ---------------------------------------------------
// --------- D3.js logic helper functions ------------
// ---------------------------------------------------

function d3_drawDeathBars(death_data, g, tooltip, persisted_data, xdomain, is_left) {
    var height = persisted_data["dimensions"]["height"];
    var damage_breakdown = persisted_data["damage_breakdown"];
    var focus = persisted_data["focus"];
    var damage_breakdown = persisted_data["damage_breakdown"];
    var width = persisted_data["dimensions"]["width"];

    var x = d3.scaleLinear()
        .range([0, width / 2 - 5])
        .domain(xdomain);
    var y = d3.scaleBand()
        .range([.8 * height, 0])
        .domain(death_data.map(function (d, i) { return d.name; }))
        .paddingInner(0.05)
        .align(0.1);
    var z; // depends on damage_breakdown, set below    
    var keys = [];
    if (damage_breakdown == "type") {
        z = d3.scaleOrdinal()
            .range(["indianred", "royalblue", "gainsboro"]);
        keys = ["physical", "magic", "true"];
    } else if (damage_breakdown == "spell") {
        z = d3.scaleOrdinal().range(["#d73027", "#fc8d59", "#fee090", "#e0f3f8", "#91bfdb", "#4575b4"]);
        keys = ["aa", "q", "w", "e", "r", "other"];
    }

    y;
    g.selectAll(".label")
        .data(death_data)
        .enter()
        .append("text")
        .text(function (d) {
            var label = "";
            if (d.takedowns > 1) {
                label = d.total.toLocaleString("en-US") + " (" + d.takedowns + " takedowns)";
            } else if (d.takedowns == 1) {
                label = d.total.toLocaleString("en-US") + " (1 takedown)";
            } else {
                label = d.total.toLocaleString("en-US") + " (0 takedowns)";
            }
            return label;
        })
        .attr("x", function (d, i) { return 0; })
        .attr("y", function (d) { return y(d.name) - 5; })
        .style("font-size", "17px")
        .attr("transform", function (d) {
            if (is_left) {
                return "translate(0, 0)";
            }

            var label = "";
            if (d.takedowns > 1) {
                label = d.total.toLocaleString("en-US") + " (" + d.takedowns + " takedowns)";
            } else if (d.takedowns == 1) {
                label = d.total.toLocaleString("en-US") + " (1 takedown)";
            } else {
                label = d.total.toLocaleString("en-US") + " (0 takedowns)";
            }
            return "translate(" + (width - BrowserText.getWidth(label, 17)) + ", 0)";
        });
    g.selectAll(".images")
        .data(death_data)
        .enter()
        .append("svg:image")
        .attr("style", "outline: thin solid white;")
        .attr("x", function (d, i) { return x(0) - (Math.min(70, height / 11) + 10); })
        .attr("y", function (d) { return y(d.name); })
        .attr('width', Math.min(70, height / 11))
        .attr('height', Math.min(70, height / 11))
        .attr("xlink:href", function (d) {
            return document.getElementById(d.name + ".png").getAttribute("data-img-url");
        })
        .on("click", function (d) {
            persisted_data["focus"] = d.name;
            return reload(persisted_data);
        })
        .attr("transform", function () {
            if (is_left) {
                return "translate(0,0)";
            }
            return "translate(" + (width + 100) + ",0)";
        })
        .style('cursor', 'pointer');
    g.selectAll(".bar")
        .data(d3.stack().keys(keys)(death_data))
        .enter().append("g")
        .attr("fill", function (d) { return z(d.key); })
        .selectAll("rect").data(function (d) { return d; })
        .enter().append("rect")
        .attr("x", function (d, i) { return x(d[0]); })
        .attr("y", function (d) { return y(d.data.name); })
        .attr("width", function (d) { return x(d[1] - d[0]); })
        .attr("height", Math.min(70, height / 11))
        .attr("transform", function () {
            if (is_left) {
                return "scale(1,1)";
            }
            return "scale(-1, 1) translate(-" + width + ", 0)";
        })
        .on("click", function (d) {
            if (persisted_data["damage_breakdown"] == "spell") {
                persisted_data["damage_breakdown"] = "type";
            } else {
                persisted_data["damage_breakdown"] = "spell";
            }
            return reload(persisted_data);
        })
        .on("mouseover", function (d) {
            var label = "" + d3.select(this.parentNode).datum().key;
            if (d.data["name"] == "NPC100" || d.data["name"] == "NPC200" || focus == "NPC100" || focus == "NPC200") {
                if (label == "aa") {
                    label = "Turret";
                }
                if (label == "q") {
                    label = "Minion";
                }
                if (label == "w") {
                    label = "Monster";
                }
            }
            if (label == "other") {
                label += " (" + d.data.other_names + ")";
            }
            label = (d[1] - d[0]).toLocaleString("en-US") + " " + label;
            return tooltip.style("visibility", "visible")
                .text(label);
        })
        .on("mousemove", function () {
            return tooltip.style("left", (d3.event.x + 20) + "px").style("top", (d3.event.y - 20) + "px")
        })
        .on("mouseout", function (event) { return tooltip.style("visibility", "hidden"); });
}

function d3_drawHeader(svg, focus, foreground_color, persisted_data) {
    var focus = persisted_data["focus"];
    var width = persisted_data["dimensions"]["width"];
    var height = persisted_data["dimensions"]["height"];
    var margin = persisted_data["dimensions"]["margin"];

    if (focus == "overview") {
        var title = svg.append("g");
        title
            .append("text")
            .text("Critical Damage Dealt Overview")
            .attr("color", foreground_color)
            .attr("text-anchor", "middle")
            .style("font-size", "50px")
            .attr("x", 125 + width / 2)
            .attr("y", 50);
        title
            .append("text")
            .text("aka damage that contributed to a kill")
            .attr("text-anchor", "middle")
            .style("font-size", "24px")
            .attr("x", 125 + width / 2)
            .attr("y", 80);
    }
    else {
        var title = svg.append("g");
        title.append("svg:image")
            .attr('width', Math.min(90, height / 6))
            .attr('height', Math.min(90, height / 6))
            .attr("style", "outline: thin solid white;")
            .attr("xlink:href", document.getElementById(focus + ".png").getAttribute("data-img-url"))
            .attr("y", 2);
        title
            .append("text")
            .text(function () {
                if (focus == "NPC200") {
                    return "Red NPCs";
                }
                if (focus == "NPC100") {
                    return "Blue NPCs";
                }
                return focus;
            })
            .style("font-size", "50px")
            .attr("x", Math.min(90, height / 6) + 5)
            .attr("y", 72);
        title.attr("transform", "translate(" + (width / 2 + margin.left - (title.node().getBBox().width / 2)) + ",0)");

        svg.append("g").append("svg:image")
            .attr('width', Math.min(80, height / 8))
            .attr('height', Math.min(80, height / 8))
            .attr("xlink:href", document.getElementById("overview.png").getAttribute("data-img-url"))
            .attr("y", 2)
            .on("click", function (d) {
                persisted_data["focus"] = "overview";
                return reload(persisted_data);
            })
            .style('cursor', 'pointer');

        svg.append("g").append("text")
            .text("Champions I killed")
            .attr("text-anchor", "middle")
            .style("font-size", "28px")
            .attr("x", margin.left + BrowserText.getWidth("Champions I killed", 28) / 2)
            .attr("y", 105);

        svg.append("g").append("text")
            .text("Champions who killed me")
            .attr("text-anchor", "right")
            .style("font-size", "28px")
            .attr("x", width + margin.right - BrowserText.getWidth("Champions who killed me", 28))
            .attr("y", 105);
    }
}

function d3_drawTimeline(svg, foreground_color, tooltip, persisted_data) {
    var all_death_data = persisted_data["all_death_data"];
    var aggregate_placeholder = persisted_data["aggregate_placeholder"];
    var start = persisted_data["start"]
    var end = persisted_data["end"]
    var game_end_time = persisted_data["game_end_time"]
    var margin = persisted_data["dimensions"]["margin"]
    var width = persisted_data["dimensions"]["width"]
    var height = persisted_data["dimensions"]["height"]
    var tx = margin.left,
        ty = margin.top + height * .8;

    var tscalex = d3.scaleLinear().range([0, width]).domain([0, game_end_time]);

    var tscalez = d3.scaleOrdinal().range(["#2d5ff5", "#db4e4e"]).domain([0, 1]);
    var tscalezout = d3.scaleOrdinal().range(["#6483DD", "#d79c9c"]).domain([0, 1]);
    var tscaley = d3.scaleLinear()
        .range([0, 100])
        .domain([0, 5]);

    var pos_map = {};
    var team_map = {}
    Object.keys(aggregate_placeholder).forEach(function (key, i) {
        pos_map[key] = i % 6;
        team_map[key] = i < 6 ? 0 : 1;
    });

    var timeline = svg.append("g");
    timeline
        .append("rect")
        .attr("x", tx)
        .attr("y", ty)
        .attr("width", width)
        .attr("height", 100)
        .attr("fill", "grey");
    timeline
        .append('line')
        .style("stroke", "darkgrey")
        .style("stroke-width", 1)
        .attr("x1", tx)
        .attr("y1", ty + 20)
        .attr("x2", tx + width)
        .attr("y2", ty + 20)
    timeline
        .append('line')
        .style("stroke", "darkgrey")
        .style("stroke-width", 1)
        .attr("x1", tx)
        .attr("y1", ty + 40)
        .attr("x2", tx + width)
        .attr("y2", ty + 40)
    timeline
        .append('line')
        .style("stroke", "darkgrey")
        .style("stroke-width", 1)
        .attr("x1", tx)
        .attr("y1", ty + 60)
        .attr("x2", tx + width)
        .attr("y2", ty + 60)
    timeline
        .append('line')
        .style("stroke", "darkgrey")
        .style("stroke-width", 1)
        .attr("x1", tx)
        .attr("y1", ty + 80)
        .attr("x2", tx + width)
        .attr("y2", ty + 80);

    timeline
        .append("line")
        .attr("class", "leftbar")
        .style("stroke", foreground_color)
        .style("stroke-width", 4)
        .attr("x1", tx - 2 + tscalex(start))
        .attr("y1", ty - 10)
        .attr("x2", tx - 2 + tscalex(start))
        .attr("y2", ty + 110)
        .style('cursor', 'pointer');
    timeline.append('text')
        .attr("class", "leftbarlabel")
        .text(formatGameTime(start))
        .attr("color", foreground_color)
        .attr("text-anchor", "middle")
        .style("font-size", "18px")
        .attr("x", tx - 22 + tscalex(start))
        .attr("y", ty + 130);
    var startDragHandler = d3.drag()
        .on("drag", function () {
            if (d3.event.x < tx || d3.event.x > tx + width || d3.event.x > (tx + tscalex(end) - 10)) {
                return;
            }

            d3.select(this)
                .attr("x1", d3.event.x)
                .attr("x2", d3.event.x);

            start = tscalex.invert(d3.event.x - tx);

            d3.select('.leftbarlabel')
                .attr("x", d3.event.x - 22)
                .text(formatGameTime(start));
            d3.select('.rightbarlabel').style("font-size", "18px");
        })
        .on("end", function (d) {
            persisted_data["start"] = start;
            persisted_data["end"] = end;
            return reload(persisted_data);
        });
    startDragHandler(svg.selectAll(".leftbar"));

    timeline
        .append("line")
        .attr("class", "rightbar")
        .style("stroke", foreground_color)
        .style("stroke-width", 4)
        .attr("x1", tx + 2 + tscalex(end))
        .attr("y1", ty - 10)
        .attr("x2", tx + 2 + tscalex(end))
        .attr("y2", ty + 110)
        .style('cursor', 'pointer')
        .style("fill", foreground_color);
    timeline.append('text')
        .attr("class", "rightbarlabel")
        .text(formatGameTime(end))
        .attr("color", foreground_color)
        .attr("text-anchor", "middle")
        .style("font-size", function () {
            if (start == end) {
                return "0px";
            }
            return "18px";
        })
        .attr("x", tx + 22 + tscalex(end))
        .attr("y", ty + 130);
    var endDragHandler = d3.drag()
        .on("drag", function () {
            if (d3.event.x < tx || d3.event.x > tx + width || d3.event.x < (tx + tscalex(start) + 10)) {
                return;
            }

            d3.select(this)
                .attr("x1", d3.event.x)
                .attr("x2", d3.event.x);

            end = tscalex.invert(d3.event.x - tx);

            d3.select('.rightbarlabel')
                .attr("x", d3.event.x + 22)
                .text(formatGameTime(end));
            d3.select('.rightbarlabel').style("font-size", "18px");
        })
        .on("end", function (d) {
            persisted_data["start"] = start;
            persisted_data["end"] = end;
            return reload(persisted_data);
        });
    endDragHandler(svg.selectAll(".rightbar"));

    timeline.selectAll(".deaths")
        .data(all_death_data)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return tx + tscalex(d.timestamp);
        })
        .attr("cy", function (d) {
            return ty + 10 + tscaley(pos_map[d.who]);
        })
        .attr("r", 7)
        .attr("fill", function (d) {
            if (d.timestamp < start || d.timestamp > end) {
                return tscalezout(team_map[d.who]);
            }
            return tscalez(team_map[d.who]);
        })
        .on("click", function (d) {
            if (d.timestamp == start && d.timestamp == end) {
                d3.select('.rightbarlabel').style("font-size", "18px");
                persisted_data["start"] = 0;
                persisted_data["end"] = persisted_data["game_end_time"];
                return reload(persisted_data);
            }

            d3.select('.rightbarlabel').style("font-size", "0px");
            persisted_data["start"] = d.timestamp;
            persisted_data["end"] = d.timestamp;
            return reload(persisted_data);
        })
        .style('cursor', 'pointer')
        .on("mouseover", function (d) {
            return tooltip.style("visibility", "visible")
                .style("font-size", "12px")
                .text(d.who + " ... killed by ... " + d.killers.map(killer => " " + killer.who).toString());
        })
        .on("mousemove", function () {
            return tooltip.style("left", (d3.event.x + 20) + "px").style("top", (d3.event.y - 20) + "px")
        })
        .on("mouseout", function (event) { return tooltip.style("visibility", "hidden").style("font-size", "18px"); });

    var marker_time = 300000;
    var intervals = [];
    while (marker_time < game_end_time) {
        intervals.push({
            "x": tx + tscalex(marker_time),
            "y": ty + 100
        });
        marker_time += 300000;
    }

    timeline.selectAll("gametimeticks")
        .data(intervals)
        .enter()
        .append("line")
        .attr("x1", function (d) {
            return d["x"];
        })
        .attr("y1", function (d) {
            return d["y"];
        })
        .attr("x2", function (d) {
            return d["x"];
        })
        .attr("y2", function (d) {
            return d["y"] + 10;
        })
        .style("stroke", "white")
        .style("stroke-width", 2);
}

// ---------------------------------------------------
// ------ Data transformation helper functions -------
// ---------------------------------------------------

// Fill out the aggregate_placeholder with data from deaths 
// in the range [start, end]
function aggregate_death_data(all_death_data, aggregate_placeholder, start, end) {
    var aggregated_data_copy = JSON.parse(JSON.stringify(aggregate_placeholder));
    all_death_data.forEach(death => {
        if (death.timestamp < start || death.timestamp > end) {
            return;
        }

        var victim = death["who"];

        death["killers"].forEach(killer_info => {
            var killer = killer_info["who"];
            var physical = killer_info["physical"];
            var magic = killer_info["magic"];
            var trued = killer_info["true"];
            var total = physical + magic + trued;
            var aa = killer_info["aa"];
            var q = killer_info["q"];
            var w = killer_info["w"];
            var e = killer_info["e"];
            var r = killer_info["r"];
            var other = killer_info["other"];
            var other_names = killer_info["other_names"];

            aggregated_data_copy[killer]["as_killer"]["aggregate"]["total"] += total;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["physical"] += physical;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["magic"] += magic;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["true"] += trued;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["aa"] += aa;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["q"] += q;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["w"] += w;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["e"] += e;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["r"] += r;
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["other"] += other;
            existing_other_names = new Set(aggregated_data_copy[killer]["as_killer"]["aggregate"]["other_names"])
            other_names.forEach(spell => existing_other_names.add(spell));
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["other_names"] = Array.from(existing_other_names);
            aggregated_data_copy[killer]["as_killer"]["aggregate"]["takedowns"] += 1;

            aggregated_data_copy[killer]["as_killer"][victim]["total"] += total;
            aggregated_data_copy[killer]["as_killer"][victim]["physical"] += physical;
            aggregated_data_copy[killer]["as_killer"][victim]["magic"] += magic;
            aggregated_data_copy[killer]["as_killer"][victim]["true"] += trued;
            aggregated_data_copy[killer]["as_killer"][victim]["aa"] += aa;
            aggregated_data_copy[killer]["as_killer"][victim]["q"] += q;
            aggregated_data_copy[killer]["as_killer"][victim]["w"] += w;
            aggregated_data_copy[killer]["as_killer"][victim]["e"] += e;
            aggregated_data_copy[killer]["as_killer"][victim]["r"] += r;
            aggregated_data_copy[killer]["as_killer"][victim]["other"] += other;
            existing_other_names = new Set(aggregated_data_copy[killer]["as_killer"][victim]["other_names"])
            other_names.forEach(spell => existing_other_names.add(spell));
            aggregated_data_copy[killer]["as_killer"][victim]["other_names"] = Array.from(existing_other_names);
            aggregated_data_copy[killer]["as_killer"][victim]["takedowns"] += 1;

            aggregated_data_copy[victim]["as_victim"][killer]["total"] += total;
            aggregated_data_copy[victim]["as_victim"][killer]["physical"] += physical;
            aggregated_data_copy[victim]["as_victim"][killer]["magic"] += magic;
            aggregated_data_copy[victim]["as_victim"][killer]["true"] += trued;
            aggregated_data_copy[victim]["as_victim"][killer]["aa"] += aa;
            aggregated_data_copy[victim]["as_victim"][killer]["q"] += q;
            aggregated_data_copy[victim]["as_victim"][killer]["w"] += w;
            aggregated_data_copy[victim]["as_victim"][killer]["e"] += e;
            aggregated_data_copy[victim]["as_victim"][killer]["r"] += r;
            aggregated_data_copy[victim]["as_victim"][killer]["other"] += other;
            existing_other_names = new Set(aggregated_data_copy[victim]["as_victim"][killer]["other_names"])
            other_names.forEach(spell => existing_other_names.add(spell));
            aggregated_data_copy[victim]["as_victim"][killer]["other_names"] = Array.from(existing_other_names);
            aggregated_data_copy[victim]["as_victim"][killer]["takedowns"] += 1;
        });

    });

    var listified = [];
    Object.entries(aggregated_data_copy).forEach(([k, v]) => {
        v["name"] = k;
        listified.push(v);
    });

    return listified;
}

// prepare the aggregated data in the way it is needed for d3.js to use it
function prepare_data(data, focus) {
    prepared_data = []
    if (focus == "overview") {
        data.forEach(function (d) {
            prepared_data.push({
                "name": d["name"],
                "total": d["as_killer"]["aggregate"]["total"],
                "physical": d["as_killer"]["aggregate"]["physical"],
                "magic": d["as_killer"]["aggregate"]["magic"],
                "true": d["as_killer"]["aggregate"]["true"],
                "aa": d["as_killer"]["aggregate"]["aa"],
                "q": d["as_killer"]["aggregate"]["q"],
                "w": d["as_killer"]["aggregate"]["w"],
                "e": d["as_killer"]["aggregate"]["e"],
                "r": d["as_killer"]["aggregate"]["r"],
                "other": d["as_killer"]["aggregate"]["other"],
                "takedowns": d["as_killer"]["aggregate"]["takedowns"],
                "other_names": d["as_killer"]["aggregate"]["other_names"],
            });
        });
        return prepared_data.reverse();
    }
    else {
        // focus is a specific champ
        prepared_data = []
        data.forEach(function (d) {
            if (d.name == focus) {

                for (key in d["as_killer"]) {
                    if (key != "aggregate") {
                        prepared_data.push({
                            "name": key,
                            "total": d["as_killer"][key]["total"],
                            "physical": d["as_killer"][key]["physical"],
                            "magic": d["as_killer"][key]["magic"],
                            "true": d["as_killer"][key]["true"],
                            "aa": d["as_killer"][key]["aa"],
                            "q": d["as_killer"][key]["q"],
                            "w": d["as_killer"][key]["w"],
                            "e": d["as_killer"][key]["e"],
                            "r": d["as_killer"][key]["r"],
                            "other": d["as_killer"][key]["other"],
                            "takedowns": d["as_killer"][key]["takedowns"],
                            "other_names": d["as_killer"][key]["other_names"],
                        });
                    }
                }
                for (key in d["as_victim"]) {
                    if (key != "aggregate") {
                        prepared_data.push({
                            "name": key,
                            "total": d["as_victim"][key]["total"],
                            "physical": d["as_victim"][key]["physical"],
                            "magic": d["as_victim"][key]["magic"],
                            "true": d["as_victim"][key]["true"],
                            "aa": d["as_victim"][key]["aa"],
                            "q": d["as_victim"][key]["q"],
                            "w": d["as_victim"][key]["w"],
                            "e": d["as_victim"][key]["e"],
                            "r": d["as_victim"][key]["r"],
                            "other": d["as_victim"][key]["other"],
                            "takedowns": d["as_victim"][key]["takedowns"],
                            "other_names": d["as_victim"][key]["other_names"],
                        });
                    }
                }

            }

        });

        return prepared_data.reverse();
    }
};

// ---------------------------------------------------
// ---------- Formatting Helper Functions ------------
// ---------------------------------------------------

function formatGameTime(millis) {
    var minutes = Math.floor(millis / 60000);
    var seconds = ((millis % 60000) / 1000).toFixed(0);
    return (
        seconds == 60 ?
            (minutes + 1) + ":00" :
            minutes + ":" + (seconds < 10 ? "0" : "") + seconds
    );
};

var BrowserText = (function () {
    var canvas = document.createElement('canvas'),
        context = canvas.getContext('2d');

    /**
     * Measures the rendered width of arbitrary text given the font size and font face
     * @param {string} text The text to measure
     * @param {number} fontSize The font size in pixels
     * @param {string} fontFace The font face ("Arial", "Helvetica", etc.)
     * @returns {number} The width of the text
     **/
    function getWidth(text, fontSize, fontFace = "Helvetica") {
        context.font = fontSize + 'px ' + fontFace;
        return context.measureText(text).width;
    }

    return {
        getWidth: getWidth
    };
})();