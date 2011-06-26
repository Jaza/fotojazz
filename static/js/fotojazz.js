fotojazz.operations = function() {
    function process_start(process_css_name, process_class_name) {
        $('#operation-' + process_css_name).click(function() {
            var filenames_input = get_filenames_list();
            $.getJSON(SCRIPT_ROOT + '/process/start/' + process_class_name + '/', {
                'filenames_input': filenames_input.join(' ')
            }, function(data) {
                $('#operation-' + process_css_name).attr('disabled', 'disabled');
                $('#operation-' + process_css_name + '-progress').progressbar('option', 'disabled', false);
                $('#operation-' + process_css_name + '-progress').progressbar('option', 'value', data.percent);
                setTimeout(function() {
                    process_progress(process_css_name, process_class_name, data.key);
                }, 100);
            });
            return false;
        });
    }
    
    function process_progress(process_css_name, process_class_name, key) {
        $.getJSON(SCRIPT_ROOT + '/process/progress/' + process_class_name + '/', {
            'key': key
        }, function(data) {
            $('#operation-' + process_css_name + '-progress').progressbar('option', 'value', data.percent);
            if (!data.done) {
                setTimeout(function() {
                    process_progress(process_css_name, process_class_name, data.key);
                }, 100);
            }
            else {
                $('#operation-' + process_css_name).removeAttr('disabled');
                $('#operation-' + process_css_name + '-progress').progressbar('option', 'value', 0);
                $('#operation-' + process_css_name + '-progress').progressbar('option', 'disabled', true);
                refresh_photos();
            }
        });
    }
    
    function get_filenames_list() {
        var filenames_input = [];
        var filebrowse_path = $('#id_path').val();
        $('.filebrowse-checkbox:checked').each(function() {
            var filename = $(this).val();
            filenames_input.push(filebrowse_path + filename);
        });
        return filenames_input;
    }
    
    function refresh_photos(check_all) {
        if (check_all == undefined) {
            check_all = false;
        }
        var filebrowse_path = $('#id_path').val();
        var filenames_input = get_filenames_list();
        $('#filebrowse-display').load(SCRIPT_ROOT + '/photos/?photos_path=' + filebrowse_path + '&check_all=' + (check_all ? '1' : '0') + '&filenames_input=' + encodeURIComponent(filenames_input.join(' ')));
    }
    
    return {
        init: function() {
            $('.operation-progress').progressbar({'disabled': true});
            
            $('#select-all').click(function() {
                $('.filebrowse-checkbox').attr('checked', 'checked');
                return false;
            });
            $('#select-none').click(function() {
                $('.filebrowse-checkbox').removeAttr('checked');
                return false;
            });
            
            $('#id_path').keyup(function() {
                refresh_photos(true);
                return true;
            });
            
            process_start('reorient', 'ExifTranProcess');
        }
    }
}();


$(function() {
    fotojazz.operations.init();
});
