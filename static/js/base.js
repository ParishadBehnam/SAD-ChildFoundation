/**
 * Created by afra on 12/13/17.
 */

$('.emergency-need-admin').click(function() {
    if ($(this).hasClass("badge-secondary")) {
        $(this).removeClass('badge-secondary').addClass('badge-danger');
        //$('<p>نیاز فوری برای تایید به مدیر ارسال می‌شود</p>').appendTo($(this).parent())
    }else {
        $(this).removeClass('badge-danger').addClass('badge-secondary');
        $(this).parent().contents().filter(function(){ return this.tagName == 'P'; }).remove();

    }
});

$('.emergency-need').click(function() {
    if ($(this).hasClass("badge-secondary")) {
        $(this).removeClass('badge-secondary').addClass('badge-danger');
        $('<p>نیاز فوری برای تایید به مدیر ارسال می‌شود</p>').appendTo($(this).parent())
    }else {
        $(this).removeClass('badge-danger').addClass('badge-secondary');
        $(this).parent().contents().filter(function(){ return this.tagName == 'P'; }).remove();

    }
});

$(function(){
    $(document).on("change","input", function(){
        var allGood=true;
        var lastInputField=0;
        $("input").each(function() {
            if ($(this).val() =="") {
                allGood=false;
                return false;
            }
            lastInputField++;
        });

        if (allGood) {
            $("<span>" + lastInputField + "<input type='text' id='lastinputfieldId" + lastInputField +"'" +
              "name='lastinputfieldName" + lastInputField + "'></span>").appendTo("form");
        }
    });
});
​
