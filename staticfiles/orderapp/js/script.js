
const chartDataElement = document.getElementById('chart_data');
const parseData = JSON.parse(chartDataElement.textContent);


console.log(parseData)
var ordersByStatusLabels = Object.keys(parseData.chart_1.orders_by_status_data);
var ordersByStatusData = Object.values(parseData.chart_1.orders_by_status_data);

var ctx1 = document.getElementById("order_status").getContext("2d");
var myChart1 = new Chart(ctx1, {
  // Type of Chart - bar, line, pie, doughnut, radar, polarArea
  type: "doughnut",

  // The data for our dataset
  data: {
    // Data Labels
    labels: ordersByStatusLabels,
    datasets: [
      // Data Set 1
      {
        //  Chart Label
        label: "Order Status",

        // Actual Data
        data: ordersByStatusData,

        // Background Color
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],

        // Border Color
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],

        // Border Width
        borderWidth: 1,
      },

      // Data Set 2
      // {
      //   //  Chart Label
      //   label: "Framework",

      //   // Actual Data
      //   data: [10, 8, 3, 7, 8, 9],

      //   // Background Color
      //   backgroundColor: [
      //     "rgba(255, 97, 132, 0.2)",
      //     "rgba(54, 16, 235, 0.2)",
      //     "rgba(255, 26, 86, 0.2)",
      //     "rgba(75, 12, 192, 0.2)",
      //     "rgba(153, 2, 255, 0.2)",
      //     "rgba(255, 19, 64, 0.2)",
      //   ],
      // },
    ],
  },

  // Configuration options go here
  // options: {
  //   responsive: false,
    
  // },
});


// Set new default font family and font color to mimic Bootstrap's default styling
// Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
// Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example




"-----------------------------------------------------------------------------------------------------"
//  Chart 2 
var quantityByItemLabels = Object.keys(parseData.chart_2.quantity_by_item_data);
var quantityByItemData = Object.values(parseData.chart_2.quantity_by_item_data);


console.log(quantityByItemLabels)
console.log(quantityByItemData)

var ctx2 = document.getElementById("item_quantity").getContext("2d");
var myChart2 = new Chart(ctx2, {
  // Type of Chart - bar, line, pie, doughnut, radar, polarArea
  type: "bar",

  // The data for our dataset
  data: {
    // Data Labels
    labels: quantityByItemLabels,
    datasets: [
      // Data Set 1
      {
        //  Chart Label
        label: "Item Quantity",

        // Actual Data
        data: quantityByItemData,

        // Background Color
        backgroundColor: [
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(75, 192, 192, 0.2)",
          "rgba(153, 102, 255, 0.2)",
          "rgba(255, 159, 64, 0.2)",
        ],

        // Border Color
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(153, 102, 255, 1)",
          "rgba(255, 159, 64, 1)",
        ],

        // Border Width
        borderWidth: 1,
      },


      // Data Set 2
      // {
      //   //  Chart Label
      //   label: "Framework",

      //   // Actual Data
      //   data: [10, 8, 3, 7, 8, 9],

      //   // Background Color
      //   backgroundColor: [
      //     "rgba(255, 97, 132, 0.2)",
      //     "rgba(54, 16, 235, 0.2)",
      //     "rgba(255, 26, 86, 0.2)",
      //     "rgba(75, 12, 192, 0.2)",
      //     "rgba(153, 2, 255, 0.2)",
      //     "rgba(255, 19, 64, 0.2)",
      //   ],
      // },
    ],
  },

  // Configuration options go here
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 60000,
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  },
});

"-----------------------------------------------------------------------------------------------------"
