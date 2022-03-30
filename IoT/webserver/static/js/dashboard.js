/* globals Chart:false, feather:false */

function changeButtonStatus() {
  document.getElementById('dashboard-button').classList.remove('active');
  document.getElementById('control-button').classList.remove('active');
  document.getElementById('devices-button').classList.remove('active');
  document.getElementById('reports-button').classList.remove('active');
  document.getElementById('info-button').classList.remove('active');

  document.getElementById(this.id).classList.add('active');
}

document.getElementById('dashboard-button').onclick = changeButtonStatus;
document.getElementById('control-button').onclick = changeButtonStatus;
document.getElementById('devices-button').onclick = changeButtonStatus;
document.getElementById('reports-button').onclick = changeButtonStatus;
document.getElementById('info-button').onclick = changeButtonStatus;

(function () {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: 'rgb(255,121,1)',
        borderWidth: 4,
        pointBackgroundColor: 'rgb(255,121,1)',
        pointBorderColor: 'rgb(255,121,1)',
        pointHoverBackgroundColor: 'rgb(251,47,0)',
        pointHoverBorderColor: 'rgb(251,47,0)',
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()
