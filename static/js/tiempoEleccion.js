function tiempo(clicked_id){
    document.getElementById(clicked_id).innerHTML = "pulsado"
    Flask.url_for('calcula_tiempo', {clicked_id});
}