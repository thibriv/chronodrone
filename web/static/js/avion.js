jQuery(function ($) {

        $('header h1').on('click', function () { /* clic sur la balise h1*/
            message();
        });

        $('img[src="static/images/soirees.jpg"]').on('click', function () {
             $('header p').show();
        });
});




function message() {
    console.log('bien vise');
    let contenu=$('header').html();
    /*alert(contenu);*/

    $('header h1').html('Voici le titre 2');

    $('img[src="static/images/soirees.jpg"]').css('border','10px solid red');

    let att=$('section:last').attr('id');
    console.log("l'attribut id vaut:"+att);

    $('header p').hide();
}

function montre()
{
    $('header p').show();

}