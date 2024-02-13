// parsed data is comming from chart.js
console.log("cchartdata3 : ",chartData3)
var dailyCounts = { 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0 };

// Iterate over each date
chartData3.forEach(data => {
  // Get the day of the week
  var day = moment(data.date).format('dddd');
  
  // Increment the count for the day
  dailyCounts[day] += data.c;
});

var monthlyCounts = { 'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 'June': 0, 'July': 0, 'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 0 };

// Iterate over each order
chartData3.forEach(data => {
  // Get the month of the order
  var month = moment(data.date).utc().format('MMMM');
  
  // Increment the count for the month
  monthlyCounts[month] += data.c;
});





// console.log(parseData)
var month_labels = Object.keys(monthlyCounts);
var month_count = Object.values(monthlyCounts);

// console.log(parseData)
var weeks_day = Object.keys(dailyCounts);
var weekdays_count = Object.values(dailyCounts);

var ctx4 = document.getElementById("week-month").getContext("2d");
var myChart4 = new Chart(ctx4, {
  // Type of Chart - bar, line, pie, doughnut, radar, polarArea
  type: "bar",

  // The data for our dataset
  data: {
    // Data Labels
    labels: weeks_day,
    datasets: [
      // Data Set 1
      {
        //  Chart Label
        label: "Week | Month",

        // Actual Data
        data: weekdays_count,

        // Background Color
        backgroundColor: [
            'rgba(255, 26, 104, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(0, 0, 0, 0.2)'
          ],
          borderColor: [
            'rgba(255, 26, 104, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(0, 0, 0, 1)'
          ],

   
        borderWidth: 1,
      },


    ],
  },

  
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





function timeFrame(period){
    console.log(period.value)
    
    // if (period.value =='day'){
    //   myChart.config.options.scales.x.time.unit = period.value;
    //   myChart.config.data.datasets[0].data = day
    // }
    if (period.value =='week'){
        // console.log(myChart4)
        // console.log(myChart4.config._config.data.datasets[0].data)

        myChart4.config._config.data.labels = weeks_day
        myChart4.config._config.data.datasets[0].data = weekdays_count
    console.log('Exectted successfully')
    }
    if (period.value =='month'){
        myChart4.config._config.data.labels = month_labels
        myChart4.config._config.data.datasets[0].data = month_count
    }

    myChart4.update()
  };