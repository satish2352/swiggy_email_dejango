
// Chart 3

// const chart3DataElement = document.getElementById('chart_data');
// var parseData = JSON.parse(chart3DataElement.textContent);
console.log("parsedata:" ,parseData)
chartData3 = parseData.chart_3.orders_over_time;

console.log("chartData3:-->",chartData3)

let c_values = chartData3.map(obj => obj.c);


// let date_values = chartData3.map(obj => obj.date.format('YYYY-MM-DD'));
// console.log(date_values)


var date_data = [];
chartData3.forEach(data => {
  data.date = moment(data.date); // Assuming data.date is the date string in your chartData
  date_data.push(data.date);
});

const formattedDates = [];

// Iterate through each moment object and format the date
date_data.forEach(date => {
  const formattedDate = date.format('YYYY-MM-DD');
  formattedDates.push(formattedDate);
});


console.log('formattedDates',formattedDates,'c_values',c_values)




// const dates = ['2021-08-25', '2021-08-26', '2021-08-27', '2021-08-28', '2021-08-29', '2021-08-30', '2021-08-31']
//     const datapoints = [1,2,3,4,5,6,7];
    const data = {
      labels: formattedDates,
      datasets: [{
        label: 'total orders',
        data: c_values ,
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
        borderWidth: 1
      }]
    };

    // config 
    const config = {
      type: 'bar',
      data,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };

    // render init block
    const myChart3 = new Chart(
      document.getElementById('datewiseOrder'),
      config
    );

    // const startdate=document.getElementById('startdate');
    // const enddate=document.getElementById('enddate');
    // startdate.value = formattedDates[0];
    // enddate.value = formattedDates.slice(-1)[0]; 

    // function filterData() {
    //     const startDate = new Date(document.getElementById('startdate').value);
    //     const endDate = new Date(document.getElementById('enddate').value);
      
    //     const filteredDates = formattedDates.filter(date => {
    //       const currentDate = new Date(date);
    //       return currentDate >= startDate && currentDate <= endDate;
    //     });

    //     console.log( "filtered dataes:",  filteredDates)
    //     myChart3.data.labels = filteredDates;
    //     myChart3.update();
    //   }