window.addEventListener("load", function() {

    load_world_map();

});


function load_world_map() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);

            hoverinfo = function() {
                result = [];


                for (let index = 0; index < Object.values(data["coord"]).length; index++) {
                    result.push(
                        "<b>" + Object.values(data["coord"])[index] + "</b><br>" +
                        "Lat: " + Object.values(data["latitude"])[index] + "<br>" +
                        "Long: " + Object.values(data["longitude"])[index]
                    );
                }

                return result;
            }()

            var plot_data = [{
                type: "scattermapbox",
                lat: 46.0709,
                lon: 23.5731,
                hovertext: hoverinfo,
                hoverinfo: "text",
                marker: {
                    color: 30000,
                    colorbar: {
                        outlinewidth: 0,
                        title: {
                            text: "Confirmed"
                        }
                    },
                    colorscale: [[0, "hsl(255, 95%, 26%)"], [0.5, "hsl(330, 60%, 50%)"], [1, "hsl(60, 100%, 60%)"]],
                    showscale: true,
                    size: 30000,
                    sizemin: 0,
                    sizeref: 2000,
                    sizemode: "area"
                }
            }];

            var plot_layout = {
                margin: {t:0, l:0, r:0, b:0},
                paper_bgcolor:'rgba(0,0,0,0)',
                mapbox: {
                    style: "carto-positron",
                    center: {lat: 20, lon: -20},
                    zoom: 1
                }
            };

            var plot_config = {responsive: true, displayModeBar: false}

            Plotly.newPlot(document.getElementById("world_map"), plot_data, plot_layout, plot_config);
        }
    };

    xhttp.open("GET", "daily", true);
    xhttp.send();
}
