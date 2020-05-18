// 设置头像
function SetAvatar() {
    // 头像背景色
    let bgColor = [ //from  https://www.google.com/design/spec/style/color.html
        '#F44336', // red 500
        '#E91E63', // pink 500
        '#9C27B0', // purple 500,
        '#673AB7', // deep purple 500
        '#3F51B5', // indigo 500
        '#2196F3', // blue 500
        '#03A9F4', // light blue 500
        '#00BCD4', // cyan 500
        '#009688', // teal 500
        '#4CAF50', // green 500
        '#8BC34A', // light green 500
        '#CDDC39', // lime 500
        '#FFEB3B', // yellow 500
        '#FFC107', // amber 500
        '#FF9800', // orange 500
        '#FF5722', // deep orange 500
        '#795548', // brown 500
        '#9E9E9E', // grey 500
        '#607D8B', // blue grey 500
    ];

    username = localStorage.getItem("username");
    let myAvatar = document.getElementById('avatar');
    let index = Math.floor(Math.random() * bgColor.length);
    myAvatar.style.backgroundColor = bgColor[index];
    myAvatar.innerHTML = username.substr(0,1).toLocaleUpperCase();
}


// 获取年份
function GetYear(){
    let obj = document.getElementById('data_year');

    $.ajax({
        type : "GET",
        async : false,
        url : "../../api/date/year",
        data: {},
        dataType : "json",
        success : function(result) {
            if(localStorage.getItem('selected_year') == null){
                localStorage.setItem('selected_year', result.data[0]);
            }

            // 设置下拉框内容
            for(let i in result.data) {
                obj.options.add(new Option(result.data[i], result.data[i]));
            };
        },
    })
}


// 获取季度
function GetQuarter(){
    let opt = document.getElementById('data_year');
    let year = opt.options[opt.selectedIndex].value;
    $.ajax({
        type : "GET",
        async : false,
        url : "../../api/date/quarter",
        data: {
            'year': year
        },
        dataType : "json",
        success : function(result) {
            if(localStorage.getItem('selected_quarter') == null){
                localStorage.setItem('selected_quarter', result.data[0]);
            }

            // 设置下拉框内容
            var obj = document.getElementById('data_quarter');
            obj.options.length=0;
            for(let i in result.data) {
                obj.options.add(new Option(result.data[i], result.data[i]));
            };

            if (result.data.length == 1){
                GetMonth();
            }
        },
    })
}


// 获取月份
function GetMonth(){
    let opt = document.getElementById('data_year');
    let year = opt.options[opt.selectedIndex].value;

    opt = document.getElementById('data_quarter');
    let quarter = opt.options[opt.selectedIndex].value;

    $.ajax({
        type : "GET",
        async : false,
        url : "../../api/date/month",
        data: {
            'year': year,
            'quarter': quarter
        },
        dataType : "json",
        success : function(result) {
            if(localStorage.getItem('selected_month') == null){
                localStorage.setItem('selected_month', result.data[0]);
            }

            var obj = document.getElementById('data_month');
            obj.options.length=0;
            for(let i in result.data) {
                obj.options.add(new Option(result.data[i], result.data[i]));
            };

            if (result.data.length == 1){
                GetDay();
            }
        },
    })
}


// 获取天
function GetDay(){
    let opt = document.getElementById('data_year');
    let year = opt.options[opt.selectedIndex].value;

    opt = document.getElementById('data_quarter');
    let quarter = opt.options[opt.selectedIndex].value;

    opt = document.getElementById('data_month');
    let month = opt.options[opt.selectedIndex].value;

    $.ajax({
        type : "GET",
        async : false,
        url : "../../api/date/day",
        data: {
            'year': year,
            'quarter': quarter,
            'month': month
        },
        dataType : "json",
        success : function(result) {
            // 若未选择过数据日期，则显示最新日期数据
            if(localStorage.getItem('selected_day') == null){
                localStorage.setItem('selected_day', result.data[0]);
                // 刷新页面
                history.go(0);
            }

            var obj = document.getElementById('data_day');
            obj.options.length=0;
            for(let i in result.data) {
                obj.options.add(new Option(result.data[i], result.data[i]));
            };
        },
    })
}


// 监听日期选择事件，根据所选的年/季/月更改下拉框中显示的日期
function ChangeDataDate(){
    let opt = document.getElementById('data_year');
    let year = opt.options[opt.selectedIndex].value;

    opt = document.getElementById('data_quarter');
    let quarter = opt.options[opt.selectedIndex].value;

    opt = document.getElementById('data_month');
    let month = opt.options[opt.selectedIndex].value;

    opt = document.getElementById('data_day');
    let day = opt.options[opt.selectedIndex].value;

    localStorage.setItem("selected_year", year);
    localStorage.setItem("selected_quarter", quarter);
    localStorage.setItem("selected_month", month);
    localStorage.setItem("selected_day", day);

    //url = './?year=' + year + '&quarter=' + quarter + '&month=' + month + '&day=' + day;
    //修改localstorge存放的日期后，刷新页面
    window.location.reload();
}


// 设置默认显示的日期
function InitSelectedDate(){
    // 根据用户上一次选择的日期，设置下拉框的默认显示日期
    var year = localStorage.getItem("selected_year");
    var quarter = localStorage.getItem("selected_quarter");
    var month = localStorage.getItem("selected_month");
    var day = localStorage.getItem("selected_day");

    // 若未有选择过日期，默认显示最新日期
    if(year||quarter||month||day == null){
        GetYear();
        GetQuarter();
        GetMonth();
        GetDay();
    }
    else{
        GetYear();
        let opt = document.getElementById('data_year');
        for(let i=0;i<opt.length;i++){
            if(opt[i].value == year){
                opt[i].selected = true;
            }
        }
    
        GetQuarter();
        opt = document.getElementById('data_quarter');
        for(i=0;i<opt.length;i++){
            if(opt[i].value == quarter){
                opt[i].selected = true;
            }
        }
    
        GetMonth();
        opt = document.getElementById('data_month');
        for(i=0;i<opt.length;i++){
            if(opt[i].value == month){
                opt[i].selected = true;
            }
        }
    
        GetDay();
        opt = document.getElementById('data_day');
        for(i=0;i<opt.length;i++){
            if(opt[i].value == day){
                opt[i].selected = true;
            }
        }
    }
}

function init(){
    // 设置头像
    SetAvatar();

    // 设置日期
    if (document.getElementById('data_year') != null){
        InitSelectedDate();
    }
}

