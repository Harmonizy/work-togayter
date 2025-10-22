// ✅ Dynamic Donut Charts จาก Django
var chartDonutBasicColors = getChartColorsArray("store-visits-source");
if (chartDonutBasicColors) {
    let datasets = window.REPORT_DATASETS || [];
    let series = datasets.map(d => d.count);
    let labels = datasets.map(d => d.label);

    console.log("📊 Donut Labels:", labels);
    console.log("📊 Donut Series:", series);

    var options = {
        series: series,
        labels: labels,
        chart: {
            height: 333,
            type: "donut",
        },
        legend: {
            position: "bottom",
        },
        stroke: {
            show: false
        },
        dataLabels: {
            dropShadow: {
                enabled: false,
            },
        },
        colors: chartDonutBasicColors,
    };

    if (storeVisitsSourceChart != "")
        storeVisitsSourceChart.destroy();
    storeVisitsSourceChart = new ApexCharts(document.querySelector("#store-visits-source"), options);
    storeVisitsSourceChart.render();
}
