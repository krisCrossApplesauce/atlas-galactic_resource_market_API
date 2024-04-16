// Function to set the height and width of text-container and path-container based on rocket image size
function setTextContainerHeight() {
    var rocketHeight = $(".rocket-image").height();
    // Set text-container height
    $(".text-container").height((rocketHeight / 2.35) + "px");

    var rocketWidth = $(".rocket-image").width();
    // Set text-container width
    $(".text-container").width((rocketWidth / 1.75) + "px");

    // Set path-container height
    $(".path-container").height((rocketHeight / 2.2) + "px");

    // Set path-container width
    $(".path-container").width((rocketWidth / 3.9) + "px");
}

// Function to fetch and populate data in text-container based on type (systems, planets, resources)
function fetchAndPopulateData(type) {
    $.get(`/data/${type}`)
    .done(function(data) {
        let text = `Welcome to the Galactic Resource Market - ${type.toUpperCase()} Data: ${data}`;
        $(".text-container").html(`<p>${text}</p>`);
    })
    .fail(function() {
        $(".text-container").html("<p>Error, cannot load data</p>");
    });
}

// Set initial sizes on page load
$(function () {
    setTextContainerHeight();

    // Event listener for Systems paragraph click
    $("#systems").click(function() {
        fetchAndPopulateData("systems");
    });

    // Event listener for Planets paragraph click
    $("#planets").click(function() {
        fetchAndPopulateData("planets");
    });

    // Event listener for Resources paragraph click
    $("#resources").click(function() {
        fetchAndPopulateData("resources");
    });
});

// Update sizes on window resize
window.addEventListener('resize', setTextContainerHeight);
