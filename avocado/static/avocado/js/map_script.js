let globalX = 0;
let globalY = 0;

$(document).on('mousemove', function(e) {
    globalX = e.pageX;
    globalY = e.pageY;
    console.log(globalX, globalY)
});

$('.zoom-img-block').on('mousemove', function(e){
    let zoom = 5;
    let img = $(this).find('.zoom-img-item').attr('href');
    let imgBlock = $(this).find('.zoom-img-item img');
    let imgWidth = imgBlock.width();
    let imgHeight = imgBlock.height();    
    let overlay = $('.zoom-img-overlay');
    let cursor = $('.zoom-img-cursor');
    cursor.css('width', overlay.width() / zoom + 'px');
    cursor.css('height', overlay.height() / zoom + 'px');
    let cursorWidth = cursor.outerWidth();
    let cursorHeight = cursor.outerHeight();
    let posX = globalX - $(this).offset().left - cursorWidth / 2;
    let posY = globalY - $(this).offset().top - cursorHeight / 2;

    if (posX < 0) {
        posX = 0;
    }
    if (posX > (imgWidth - cursorWidth)) {
        posX = imgWidth - cursorWidth;
    }
    if (posY < 0) {
        posY = 0;
    }
    if (posY > (imgHeight - cursorHeight)) {
        posY = imgHeight - cursorHeight;
    }

    cursor.css('left', posX + 'px');
    cursor.css('top', posY + 'px');
    cursor.show();

    posX *= zoom;
    posY *= zoom;
    overlay.css('background-image', `url(${img})`);
    overlay.css('background-size', (imgWidth * zoom) +'px');
    overlay.css('background-position', `-${posX}px -${posY}px`);
    overlay.show();
});

$('.zoom-img-block').on('mouseleave', function () {
    $('.zoom-img-cursor').hide();
    $('.zoom-img-overlay').hide();
});
