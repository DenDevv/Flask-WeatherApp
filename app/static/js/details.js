$(document).ready(function () {
    $(".block__details__title").click(function(event) {
        if ($(".block__details").hasClass("one")){
            $(".block__details__title").not($(this)).removeClass("active");
            $(".block__details__text").not($(this).next()).slideUp(300);
        }
        $(this).toggleClass('active').next().slideToggle(300);
    });
});