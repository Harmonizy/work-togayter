function getChartColorsArray(e) {
  if (null !== document.getElementById(e)) {
    var t = "data-colors" + ("-" + document.documentElement.getAttribute("data-theme") ?? "");
    t = document.getElementById(e).getAttribute(t) ?? document.getElementById(e).getAttribute("data-colors");
    if (t)
      return (t = JSON.parse(t)).map(function (e) {
        var t = e.replace(" ", "");
        return -1 === t.indexOf(",")
          ? getComputedStyle(document.documentElement).getPropertyValue(t) || t
          : 2 == (e = e.split(",")).length
          ? "rgba(" + getComputedStyle(document.documentElement).getPropertyValue(e[0]) + "," + e[1] + ")"
          : t;
      });
    console.warn("data-colors attributes not found on", e);
  }
}

var worldemapmarkers = "",
  storeVisitsSourceChart = "",
  customerImpressionChart = "";

function loadCharts() {
  // 🌍 Vector Map
  var t = getChartColorsArray("sales-by-locations");
  if (t) {
    document.getElementById("sales-by-locations").innerHTML = "";
    worldemapmarkers = new jsVectorMap({
      map: "world_merc",
      selector: "#sales-by-locations",
      zoomOnScroll: !0,
      zoomButtons: !0,
      selectedMarkers: [0, 5],
      regionStyle: { initial: { stroke: "#9599ad", strokeWidth: 0.25, fill: t[0], fillOpacity: 1 } },
      markersSelectable: !0,
      markers: [
        { name: "บน.1", coords: [13.9101, 100.6033], report: 120 },
        { name: "บน.2", coords: [17.3657, 102.771], report: 85 },
        { name: "บน.3", coords: [13.478, 100.947], report: 95 },
        { name: "บน.4", coords: [14.9895, 102.0952], report: 200 },
        { name: "บน.5", coords: [18.7977, 98.975], report: 150 },
        { name: "บน.6", coords: [9.1376, 99.3125], report: 130 },
        { name: "บน.7", coords: [13.7258, 100.6181], report: 175 },
        { name: "บน.8", coords: [19.9114, 99.8443], report: 90 },
        { name: "บน.9", coords: [16.8802, 100.2683], report: 110 },
        { name: "บน.10", coords: [7.1203, 100.5299], report: 160 },
      ],
      markerStyle: { initial: { fill: t[1] }, selected: { fill: t[2] } },
      labels: {
        markers: {
          render: function (e) {
            return e.name + " - " + e.report + " รายงาน";
          },
        },
      },
      onLoaded: function () {
        this.setCenter([13.7367, 100.5236]);
        this.setScale(3);
      },
    });
  }

  // 📊 Customer Impression Chart
  t = getChartColorsArray("customer_impression_charts");
  if (t) {
    var e = {
      series: [
        { name: "รายงาน", type: "area", data: [4, 5, 6, 8, 9, 1, 2, 4, 8, 2, 3, 7] },
        { name: "อนุมัติ", type: "bar", data: [34, 45, 32, 56, 47, 58, 39, 41, 52, 45, 48, 55] },
        { name: "เร่งด่วน", type: "bar", data: [28, 35, 30, 44, 39, 41, 30, 29, 48, 33, 38, 40] },
        { name: "ต้องติดตาม", type: "bar", data: [22, 31, 27, 36, 32, 38, 25, 24, 40, 29, 34, 36] },
        { name: "ไม่อนุมัติ", type: "line", data: [8, 12, 7, 17, 21, 11, 5, 9, 7, 29, 12, 35] },
      ],
      chart: { height: 370, type: "line", toolbar: { show: !1 } },
      stroke: { curve: "straight", dashArray: [0, 0, 8], width: [2, 0, 2.2] },
      fill: { opacity: [0.1, 0.9, 1] },
      markers: { size: [0, 0, 0], strokeWidth: 2, hover: { size: 4 } },
      xaxis: {
        categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        axisTicks: { show: !1 },
        axisBorder: { show: !1 },
      },
      grid: {
        show: !0,
        xaxis: { lines: { show: !0 } },
        yaxis: { lines: { show: !1 } },
        padding: { top: 0, right: -2, bottom: 15, left: 10 },
      },
      legend: {
        show: !0,
        horizontalAlign: "center",
        offsetX: 0,
        offsetY: -5,
        markers: { width: 9, height: 9, radius: 6 },
        itemMargin: { horizontal: 10, vertical: 0 },
      },
      plotOptions: { bar: { columnWidth: "70%", barHeight: "70%" } },
      colors: t,
      tooltip: {
        shared: !0,
        y: [
          { formatter: function (e) { return void 0 !== e ? e.toFixed(0) : e; } },
          { formatter: function (e) { return void 0 !== e ? "$" + e.toFixed(2) + "k" : e; } },
          { formatter: function (e) { return void 0 !== e ? e.toFixed(0) + " Sales" : e; } },
        ],
      },
    };
    if ("" != customerImpressionChart) customerImpressionChart.destroy();
    customerImpressionChart = new ApexCharts(document.querySelector("#customer_impression_charts"), e);
    customerImpressionChart.render();
  }

  // 🍩 Donut Chart - store-visits-source
  var chartEl = document.getElementById("store-visits-source");
  if (chartEl && chartEl.dataset.reportType) {
    let rawData = [];
    try {
      rawData = JSON.parse(chartEl.dataset.reportType);
    } catch (err) {
      console.error("❌ JSON parse error:", err);
    }

    var labels = rawData.map(item => item[0]);
    var series = rawData.map(item => item[1]);
    var colors = getChartColorsArray("store-visits-source");

    console.log("✅ Labels:", labels);
    console.log("✅ Series:", series);

    var donutOptions = {
      series: series,
      labels: labels,
      chart: { height: 333, type: "donut" },
      legend: { position: "bottom" },
      stroke: { show: false },
      dataLabels: { dropShadow: { enabled: false } },
      colors: colors,
    };

    if (storeVisitsSourceChart) storeVisitsSourceChart.destroy();
    storeVisitsSourceChart = new ApexCharts(chartEl, donutOptions);
    storeVisitsSourceChart.render();
  } else {
    console.warn("⚠️ store-visits-source element หรือ dataset ไม่พบ");
  }
}

// ✅ โหลดกราฟหลัง DOM โหลดเสร็จ
document.addEventListener("DOMContentLoaded", loadCharts);

// ✅ รีโหลดเมื่อขนาดจอเปลี่ยน
window.onresize = function () {
  setTimeout(() => {
    loadCharts();
  }, 0);
};

// 📜 Layout ส่วนอื่น ๆ
var overlay,
  swiper = new Swiper(".vertical-swiper", {
    slidesPerView: 2,
    spaceBetween: 10,
    mousewheel: !0,
    loop: !0,
    direction: "vertical",
    autoplay: { delay: 2500, disableOnInteraction: !1 },
  }),
  layoutRightSideBtn = document.querySelector(".layout-rightside-btn");

layoutRightSideBtn &&
  (Array.from(document.querySelectorAll(".layout-rightside-btn")).forEach(function (e) {
    var t = document.querySelector(".layout-rightside-col");
    e.addEventListener("click", function () {
      t.classList.contains("d-block") ? (t.classList.remove("d-block"), t.classList.add("d-none")) : (t.classList.remove("d-none"), t.classList.add("d-block"));
    });
  }),
  window.addEventListener("resize", function () {
    var e = document.querySelector(".layout-rightside-col");
    e &&
      Array.from(document.querySelectorAll(".layout-rightside-btn")).forEach(function () {
        window.outerWidth < 1699 || 3440 < window.outerWidth ? e.classList.remove("d-block") : 1699 < window.outerWidth && e.classList.add("d-block");
      }),
      "semibox" == document.documentElement.getAttribute("data-layout") && (e.classList.remove("d-block"), e.classList.add("d-none"));
  }),
  (overlay = document.querySelector(".overlay"))) &&
  document.querySelector(".overlay").addEventListener("click", function () {
    1 == document.querySelector(".layout-rightside-col").classList.contains("d-block") && document.querySelector(".layout-rightside-col").classList.remove("d-block");
  }),
  window.addEventListener("load", function () {
    var e = document.querySelector(".layout-rightside-col");
    e &&
      Array.from(document.querySelectorAll(".layout-rightside-btn")).forEach(function () {
        window.outerWidth < 1699 || 3440 < window.outerWidth ? e.classList.remove("d-block") : 1699 < window.outerWidth && e.classList.add("d-block");
      }),
      "semibox" == document.documentElement.getAttribute("data-layout") && 1699 < window.outerWidth && (e.classList.remove("d-block"), e.classList.add("d-none"));
  });
