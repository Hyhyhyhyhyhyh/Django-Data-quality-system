var year = localStorage.getItem("selected_year");
var quarter = localStorage.getItem("selected_quarter");
var month = localStorage.getItem("selected_month");
var day = localStorage.getItem("selected_day");

//报告标题
var obj = document.getElementById("report_title");
obj.innerHTML = "粤财控股"+ year + 'Q' + quarter +"数据质量报告(" + year + '-' + month + '-' + day + ")";

//总结概述
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
        let text = document.getElementById("summary_1");
        let html = "&nbsp;&nbsp;本季度对对信托、资产、再担保、金科、基金创投、中银粤财、金租七个公司风险集市相关共" + result.all_cnt + "条数据进行检查，合计问题数" + result.problem_cnt + "，问题占比"+ result.problem_per +"%。";
        html += '<font style="font-style:italic;size:21.3px;font-family:SimSun;color:rgb(91, 155, 213);text-decoration:underline;">补充环比统计和需求完成情况统计</font>';
        text.innerHTML = html;
    },
})

//各公司风险集市相关数据质量概况
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
        let text = document.getElementById("summary_2");
        var html = "";
        for (i of result){
            html += "<tr>";
            html += "<td>"+ year + 'Q' + quarter +"</td>";
            html += "<td>"+ i[0] +"</td>";
            html += "<td>"+ i[1] +"</td>";
            html += "<td>"+ i[2] +"</td>";
            html += "<td>"+ i[3] +"%</td>";
            html += "</tr>";
        }
        text.innerHTML = html;
    },
})

//填充各公司检核结果明细
for (i of ["ycxt", "yczc", "gdzdb", "ycjk", "fdct", "zyyc", "jz"]){
    $.ajax({
        type : "GET",
        async : false,
        url : "../../api/quality/report",
        data: {
            'year': year,
            'quarter': quarter,
            'month': month,
            'day': day,
            'company': i
        },
        dataType : "json",
        success : function(result) {
            let text = document.getElementById("table_"+i);
            var html = "";
            for (let t of result.data){
               html += "<tr>";
               html += "<td>"+ t.check_item +"</td>";
               html += "<td>"+ t.problem_type +"</td>";
               html += "<td>"+ t.problem_count +"</td>";
               html += "<td>"+ t.item_count +"</td>";
               html += "<td>"+ t.problem_per +"</td>";
               html += "<td></td>"
               html += "</tr>";
            }
            text.innerHTML = html;
        },
    })
}