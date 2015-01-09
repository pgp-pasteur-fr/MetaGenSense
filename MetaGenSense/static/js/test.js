$(document).ready(function(){
    var csrftoken = $.cookie('csrftoken'); // Création du cookie du token CSRF
    $('#testform').submit(function(){ // Évènement Submit du formulaire
        var submitButton = $(":submit", this);
        submitButton.attr('disabled', true); // Désactivation du bouton Submit
        $('.error', this).removeClass('error'); // Réinitialisation des erreurs
        $('.error-tooltip', this).hide();
        $.ajax({ // Requête Ajax
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            crossDomain: false,
            beforeSend: function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }).done(function(data){
            if(data.success){
                alert(data.message); // Affiche le message retourné par la vue
            } else{ // Applique une classe CSS aux champs en erreur et affiche le texte
                $.each(data.error_fields, function(field, error){
                    $('#' + field).addClass('error');
                    $('#error_' + field).html(error).fadeIn(300);
                })
            }
        }).fail(function(data){
            alert(data.status + ': ' + data.statusText);
        }).always(function(){
            submitButton.attr('disabled', false);
        });
        return false;
    });
});