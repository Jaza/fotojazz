fotojazz.operations = function() {
    return {
        init: function() {
            $('#operation-reorient').click(function() {
                var filenames_input = [];
                var filebrowse_path = $('#id_path').val();
                $('.filebrowse-checkbox:checked').each(function() {
                    var filename = $(this).val();
                    filenames_input.push(filebrowse_path + filename);
                });
                $.getJSON(SCRIPT_ROOT + '/reorient/', {
                    'filenames_input': filenames_input.join(' ')
                }, function(data) {
                    alert(data.percent);
                });
                return false;
            });
        }
    }
}();


$(function() {
    fotojazz.operations.init();
});
