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
    // Clear the text container
    $(".text-container").empty();

    $.get(`/${type}`)
    .done(function(data) {
        let text = `${type.toUpperCase()} Data:<br>`;
        data.forEach(result => {
            text += `<span class="result">${result}</span><br>`;
        });
        $(".text-container").html(`<p>${text}</p>`);

        // Click event listener for result elements
        $(".result").click(function() {
            let selectedResult = $(this).text();
            fetchSelectedData(type, selectedResult);
        });
    })
    .fail(function() {
        $(".text-container").html("<p>Error, cannot load data</p>");
    });
}

function fetchSelectedData(type, selectedResult) {
    // Check if selectedResult contains a comma
    if (selectedResult.includes(',')) {
        // Split the string at the comma and take the first part
        selectedResult = selectedResult.split(',')[0].trim();
    }

    $.get(`/${selectedResult}`)
        .done(function(data) {
            let text = `Selected ${type.toUpperCase()}: ${selectedResult}<br>`;
            text += `${type.toUpperCase()} Data: `;
            data.forEach(result => {
                console.log(result);
                let rString = `${result}`
                if (rString.includes(',')) {
                    // Split the string at the comma and take the first part
                    result.forEach(resultFromList => {
                        text += `${resultFromList}<br>`;
                    });
                } else {
                    text += `${result}<br>`;
                }
            });
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