window.addEventListener("load", function() {

    load_world_map();
    load_realtime_growth_chart();

});


function load_world_map() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);
            hoverinfo = function() {
                result = [];

                for (let index = 0; index < Object.values(data["pk"]).length; index++) {
                    result.push(
                        "<b>" + Object.values(data["pk"])[index] + "</b><br>" +
                        "Confirmed: " + Object.values(data["conf"])[index] + "<br>" +
                        "Lat: " + Object.values(data["lat"])[index] + "<br>" +
                        "Long: " + Object.values(data["long"])[index] + "<br>" +
                        "New: " + Object.values(data["nou"])[index] + "<br>" +
                        "Inicdence: " + Object.values(data["incidenta"])[index]
                    );
                }

                return result;
            }();

            var plot_data = [{
                type: "scattermapbox",
                lat: Object.values(data["lat"]),
                lon: Object.values(data["long"]),
                hovertext: hoverinfo,
                hoverinfo: "text",
                marker: {
                    color: Object.values(data["conf"]),
                    colorbar: {
                        outlinewidth: 0,
                        title: {
                            text: "Confirmed"
                        }
                    },
                    colorscale: [[0, "hsl(255, 95%, 26%)"], [0.5, "hsl(330, 60%, 50%)"], [1, "hsl(60, 100%, 60%)"]],
                    showscale: true,
                    size: Object.values(data["conf"]),
                    sizemin: 0,
                    sizeref: 50,
                    sizemode: "area"
                }
            }];

            var plot_layout = {
                margin: {t:0, l:0, r:0, b:0},
                paper_bgcolor:'rgba(0,0,0,0)',
                mapbox: {
                    style: "carto-darkmatter",
                    center: {lat: 46, lon: 25},
                    zoom: 5.5
                }
            };

            var plot_config = {responsive: true, displayModeBar: false}

            Plotly.newPlot(document.getElementById("world_map"), plot_data, plot_layout, plot_config);
        }
    };

    xhttp.open("GET", "daily");
    xhttp.send();
}


function load_realtime_growth_chart() {
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.response);

            var dates = Object.keys(data["dates"])

            var confirmed_trace = {
                x: dates,
                y: Object.values(data["conf"]),
                name: "Confirmed",
                line: {color: "#8965E0", width: 4}
            };

            var recovered_trace = {
                x: dates,
                y: Object.values(data["nou"]),
                name: "Recovered",
                line: {color: "#2DCE89", width: 4}
            };

            var deaths_trace = {
                x: dates,
                y: Object.values(data["incidenta"]),
                name: "Deaths",
                line: {
                    color: "#F9345E",
                    width: 4
                }
            };

            var plot_data = [confirmed_trace, recovered_trace, deaths_trace];

            var plot_layout = {
                paper_bgcolor:'rgba(0,0,0,0)',
                plot_bgcolor:'rgba(0,0,0,0)',
                yaxis: {automargin: true, type: "log", gridcolor: "#32325d"},
                xaxis: {automargin: true, showgrid: false},
                showlegend: false,
                font: {color: '#ced4da'},
                margin: {t:0, l:0, r:0, b:0},
                hovermode: "closest",
                updatemenus: [
                    {
                        visible: true,
                        type: "dropdown",
                        buttons: [
                            {method: "relayout", label: "Logarithmic", args: [{"yaxis.type": "log"}]},
                            {method: "relayout", label: "Linear", args: [{"yaxis.type": "linear"}]}
                        ],
                        x: 0.05,
                        xanchor: "auto",
                        bgcolor: "#6236FF",
                        bordercolor: "rgba(0,0,0,0)"
                    }
                ]
            };

            var plot_config = {responsive: true, displayModeBar: false};

            Plotly.newPlot(document.getElementById("realtime_growth_chart"), plot_data, plot_layout, plot_config);
        }
    };

    xhttp.open("GET", "daily");
    xhttp.send();
}
