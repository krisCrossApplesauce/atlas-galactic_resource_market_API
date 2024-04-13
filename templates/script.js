function setTextContainerHeight() {
    var rocketHeight = $(".rocket-image").height();
    // console.log("\nrocketHeight: " + rocketHeight + "\n");
    $(".text-container").height((rocketHeight / 2.35) + "px");
    // console.log("textHeight: " + $(".text-container").height() + "\n");

    var rocketWidth = $(".rocket-image").width();
    // console.log("rocketWidth: " + rocketWidth + "\n");
    $(".text-container").width((rocketWidth / 1.75) + "px");
    // console.log("textWidth: " + $(".text-container").width() + "\n");
}

$(function () {
    setTextContainerHeight();
});

window.addEventListener('resize', setTextContainerHeight);

