fotojazz.operations = function() {
    function reorient_start() {
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
                    reorient_progress(data.key);
                }, 100);
            });
            return false;
        });
    }
    
    function reorient_progress(key) {
        $.getJSON(SCRIPT_ROOT + '/reorient/progress/', {
            'key': key
        }, function(data) {
            $('#operation-reorient-progress').html(data.percent + '%');
            if (!data.done) {
                setTimeout(function() {
                    reorient_progress(data.key);
                }, 100);
            }
            else {
                $('#operation-reorient-progress').html($('#operation-reorient-progress').html() + ' Done!');
                refresh_photos();
            }
        });
    }
    
    function refresh_photos() {
        var filebrowse_path = $('#id_path').val();
        $('#filebrowse-display').load(SCRIPT_ROOT + '/photos/?photos_path=' + filebrowse_path);
    }
    
    return {
        init: function() {
            reorient_start();
        }
    }
}();


$(function() {
    fotojazz.operations.init();
});
