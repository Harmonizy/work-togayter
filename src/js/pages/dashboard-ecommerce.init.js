/*
Template Name: Velzon - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Ecommerce Dashboard init js
*/

// get colors array from the string
function getChartColorsArray(chartId) {
    if (document.getElementById(chartId) !== null) {
        const colorAttr = "data-colors" + ("-" + document.documentElement.getAttribute("data-theme") ?? "");
        var colors = document.getElementById(chartId).getAttribute(colorAttr) ?? document.getElementById(chartId).getAttribute("data-colors");
        if (colors) {
            colors = JSON.parse(colors);
            return colors.map(function (value) {
                var newValue = value.replace(" ", "");
                if (newValue.indexOf(",") === -1) {
                    var color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
                    if (color) return color;
                    else return newValue;;
                } else {
                    var val = value.split(',');
                    if (val.length == 2) {
                        var rgbaColor = getComputedStyle(document.documentElement).getPropertyValue(val[0]);
                        rgbaColor = "rgba(" + rgbaColor + "," + val[1] + ")";
                        return rgbaColor;
                    } else {
                        return newValue;
                    }
                }
            });
        } else {
            console.warn('data-colors attributes not found on', chartId);
        }
    }
}

var worldemapmarkers = "";
var storeVisitsSourceChart = "";
var customerImpressionChart = "";
function loadCharts() {
    // world map with markers
    var vectorMapWorldMarkersColors = getChartColorsArray("sales-by-locations");
    if (vectorMapWorldMarkersColors) {
        document.getElementById("sales-by-locations").innerHTML = "";
        worldemapmarkers = "";
        worldemapmarkers = new jsVectorMap({
            map: "world_merc",
            selector: "#sales-by-locations",
            zoomOnScroll: true,
            zoomButtons: true,
            selectedMarkers: [0, 5],
            regionStyle: {
                initial: {
                    stroke: "#9599ad",
                    strokeWidth: 0.25,
                    fill: vectorMapWorldMarkersColors[0],
                    fillOpacity: 1,
                },
            },
            markersSelectable: true,
            markers: [
                {
                    name: "บน.1",
                    coords: [13.9101, 100.6033],
                    report: 120, // จำนวนรายงาน
                },
                {
                    name: "บน.2",
                    coords: [17.3657, 102.7710],
                    report: 85,
                },
                {
                    name: "บน.3",
                    coords: [13.4780, 100.9470],
                    report: 95,
                },
                {
                    name: "บน.4",
                    coords: [14.9895, 102.0952],
                    report: 200,
                },
                {
                    name: "บน.5",
                    coords: [18.7977, 98.9750],
                    report: 150,
                },
                {
                    name: "บน.6",
                    coords: [9.1376, 99.3125],
                    report: 130,
                },
                {
                    name: "บน.7",
                    coords: [13.7258, 100.6181],
                    report: 175,
                },
                {
                    name: "บน.8",
                    coords: [19.9114, 99.8443],
                    report: 90,
                },
                {
                    name: "บน.9",
                    coords: [16.8802, 100.2683],
                    report: 110,
                },
                {
                    name: "บน.10",
                    coords: [7.1203, 100.5299],
                    report: 160,
                },
            ],
            markerStyle: {
                initial: {
                    fill: vectorMapWorldMarkersColors[1],
                },
                selected: {
                    fill: vectorMapWorldMarkersColors[2],
                },
            },
            labels: {
                markers: {
                    render: function (marker) {
                        return marker.name + " - " + marker.report + " รายงาน"; // แสดงชื่อกองบิน + จำนวนรายงาน
                    },
                },
            },
            onLoaded: function () {
                // Zoom and center the map to Thailand's coordinates
                var map = this; // This refers to the map instance
                var thailandCoordinates = [13.7367, 100.5236]; // Coordinates of Thailand's center (Bangkok)
                
                // Set the center to Thailand
                map.setCenter(thailandCoordinates);
                
                // Zoom in (optional, you can adjust the zoom level)
                map.setScale(3); // Adjust scale to zoom in/out the map
            }
        });
    }

    var linechartcustomerColors = "";
    linechartcustomerColors = getChartColorsArray("customer_impression_charts");
    if (linechartcustomerColors) {
        var options = {
            series: [{
                name: "รายงาน",
                type: "area",
                data: [4, 5, 6, 8, 9, 1, 2, 4, 8, 2, 3, 7],
            },
            {
                name: "อนุมัติ",
                type: "bar",
                data: [34, 45, 32, 56, 47, 58, 39, 41, 52, 45, 48, 55],
            },
            {
                name: "เร่งด่วน",
                type: "bar",
                data: [28, 35, 30, 44, 39, 41, 30, 29, 48, 33, 38, 40],
            },
            {
                name: "ต้องติดตาม",
                type: "bar",
                data: [22, 31, 27, 36, 32, 38, 25, 24, 40, 29, 34, 36],
            },
            {
                name: "ไม่อนุมัติ",
                type: "line",
                data: [8, 12, 7, 17, 21, 11, 5, 9, 7, 29, 12, 35],
            },
            ],
            chart: {
                height: 370,
                type: "line",
                toolbar: {
                    show: false,
                },
            },
            stroke: {
                curve: "straight",
                dashArray: [0, 0, 8],
                width: [2, 0, 2.2],
            },
            fill: {
                opacity: [0.1, 0.9, 1],
            },
            markers: {
                size: [0, 0, 0],
                strokeWidth: 2,
                hover: {
                    size: 4,
                },
            },
            xaxis: {
                categories: [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec",
                ],
                axisTicks: {
                    show: false,
                },
                axisBorder: {
                    show: false,
                },
            },
            grid: {
                show: true,
                xaxis: {
                    lines: {
                        show: true,
                    },
                },
                yaxis: {
                    lines: {
                        show: false,
                    },
                },
                padding: {
                    top: 0,
                    right: -2,
                    bottom: 15,
                    left: 10,
                },
            },
            legend: {
                show: true,
                horizontalAlign: "center",
                offsetX: 0,
                offsetY: -5,
                markers: {
                    width: 9,
                    height: 9,
                    radius: 6,
                },
                itemMargin: {
                    horizontal: 10,
                    vertical: 0,
                },
            },
            plotOptions: {
                bar: {
                    columnWidth: "70%",
                    barHeight: "70%",
                },
            },
            colors: linechartcustomerColors,
            tooltip: {
                shared: true,
                y: [{
                    formatter: function (y) {
                        if (typeof y !== "undefined") {
                            return y.toFixed(0);
                        }
                        return y;
                    },
                },
                {
                    formatter: function (y) {
                        if (typeof y !== "undefined") {
                            return "$" + y.toFixed(2) + "k";
                        }
                        return y;
                    },
                },
                {
                    formatter: function (y) {
                        if (typeof y !== "undefined") {
                            return y.toFixed(0) + " Sales";
                        }
                        return y;
                    },
                },
                ],
            },
        };
        if (customerImpressionChart != "")
            customerImpressionChart.destroy();
        customerImpressionChart = new ApexCharts(document.querySelector("#customer_impression_charts"), options);
        customerImpressionChart.render();
    }

    // Simple Donut Charts
    var chartDonutBasicColors = "";
    chartDonutBasicColors = getChartColorsArray("store-visits-source");
    if (chartDonutBasicColors) {
        var options = {
            series: [44, 41, 17, 15],
            labels: ["รายงานอุบัติเหตุภาคพื้น", "รายงานอุบัติการณ์ภาคพื้น", "รายงานอากาศยานอุบัติเหตุ", "รายงานอากาศยานอุบัติการณ์"],
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
}

window.onresize = function() {
    setTimeout(() => {
        loadCharts();
    }, 0);
};

loadCharts();

// Vertical Swiper
var swiper = new Swiper(".vertical-swiper", {
    slidesPerView: 2,
    spaceBetween: 10,
    mousewheel: true,
    loop: true,
    direction: "vertical",
    autoplay: {
        delay: 2500,
        disableOnInteraction: false,
    },
});

var layoutRightSideBtn = document.querySelector('.layout-rightside-btn');
if (layoutRightSideBtn) {
    Array.from(document.querySelectorAll(".layout-rightside-btn")).forEach(function (item) {
        var userProfileSidebar = document.querySelector(".layout-rightside-col");
        item.addEventListener("click", function () {
            if (userProfileSidebar.classList.contains("d-block")) {
                userProfileSidebar.classList.remove("d-block");
                userProfileSidebar.classList.add("d-none");
            } else {
                userProfileSidebar.classList.remove("d-none");
                userProfileSidebar.classList.add("d-block");
            }
        });
    });
    window.addEventListener("resize", function () {
        var userProfileSidebar = document.querySelector(".layout-rightside-col");
        if (userProfileSidebar) {
            Array.from(document.querySelectorAll(".layout-rightside-btn")).forEach(function () {
                if (window.outerWidth < 1699 || window.outerWidth > 3440) {
                    userProfileSidebar.classList.remove("d-block");
                } else if (window.outerWidth > 1699) {
                    userProfileSidebar.classList.add("d-block");
                }
            });
        }

        var htmlAttr = document.documentElement;
        if (htmlAttr.getAttribute("data-layout") == "semibox") {
            userProfileSidebar.classList.remove("d-block");
            userProfileSidebar.classList.add("d-none");
        }
    });
    var overlay = document.querySelector('.overlay');
    if (overlay) {
        document.querySelector(".overlay").addEventListener("click", function () {
            if (document.querySelector(".layout-rightside-col").classList.contains('d-block') == true) {
                document.querySelector(".layout-rightside-col").classList.remove("d-block");
            }
        });
    }
}

window.addEventListener("load", function () {
    var userProfileSidebar = document.querySelector(".layout-rightside-col");
    if (userProfileSidebar) {
        Array.from(document.querySelectorAll(".layout-rightside-btn")).forEach(function () {
            if (window.outerWidth < 1699 || window.outerWidth > 3440) {
                userProfileSidebar.classList.remove("d-block");
            } else if (window.outerWidth > 1699) {
                userProfileSidebar.classList.add("d-block");
            }
        });
    }

    var htmlAttr = document.documentElement

    if (htmlAttr.getAttribute("data-layout") == "semibox") {
        if (window.outerWidth > 1699) {
            userProfileSidebar.classList.remove("d-block");
            userProfileSidebar.classList.add("d-none");
        }
    }
});