var year = localStorage.getItem("selected_year");
var quarter = localStorage.getItem("selected_quarter");
var month = localStorage.getItem("selected_month");
var day = localStorage.getItem("selected_day");


//数据质量总览
$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/data_overview_total",    
    data: {
        'year': year,
        'quarter': quarter,
        'month': month,
        'day': day
    },
    dataType : "json",
    success : function(result) {
        all_cnt = document.getElementById("all_cnt");
        all_cnt.innerHTML = result.all_cnt;
        problem_cnt = document.getElementById("problem_cnt");
        problem_cnt.innerHTML = result.problem_cnt;
        problem_per = document.getElementById("problem_per");
        problem_per.innerHTML = result.problem_per + '%';
    },
})


// 数据质量问题概况
function InsertTable(company, data){
    // 填充各公司数据概况<table>
    let table = document.getElementById("overview_"+company);
    let html = "";
    html += "<td>检核数据量</td>";
    html += "<td>" + data[1] + "</td>";
    html += '<td rowspan="3" id="overview_chart_' + company + '", style="weight:auto; height: auto;"></td>';
    html += "</tr>"
    html += "<tr>";
    html += "<td>问题数据量</td>";
    html += '<td style="color:red;">' + data[2] + "</td>";
    html += "</tr>"
    html += "<tr>";
    html += "<td>问题占比</td>";
    html += '<td>' + data[3] + '%' + "</td>";
    html += "</tr>"
    table.innerHTML = html;
}

function GetCompanyTrend(company, year, month, day, chart_obj){
    $.ajax({
        type : "GET",
        async : true,
        url : "../../api/dashboard/data_overview_company_trend",
        data: {
            'company': company,
            'year': year,
            'month': month,
            'day': day
        },
        dataType : "json",
        success : function(result) {
            chart_obj.setOption({
                series:[{data: result}]
            });
        },
    })
}

$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/data_overview_company",    
    data: {
        'year': year,
        'quarter': quarter,
        'month': month,
        'day': day
    },
    dataType : "json",
    success : function(result) {
        let company = ["xt", "zc", "db", "jk", "jj1", "jj2", "jz"]
        for(let i in company){
            InsertTable(company[i], result[i]);
        }

        var option = {
            grid: {
                left: '4%',
                right: '4%',
                bottom: '6%',
                top: '6%',
                containLabel: true
            },
            xAxis: {
                data: [],
            },
            yAxis: {},
            series: [{
                name: '问题占比',
                type: 'line',
                data: []
            }]
        };
        var CompanyChart1 = echarts.init(document.getElementById('overview_chart_xt'));
        var CompanyChart2 = echarts.init(document.getElementById('overview_chart_zc'));
        var CompanyChart3 = echarts.init(document.getElementById('overview_chart_db'));
        var CompanyChart4 = echarts.init(document.getElementById('overview_chart_jk'));
        var CompanyChart5 = echarts.init(document.getElementById('overview_chart_jj1'));
        var CompanyChart6 = echarts.init(document.getElementById('overview_chart_jj2'));
        var CompanyChart7 = echarts.init(document.getElementById('overview_chart_jz'));
        CompanyChart1.setOption(option);
        CompanyChart2.setOption(option);
        CompanyChart3.setOption(option);
        CompanyChart4.setOption(option);
        CompanyChart5.setOption(option);
        CompanyChart6.setOption(option);
        CompanyChart7.setOption(option);
        
        let objs = [CompanyChart1, CompanyChart2, CompanyChart3, CompanyChart4, CompanyChart5, CompanyChart6, CompanyChart7]
        for(let i in objs){
            GetCompanyTrend(company[i], year, month, day, objs[i]);
        }
    },
})


// echarts部分
var color = [
"#60acfc",
"#32d3eb",
"#5bc49f",
"#feb64d",
"#ff7c7c",
"#9287e7",
"#009688"] ;

var myChart1 = echarts.init(document.getElementById('echarts1'));
var option = {
    color : '#ff7c7c',
    title : {
        text: '各公司平均问题占比（%）',
        subtext: '风险集市相关',
        x:'left'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {
            type : 'shadow'
        }
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    legend: {
        x: 'left',
        top: '15%',
    },
    dataset: {
        source: []
    },
    xAxis: [
        {type: 'category', gridIndex: 0},
    ],
    yAxis: [
        {gridIndex: 0},
    ],
    series: [
        {type: 'bar', seriesLayoutBy: 'row'},
        {type: 'bar', seriesLayoutBy: 'row'},
        {type: 'bar', seriesLayoutBy: 'row'},
        {type: 'bar', seriesLayoutBy: 'row'},
        {type: 'bar', seriesLayoutBy: 'row'},
        {type: 'bar', seriesLayoutBy: 'row'},
        {type: 'bar', seriesLayoutBy: 'row'},
    ],
    grid:{
        top: 100,
    },
    dataZoom: [{
        show: true,
        bottom: 0,
        start: 15,
        end: 75,
    },{
        type: 'inside',
        start: 94,
        end: 100
    }],
};
myChart1.setOption(option);
myChart1.showLoading();

$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/avg_problem_percentage",    
    data: {},
    dataType : "json",
    success : function(result) {
        myChart1.hideLoading();              //隐藏加载动画
        myChart1.setOption({                 //加载数据图表
        //渲染echarts
            dataset: {
                source: result
            },
        });
    },
})

var myChart2 = echarts.init(document.getElementById('echarts2'));
var option = {
    color: color,
    title : {
        text: '各公司同类问题Top 5统计',
        subtext: year + '-' + month + '-' + day +'（风险集市相关）',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
    },
    series : [{
        type: 'pie',
        radius : '55%',
        center: ['50%', '55%'],
        data: [],
        itemStyle: {
            emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
};
myChart2.setOption(option);
myChart2.showLoading();

$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/same_problem_top5",    
    data: {
        'year': year,
        'quarter': quarter,
        'month': month,
        'day': day
    },
    dataType : "json",
    success : function(result) {
        var names = result.name || []
        var values = result.value || []
        var data = []
        for(var i=0;i<names.length;i++){
            data.push({ name: names[i], value: values[i] })
        }
        myChart2.hideLoading();
        myChart2.setOption({
            series : [{
                data: data,
            }]
        });
    },
})


var myChart3 = echarts.init(document.getElementById('echarts3'));
var option = {
    color: color,
    title : {
        text: '各公司数据量占比',
        subtext: year + '-' + month + '-' + day +'（风险集市相关）',
        x:'left'
    },
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        y: 'bottom',
        data:['信托','资产','担保','金科','基金1','基金2','金租']
    },
    series: [
        {
            name:'数据库来源',
            type:'pie',
            selectedMode: 'single',
            radius: [0, '30%'],
            center: ['55%', '55%'],
            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: []
        },
        {
            name:'数据量占比',
            type:'pie',
            radius: ['40%', '55%'],
            center: ['55%', '55%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    backgroundColor: '#eee',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 22,
                            align: 'center'
                        },
                        hr: {
                            borderColor: '#aaa',
                            width: '100%',
                            borderWidth: 0.5,
                            height: 0
                        },
                        b: {
                            fontSize: 16,
                            lineHeight: 33
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [2, 4],
                            borderRadius: 2
                        }
                    }
                }
            },
            data:[]
        }
    ]
};
myChart3.setOption(option);
myChart3.showLoading();

$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/subcompany_data_percentage",    
    data: {
        'year': year,
        'quarter': quarter,
        'month': month,
        'day': day
    },
    dataType : "json",
    success : function(result) {
        myChart3.setOption({
            series: [{},
            {
                data: result
            }]
        });
    },
})

$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/count_db_rows",    
    data: {
        'year': year,
        'quarter': quarter,
        'month': month,
        'day': day
    },
    dataType : "json",
    success : function(result) {
        myChart3.hideLoading();
        myChart3.setOption({
            series: [{
                data: result
            }]
        });
    },
})



var myChart4 = echarts.init(document.getElementById('echarts4'));
var option = {
    color : ['#FFC000','#70AD47','#5B9BD5'],
    title : {
        text: '需求改造进度',
        subtext: year + 'Q' + quarter +'风险集市相关',
        x:'left'
    },
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data: ['未完成','已完成','无需改造']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'value'
    },
    yAxis: {
        type: 'category',
        data: []
    },
    series: [
        {
            name: '未完成',
            type: 'bar',
            stack: '总量',
            data: []
        },
        {
            name: '已完成',
            type: 'bar',
            stack: '总量',
            data: []
        },
        {
            name: '无需改造',
            type: 'bar',
            stack: '总量',
            data: []
        },
    ]
};

myChart4.setOption(option);
myChart4.showLoading();

// 请求接口数据-填充[问题数据统计]
$.ajax({
    type : "get",
    async : false,
    url : "../../static/resource/demand.json",    
    data: {},
    dataType : "json",
    success : function(result) {
        if (result) {
            //去重获取公司名
            var company = [];
            for(var i=1;i<result.length;i++){
                if (company.indexOf(result[i][1])==-1){
                    company.push(result[i][1]);
                }
            }

            //获取当前季度的列号
            var unfinished_list  = [];
            var finished_list    = [];
            var noneed_list      = [];
            for(var i=5;i<result[0].length;i++){
                if (result[0][i].substr(0,6) == '{{ quarter }}'){
                    var quarter = i;
                    break;
                }
            }
            //改造进度计数
            for(var i=0;i<company.length;i++){
                var unfinished_count = 0;
                var finished_count   = 0;
                var noneed_count     = 0;
                for (var t=1;t<result.length;t++){
                    if (result[t][1] != company[i]){
                        continue;
                    }
                    else{
                        if (result[t][quarter] == '进行中' || result[t][quarter] == '未完成' || result[t][quarter] == '未开展'){
                            unfinished_count++;
                        }
                        else if (result[t][quarter] == '完成'){
                            finished_count++;
                        }
                        else {
                            noneed_count++;
                        }
                    }
                }
                unfinished_list.push(unfinished_count);
                finished_list.push(finished_count);
                noneed_list.push(noneed_count);
            }

            myChart4.hideLoading();              //隐藏加载动画
            myChart4.setOption({                 //加载数据图表
            //渲染echarts
                yAxis: {
                    type: 'category',
                    data: company
                },
                series: [
                    {
                        data: unfinished_list
                    },
                    {
                        data: finished_list
                    },
                    {
                        data: noneed_list
                    },
                ]
            });

            //渲染table
            var html = "<thead><th>公司</th><th>未完成需求数</th><th>已完成需求数</th><th>完成率</th></thead><tbody>";
            var total_unfinished = 0;
            var total_finished   = 0;
            var total_noneed     = 0;
            for(var i=0;i<company.length;i++){
                var unfinished = unfinished_list[i]
                var finished   = finished_list[i]
                var noneed     = noneed_list[i]
                var finished_per = (finished+noneed)/(finished+noneed+unfinished)*100
                total_unfinished += unfinished;
                total_finished   += finished;
                total_noneed     += noneed;
                total_finished_per = (total_finished+total_noneed)/(total_finished+total_noneed+total_unfinished)*100
                html += "<tr>";
                html += "<td>" + company[i] + "</td>";
                html += "<td style=\"color:red;\">" + unfinished + "</td>";
                html += "<td style=\"color:green;\">" + (finished+noneed) + "</td>";
                html += "<td>" + finished_per.toFixed(2) + "%</td>";
                html += "</tr>";
            }
            html += "<tr style=\"font-weight: 600;\"><td>集团合计</td>"
            html += "<td style=\"color:red;\">" + total_unfinished + "</td>";
            html += "<td style=\"color:green;\">" + (total_finished+total_noneed) + "</td>";
            html += "<td>" + total_finished_per.toFixed(2) + "%</td></tr>";
            html += "</tbody>";
            document.getElementById("demand_table").innerHTML = html;
        }
    },
    error : function(errorMsg) {
        console.log(errorMsg);
    }
})

//集团总问题占比
var myChart5 = echarts.init(document.getElementById('echarts5'));
var option = {
    color: "#4CAF50",
    title : {
        text: '集团总问题占比（%）',
        subtext: '风险集市相关',
        x:'left'
    },
    xAxis: {
        type: 'category',
        data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: [],
        type: 'line',
        markPoint: {
            data: [
                {type: 'max', name: '最大值'},
                {type: 'min', name: '最小值'}
            ]
        },
    }],
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    dataZoom: [{
        show: true,
        bottom: 0,
        start: 0,
        end: 100,
        width: '70%',
        x: '15%'
    },
    {
        type: 'inside',
        start: 94,
        end: 100
    },
    ],
};
myChart5.setOption(option);
myChart5.showLoading();

$.ajax({
    type : "GET",
    async : false,
    url : "../../api/dashboard/total_trend",    
    data: {},
    dataType : "json",
    success : function(result) {
        myChart5.hideLoading();
        myChart5.setOption({
            xAxis: {
                data: result.datatime
            },
            series: [{
                data: result.value,
            }]
        });
    },
})

//根据窗口缩放动态调整echarts大小
$('.chart').resize(function(){
    myChart1.resize();
    myChart2.resize();
    myChart3.resize();
    myChart4.resize();
});