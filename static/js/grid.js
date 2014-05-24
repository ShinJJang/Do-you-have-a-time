$(function() {
    $(".selectable").bind("mousedown", function(e) {
        e.metaKey = true;
    }).selectable({
        filter: "td:not('.date')",
        selected: function (event, ui) {
                if ($(ui.selected).hasClass('click-selected')) {
                    $(ui.selected).removeClass('ui-selected click-selected');

                } else {
                    $(ui.selected).addClass('click-selected');

                }
            },
        unselected: function (event, ui) {
            $(ui.unselected).removeClass('click-selected');
        }
    });

    $.djangocsrf("enable");

});

$(".selectable td").click(function(e) {
    $(this).toggleClass("ui-selected");
});

$("#done_grid").click(function() {
    var result = [];
    $(".ui-selected").each(function() {
        result.push($(this).attr("tag"));
    });
    console.log(result);
    var data = JSON.stringify({
        "times": result,
        "planid": planid
    });
    console.log(data);
    $.ajax({
        url: "/done/",
        type: "POST",
        contentType: "application/json",
        data: data,
        statusCode: {
            200: function (data) {
                $("#result").html("<div class='alert alert-success'>\
                <strong>제출 완료</strong> 결과보기로 가능한 약속 시간을 확인해 보세요\
                </div>")
            },
            401: function () {
                facebook_login();
            }
        }
    });
    return false;
});

function set_result(result) {
    if(result != false) {
        $(".time").each(function(index) {
            var location = $(this).attr("tag");
            for (var i = 0; i < result.length; i++) {
                if (location == result[i]) {
                    return true;
                }
            }
            $(this).toggleClass("ui-result");
        });
    }
}

$("#result_grid").click(function() {
    $.ajax({
        url:"/result/"+planid,
        type: "GET",
        dataType: 'json',
        statusCode:{
            200: function(data) {
                grid_clear();
                set_result(data);
            },
            401: function () {
                facebook_login();
            }
        }
    });
    return false;
});

function grid_clear() {
    $(".ui-selected").each(function() {
        $(this).toggleClass("ui-selected click-selected");
    });
    $(".ui-result").each(function() {
        $(this).toggleClass("ui-result");
    });
}

$("#reset_grid").click(function() {
    grid_clear();
    $("#result").html("<div class='alert alert-info'> \
    <strong>어떻게 씀?</strong> 약속이 안되는 시간을 그려주세요!! \
    </div>");
    return false;
});

function facebook_login() {
    alert("페이스북 로그인을 해주세요!");
}

$("#donation").click(function() {
   alert("써주시는게 기부입니다! 불편한 점이 있으시면 알려주세요!");
});

$("#makeplanform").submit(function() {
    var planname = $("input[name='planname']").val();
    if (planname.trim() == '') {
        $("input[name='planname']").val("");
        alert("모임명을 입력해주세요!");
        return false;
    }
    var data = JSON.stringify({
        'planname': planname
    });
    $.ajax({
        url: "/make/",
        type: "POST",
        dataType: "json",
        data: data,
        statusCode: {
            200: function(data) {
                window.location.href = data.planid;
            },
            401: function() {
                facebook_login();
            }
        }
    });
    return false;
});