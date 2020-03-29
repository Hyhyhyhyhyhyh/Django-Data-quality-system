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
            var obj = document.getElementById('data_day');
            obj.options.length=0;
            for(let i in result.data) {
                obj.options.add(new Option(result.data[i], result.data[i]));
            };
        },
    })

    // 根据上一次用户选择的日期设置为下拉框的默认日期
    y = localStorage.getItem("year");

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
    //根据用户上一次选择的日期，设置下拉框的默认显示日期
    var year = localStorage.getItem("selected_year");
    var quarter = localStorage.getItem("selected_quarter");
    var month = localStorage.getItem("selected_month");
    var day = localStorage.getItem("selected_day");

    if([year, quarter, month, day] == [null, null, null, null]){
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

    // 初始化gojs
    if (document.getElementById('myDiagramDiv') != null){
        var company = localStorage.getItem('selected_company');
            if (company == undefined ){
                company = '信托';
            }
            var data;
            jQuery.ajax({
                type : "GET",
                async : false,
                url : "../../api/check/blood_analyze",
                data: {'company': company},
                dataType : "json",
                success : function(result) {
                    data = result.data;
                },
            })

            var $ = go.GraphObject.make;  // for conciseness in defining templates

            myDiagram =
                $(go.Diagram, "myDiagramDiv",
                {
                    initialAutoScale: go.Diagram.UniformToFill,
                    // define the layout for the diagram
                    layout: $(go.TreeLayout, { nodeSpacing: 5, layerSpacing: 30 })
                });

            // Define a simple node template consisting of text followed by an expand/collapse button
            myDiagram.nodeTemplate =
                $(go.Node, "Horizontal",
                    { isTreeExpanded: false },  // 设置默认叶子节点全折叠
                //{ selectionChanged: nodeSelectionChanged },  // 点击叶子节点触发的动作
                $(go.Panel, "Auto",
                    $(go.Shape, { fill: "#1F4963", stroke: null }), //叶子节点背景色
                    $(go.TextBlock,                                 //叶子节点文字style
                    {
                        font: "bold 13px Helvetica, bold Arial, sans-serif",
                        stroke: "white", margin: 3
                    },
                    new go.Binding("text", "key"))
                ),
                $("TreeExpanderButton")                           //展开收缩叶子节点的按钮
                );

            // 节点间的连接线
            myDiagram.linkTemplate =
                $(go.Link,
                { selectable: true },
                $(go.Shape));  // the link shape

            // 构建树
            myDiagram.model =
                $(go.TreeModel, {
                isReadOnly: true,  // 禁止删除或复制节点
                //nodeDataArray: traverseDom(document.activeElement)
                nodeDataArray: data
                });

            //设置默认展开的叶子节点层级
            myDiagram.addDiagramListener("InitialLayoutCompleted", function(e) {
                e.diagram.findTreeRoots().each(function(r) { r.expandTree(1); });
            });
    }
}

