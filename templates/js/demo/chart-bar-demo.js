date = JSON.parse({{ date | tojson }});
income = JSON.parse({{ income | tojson }});
spent = JSON.parse({{ spent | tojson }});
money_class = JSON.parse({{ money_class | tojson }});

income_salary=JSON.parse({{ income_salary | tojson }});
income_bonus=JSON.parse({{ income_bonus | tojson }});
income_interest=JSON.parse({{ income_interest | tojson }});
income_accident=JSON.parse({{ income_accident | tojson }});
income_other=JSON.parse({{ income_other | tojson }});

spent_trans=JSON.parse({{  spent_trans | tojson }});
spent_food=JSON.parse({{ spent_food | tojson }});
spent_life=JSON.parse({{ spent_life | tojson }}); 
spent_fun=JSON.parse({{ spent_fun | tojson }});
spent_invest=JSON.parse({{ spent_invest | tojson }});
spent_other=JSON.parse({{ spent_other | tojson }});  
var ctx = document.getElementById("myBarChart");
var myChart = new Chart(ctx, {
type: 'bar',
data: {
    labels: date,
    datasets: [{
    label: '薪水',
    backgroundColor: "#BF3030",
    data: income_salary,
    stack: 'Stack 0'
    }, {
    label: '獎金',
    backgroundColor: "#D94B2B",
    data: income_bonus,
    stack: 'Stack 0'
    }, {
    label: '股息',
    backgroundColor: "#F2811D",
    data: income_interest,
    stack: 'Stack 0'
    }, {
    label: '意外財',
    backgroundColor: "#F2CA99",
    data: income_accident,
    stack: 'Stack 0'
    }, {
    label: '其他收入',
    backgroundColor: "#be5117",
    data: income_other,
    stack: 'Stack 0'
    }, {
    label: '交通',
    backgroundColor: "#4e73df",
    data: spent_trans,
    stack: 'Stack 1'
    }, {
    label: '飲食',
    backgroundColor: "#45c490",
    data: spent_food,
    stack: 'Stack 1'
    }, {
    label: '生活',
    backgroundColor: "#008d93",
    data: spent_life,
    stack: 'Stack 1'
    }, {
    label: '娛樂',
    backgroundColor: "#2e5468",
    data: spent_fun,
    stack: 'Stack 1'
    }, {
    label: '股票投資',
    backgroundColor: "#1cc88a",
    data: spent_invest,
    stack: 'Stack 1'
    }, {
    label: '其他支出',
    backgroundColor: "#36b9cc",
    data: spent_other,
    stack: 'Stack 1'
    }],
},
options: {
    tooltips: {
    displayColors: true,
    callbacks:{
        mode: 'x',
    },
    },
    scales: {
    xAxes: [{
        stacked: true,
        gridLines: {
        display: false,
        }
    }],
    yAxes: [{
        stacked: true,
        ticks: {
        beginAtZero: true,
        },
        type: 'linear',
    }]
    },
    responsive: true,
    maintainAspectRatio: false,
    legend: { position: 'bottom' },
}
});