console.log(parseData)

var ctx5 = document.getElementById("order-per-hr");
var mytimedChart = new Chart(ctx5, {
  type: 'bar',
  data: {
    labels:parseData.order_hourly_count.hour_interval,
    datasets: [{
      label: "orders",
      backgroundColor: "rgb(255, 129, 2)",
      borderColor: "rgb(255, 129, 2)",
      data: parseData.order_hourly_count.order_count,
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'time'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 6
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 15000,
          maxTicksLimit: 5
        },
        gridLines: {
          display: true
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
