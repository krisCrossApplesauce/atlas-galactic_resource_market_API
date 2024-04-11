function setTextContainerHeight() {
    var element = document.getElementById('rocket-image');
    var positionInfo = element.getBoundingClientRect();
    var height = positionInfo.height;
    console.log(height);
    $('.text-container').css("height", height + "px");
}

$(document).ready(function () {
    setTextContainerHeight();
});

window.addEventListener('resize', setTextContainerHeight());

