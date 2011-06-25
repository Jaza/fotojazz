fotojazz.operations = function() {
    function update_orientation_progress(key) {
        $.getJSON(SCRIPT_ROOT + '/reorient/progress/', {
            'key': key
        }, function(data) {
            $('#operation-reorient-progress').html(data.percent + '%');
            if (!data.done) {
                setTimeout(function() {
                    update_orientation_progress(data.key);
                }, 100);
            }
            else {
                $('#operation-reorient-progress').html($('#operation-reorient-progress').html() + ' Done!');
            }
        });
    }
    
    return {
        init: function() {
            $('#operation-reorient').click(function() {
                var filenames_input = [];
                var filebrowse_path = $('#id_path').val();
                $('.filebrowse-checkbox:checked').each(function() {
                    var filename = $(this).val();
                    filenames_input.push(filebrowse_path + filename);
                });
                $.getJSON(SCRIPT_ROOT + '/reorient/start/', {
                    'filenames_input': filenames_input.join(' ')
                }, function(data) {
                    $('#operation-reorient-progress').html(data.percent + '%');
                    setTimeout(function() {
                        update_orientation_progress(data.key);
                    }, 100);
                });
                return false;
            });
        }
    }
}();


$(function() {
    fotojazz.operations.init();
});
