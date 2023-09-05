var cacheddata = undefined;

// set the dimensions and margins of the graph
var margin = {top: 150, right: 100, bottom: 20, left: 100},
    width = $(window).width() - 50 - margin.left - margin.right,
    height = $(window).height() - 50 - margin.top - margin.bottom;

function prepare_data(data, focus, team) {
    prepared_data = []
    if (focus == "overview"){
        data.forEach(function(d){
            prepared_data.push({
                "name": d["name"],
                "total": d["as_killer"]["aggregate"]["total"],
                "physical": d["as_killer"]["aggregate"]["physical"],
                "magic": d["as_killer"]["aggregate"]["magic"],
                "true": d["as_killer"]["aggregate"]["true"],
                "takedowns": d["as_killer"]["aggregate"]["takedowns"],
            });
        });
        return prepared_data.reverse();
    }
    else {
        // focus is a specific champ
        prepared_data = []
        data.forEach(function(d){
            if(d.name == focus){
                
                for(key in d["as_killer"]){
                    if (key != "aggregate")
                    {
                        prepared_data.push({
                            "name": key,
                            "total": d["as_killer"][key]["total"],
                            "physical": d["as_killer"][key]["physical"],
                            "magic": d["as_killer"][key]["magic"],
                            "true": d["as_killer"][key]["true"],
                            "takedowns": d["as_killer"][key]["takedowns"],
                        });
                    }
                }
                for(key in d["as_victim"]){
                    if (key != "aggregate")
                    {
                        prepared_data.push({
                            "name": key,
                            "total": d["as_victim"][key]["total"],
                            "physical": d["as_victim"][key]["physical"],
                            "magic": d["as_victim"][key]["magic"],
                            "true": d["as_victim"][key]["true"],
                            "takedowns": d["as_victim"][key]["takedowns"],
                        });
                    }
                }
                
            }
            
        });

        return prepared_data.reverse();
    }
};

function reload(focus, provided_data=false, newdata=undefined){
    if(provided_data){
        cacheddata = newdata;
    }
    if(cacheddata == undefined){
        return;
    }

    console.log("here " + provided_data);

    d3.selectAll("svg").remove();
    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)

    svg.append('line')
    .style("stroke", "black")
    .style("stroke-width", 5)
    .attr("x1", margin.left/2)
    .attr("y1", 115)
    .attr("x2", width+1.5*margin.right)
    .attr("y2", 115)

    svg.append('line')
    .style("stroke", "black")
    .style("stroke-width", 2)
    .attr("x1", margin.left + width/2)
    .attr("y1", 115)
    .attr("x2", margin.left + width/2)
    .attr("y2", height+margin.top-margin.bottom)
    

    var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x = d3.scaleLinear().range([0, width/2-5]),
    y = d3.scaleBand().range([height, 0]).paddingInner(0.05).align(0.1),
    z = d3.scaleOrdinal()
        .range(["indianred", "royalblue", "gainsboro"]);
    
    data = cacheddata;

    
    data = prepare_data(data, focus);
    data_red = data.slice(0,5);
    data_blue = data.slice(5);

    if(focus == "overview") {
        var title = svg.append("g");
        title
            .append("text")
            .text("Critical damage dealt overview")
            .attr("text-anchor", "middle")
            .style("font-size", "50px")
            .attr("x", 125 + width/2)
            .attr("y", 50);
        title
            .append("text")
            .text("aka damage that contributed to a kill")
            .attr("text-anchor", "middle")
            .style("font-size", "24px")
            .attr("x", 125 + width/2)
            .attr("y", 80);
    }
    else {
        var title = svg.append("g");
        title.append("svg:image")
            .attr('width', Math.min(100,height/5))
            .attr('height', Math.min(100,height/5))
            .attr("xlink:href", document.getElementById(focus+".jpg").getAttribute("data-img-url"))
            .attr("y", 2);
        title
            .append("text")
            .text(focus)
            .style("font-size", "50px")
            .attr("x", Math.min(100,height/5)+5)
            .attr("y", 72);
        console.log((title.node().getBBox().width/2));
        console.log(width);
        title.attr("transform", "translate("+(width/2 + margin.left - (title.node().getBBox().width/2)) +",0)");

        svg.append("g").append("svg:image")
        .attr('width', Math.min(80,height/6))
        .attr('height', Math.min(80,height/6))
        .attr("xlink:href", document.getElementById("overview.png").getAttribute("data-img-url"))
        .attr("y", 2)
        .on("click", function(d) {return reload("overview");})
        .style('cursor', 'pointer');

        svg.append("g").append("text")
            .text("Champions I killed")
            .attr("text-anchor", "middle")
            .style("font-size", "28px")
            .attr("x", margin.left + BrowserText.getWidth("People who I killed", 28) / 2)
            .attr("y", 105);
        
        svg.append("g").append("text")
            .text("Champions who killed me")
            .attr("text-anchor", "right")
            .style("font-size", "28px")
            .attr("x", width + margin.right - BrowserText.getWidth("Champions who killed me", 28))
            .attr("y", 105);

        
    }

    // share a scale for the x domain
    var xdomain=[0, d3.max(data, function(d) {
        return d.total;
    })];
    x.domain(xdomain);

    // draw the blue team data
    y.domain(data_blue.map(function(d,i) {return d.name;}));
    g.selectAll(".label")
        .data(data_blue)
        .enter()
        .append("text")
        .text(function(d) {
            var label = "";
            if(d.takedowns > 1){
                label = d.total.toLocaleString("en-US") + " ("+ d.takedowns + " takedowns)";
            } else if(d.takedowns == 1){
                label = d.total.toLocaleString("en-US") + " (1 takedown)";
            } else {
                label = d.total.toLocaleString("en-US") + " (0 takedowns)";
            }
            return label;
        })
        .attr("x", function(d,i) { return 0; })
        .attr("y", function(d) { return y(d.name) - 5; })
        
        .style("font-size", "18px");
    g.selectAll(".images")
        .data(data_blue)
        .enter()
        .append("svg:image")
        .attr("x", function(d,i) { return x(0) - (Math.min(80,height/8)+10); })
        .attr("y", function(d) { return y(d.name); })
        .attr('width', Math.min(80,height/8))
        .attr('height', Math.min(80,height/8))
        .attr("xlink:href", function(d) {
            console.log(document.getElementById(d.name+".jpg").getAttribute("data-img-url"))
            return document.getElementById(d.name+".jpg").getAttribute("data-img-url");
        })
        .on("click", function(d) {return reload(d.name);})
        .style('cursor', 'pointer');

    g.selectAll(".bar")
        .data(d3.stack().keys(["physical", "magic", "true"])(data_blue))
        .enter().append("g")
        .attr("fill", function(d) { return z(d.key);})
        .selectAll("rect").data(function(d) { return d; })
        .enter().append("rect")
        .attr("x", function(d,i) { return x(d[0]); })
        .attr("y", function(d) { return y(d.data.name); })
        .attr("width", function(d) { return x(d[1] - d[0]); })
        .attr("height", Math.min(80,height/8))
        .append("svg:title")
        .text(function(d) { return (d[1] - d[0]).toLocaleString("en-US") + " " + d3.select(this.parentNode.parentNode).datum().key + "."; });
    
    // draw the red team data
    y.domain(data_red.map(function(d,i) {return d.name;}));
    g.selectAll(".label")
        .data(data_red)
        .enter()
        .append("text")
        .text(function(d) {
            var label = "";
            console.log(d);
            if(d.takedowns > 1){
                label = d.total.toLocaleString("en-US") + " ("+ d.takedowns + " takedowns)";
            } else if(d.takedowns == 1){
                label = d.total.toLocaleString("en-US") + " (1 takedown)";
            } else {
                label = d.total.toLocaleString("en-US") + " (0 takedowns)";
            }
            return label;
        })
        .attr("x", function(d,i) { return 0; })
        .attr("y", function(d) { return y(d.name) - 5; })
        .style("font-size", "18px")
        .attr("transform", function(d) {
            var label = "";
            if(d.takedowns > 1){
                label = d.total.toLocaleString("en-US") + " ("+ d.takedowns + " takedowns)";
            } else if(d.takedowns == 1){
                label = d.total.toLocaleString("en-US") + " (1 takedown)";
            } else {
                label = d.total.toLocaleString("en-US") + " (0 takedowns)";
            }
            return "translate("+(width - BrowserText.getWidth(label, 18)) + ", 0)";
        });
    g.selectAll(".images_red")
        .data(data_red)
        .enter()
        .append("svg:image")
        .attr("x", function(d,i) { return x(0) - 90; })
        .attr("y", function(d) { return y(d.name); })
        .attr('width', Math.min(80,height/8))
        .attr('height', Math.min(80,height/8))
        .attr("xlink:href", function(d) {return document.getElementById(d.name+".jpg").getAttribute("data-img-url");})
        .attr("transform", "translate("+(width+100)+",0)")
        .on("click", function(d) {return reload(d.name);})
        .style('cursor', 'pointer');
    g.selectAll(".bar")
        .data(d3.stack().keys(["physical", "magic", "true"])(data_red))
        .enter().append("g")
        .attr("fill", function(d) { return z(d.key);})
        .selectAll("rect").data(function(d) { return d; })
        .enter().append("rect")
        .attr("x", function(d,i) { return x(d[0]); })
        .attr("y", function(d) { return y(d.data.name); })
        .attr("transform", "scale(-1, 1) translate(-"+width+", 0)")
        .attr("width", function(d) { return x(d[1] - d[0]); })
        .attr("height", Math.min(80,height/8))
        .append("svg:title")
        .text(function(d) { return (d[1] - d[0]).toLocaleString("en-US") + " " + d3.select(this.parentNode.parentNode).datum().key + "."; });


}

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
    function getWidth(text, fontSize, fontFace) {
        context.font = fontSize + 'px ' + fontFace;
        return context.measureText(text).width;
    }

    return {
        getWidth: getWidth
    };
})();