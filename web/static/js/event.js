jQuery(function ($) {
    $('.fa-times').on('click', function () {
        let id_comment=$(this).parents().eq(0).attr('id');
        alert(id_comment);

       $.post('/delComment',{ id:id_comment}, function (data) {
            console.log(data);
            $('li#'+id_comment).remove();
            $("div.info").show().html("Le commentaire a bien été supprimé");

            setTimeout(function () {$("div.info").html('');}, 3000);

        });


    });
});