$(function() {
    $('button#calculate').bind('click', function() {
        $('#result').text('');
        $('button#calculate').attr('disabled', 'disabled');
        $('button#calculate').text('Calculating...');

        $.getJSON($SCRIPT_ROOT + '/_getRolesAJAX', {
            'roleName': $('select[name="roleName"]').find(":selected").val(),
            'num': $('select[name="num"]').find(":selected").val()
        }, function(data) {
            $("<ol>").appendTo('#result');
            $.each( data.champPool, function(i, champ) {
                $("<li>").text(champ + "  |  Score: " + data.roleStats[champ]['score']).appendTo('#result ol');
            });

            $('button#calculate').removeAttr('disabled');
            $('button#calculate').text('Calculate');
        });
        return false;
    });
});
