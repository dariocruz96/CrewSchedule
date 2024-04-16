$(document).ready(function() {
    // Your JavaScript code here
    $('#id_start_time').change(function() {
        var startHour = parseInt($(this).val().split(':')[0]);
        $('#id_end_time option').each(function() {
            var endHour = parseInt($(this).val().split(':')[0]);
            $(this).prop('disabled', endHour <= startHour);
        });
    });
});