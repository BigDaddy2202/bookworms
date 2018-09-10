function loadResults() {
    var result = "";
    for (var i = 0; i < 10; i++) {
        result += "<li>Result " + i + "</li>";
    }
    $.ajax({
        url: "/echo/html/",
        type: "post",
        data: {
            html: result,
            delay: 3
        },
        beforeSend: function(xhr) {
            $("#results").after($("<li class='loading'>Loading...</li>").fadeIn('slow')).data("loading", true);
        },
        success: function(data) {
            var $results = $("#results");
            $(".loading").fadeOut('fast', function() {
                $(this).remove();
            });
            var $data = $(data);
            $data.hide();
            $results.append($data);
            $data.fadeIn();
            $results.removeData("loading");
        }
    });
};

$(function() {
    loadResults();

    $(".scrollpane").scroll(function() {
        var $this = $(this);
        var $results = $("#results");

        if (!$results.data("loading")) {

            if ($this.scrollTop() + $this.height() == $results.height()) {
                loadResults();
            }
        }
    });
});