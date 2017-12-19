/**
 * Created by afra on 12/13/17.
 */
$('.emergency-need').click(function() {
    if ($(this).hasClass("badge-secondary")) {
        $(this).removeClass('badge-secondary').addClass('badge-danger');
        $('<p>نیاز فوری برای تایید به مدیر ارسال می‌شود</p>').appendTo($(this).parent())
    }else {
        $(this).removeClass('badge-danger').addClass('badge-secondary');
        $(this).parent().contents().filter(function(){ return this.tagName == 'P'; }).remove();

    }
});


$('.emergency-need-admin').click(function() {
    if ($(this).hasClass("badge-secondary")) {
        $(this).removeClass('badge-secondary').addClass('badge-danger');
        $('<p>نیاز فوری برای تایید به مدیر ارسال می‌شود</p>').appendTo($(this).parent())
    }else {
        $(this).removeClass('badge-danger').addClass('badge-secondary');
        $(this).parent().contents().filter(function(){ return this.tagName == 'P'; }).remove();

    }
});
