const header = document.querySelector('.menu');

window.onscroll = function(){
    var top = window.scrollY;
    if (top >= 35){
        header.classList.add('sticky');
    }else{
        header.classList.remove('sticky');
    }
}