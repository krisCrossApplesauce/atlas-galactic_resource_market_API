// Function to set the height and width of text-container and path-container based on rocket image size
function setTextContainerHeight() {
    var rocketHeight = $(".rocket-image").height();
    // Set text-container height
    $(".text-container").height((rocketHeight / 2.35) + "px");

    var rocketWidth = $(".rocket-image").width();
    // Set text-container width
    $(".text-container").width((rocketWidth / 1.75) + "px");

    // Set path-container height
    if (rocketHeight < 450) {
        $(".path-container").height((rocketHeight / 2.3) + "px");
    } else {
        $(".path-container").height((rocketHeight / 2.2) + "px");
    }

    // Set path-container width
    $(".path-container").width((rocketWidth / 1.75) + "px");
}

// Function to fetch and populate data in text-container based on type (systems, planets, resources)
function fetchAndPopulateData(type) {
    // Clear the text container
    $(".text-container").empty();

    $.get(`/${type}`)
    .done(function(data) {
        let text = `[${type.toUpperCase()} Data]<br>`;
        let color = ""
        if (type == "resources") { color = "purple_hoverable"; }
        if (type == "systems") { color = "orange_hoverable"; }
        data.forEach(result => {
            text += `<span class="result ${color}">${result}</span><br>`;
        });
        $(".text-container").html(`<p>${text}</p>`);

        // Click event listener for result elements
        $(".result").click(function() {
            let selectedResult = $(this).text();
            if (type == "systems") {
                fetchSelectedData(type, selectedResult);
            }
            if (type == "resources") {
                fetchSelectedResourceData(type, selectedResult);
            }
            if (type == "planets") {
                console.log('planets button calls fetchAndPopulateData function instead of its own fetchAndPopulatePlanetsData function');
                fetchSelectedPlanetData(type, selectedResult);
            }
        });
    })
    .fail(function() {
        $(".text-container").html('<p class="grey2">Error, cannot load data</p>');
    });
}

function fetchAndPopulatePlanetsData() {
    // Clear the text container
    $(".text-container").empty();

    $.get(`/planets`)
    .done(function(data) {
        let text = `[Planets Data]<br>`;
        let systems = [];
        let colors = ["green", "blue", "orange", "purple", "grey"];
        let i = 0;
        data.forEach(result => {
            if (!systems.includes(result[1])) {
                // if (i == 4) { i = 0; } else { i += 1; }
                systems.push(result[1]);
                // if (systems.length != 1) { text += `<br>`; }
                text += `<span class="orange">${result[1]} System:</span><br>`;
            }
            text += `<span class="planets_result blue_hoverable">${result[0]}</span><br>`;
        });
        $(".text-container").html(`<p>${text}</p>`);

        // Click event listener for result elements
        $(".planets_result").click(function() {
            let selectedResult = $(this).text();
            fetchSelectedPlanetData("planets", selectedResult);
        });
    })
    .fail(function() {
        $(".text-container").html('<p class="grey2">Error, cannot load data</p>');
    });
}

function fetchSelectedData(type, selectedResult) {
    // Check if selectedResult contains a comma
    if (selectedResult.includes(',')) {
        // Split the string at the comma and take the first part
        selectedResult = selectedResult.split(',')[0].trim();
    }

    if (type == "planets") {
        fetchPlanetData(type, selectedResult);
    } else if (type == "resources") {
        fetchSelectedResourceData(type, selectedResult);
    } else {
        $.get(`/${selectedResult}`)
            .done(function(data) {
                let text = `<span class="orange">Selected Star:</span> <span class="orange2">${selectedResult}</span><br>`;
                text += `[${selectedResult.toUpperCase()} System Data]<br>`;
                data.forEach(result => {
                    text += `<span class="planets_result blue_hoverable">${result}</span><br>`;
                });
                $(".text-container").html(`<p>${text}</p>`);

                // Click event listener for result elements
                $(".planets_result").click(function() {
                    let selectedResult = $(this).text();
                    fetchSelectedPlanetData("planets", selectedResult);
                });
            })
            .fail(function() {
                $(".text-container").html('<p class="grey2">Error, cannot load data</p>');
            });
    }
}

function fetchSelectedPlanetData(type, selectedResult) {
    // Check if selectedResult contains a comma
    if (selectedResult.includes(',')) {
        // Split the string at the comma and take the first part
        selectedResult = selectedResult.split(',')[0].trim();
    }

    $.get(`/${selectedResult}`)
        .done(function(data) {
            let text = `<span class="blue">Selected Planet:</span> <span class="blue2">${selectedResult}</span><br>`;
            text += `[${selectedResult.toUpperCase()} Data]<br>`;
            let i = 0;
            data.forEach(result => {
                let rString = `${result}`
                if (rString.includes(',') || i > 0) {
                    result.forEach(resultFromList => {
                        text += `<span class="resource_result purple_hoverable">${resultFromList}</span><br>`;
                    });
                } else {
                    text += `<span class="orange2">System:</span> <span class="system_result orange_hoverable">${result}</span><br><span class="purple2">Resources:</span><br>`;
                    i += 1;
                }
            });
            $(".text-container").html(`<p>${text}</p>`);

            // Click event listener for result elements
            $(".resource_result").click(function() {
                let selectedResult = $(this).text();
                fetchSelectedResourceData("resources", selectedResult);
            });

            $(".system_result").click(function() {
                let selectedResult = $(this).text();
                fetchSelectedData("systems", selectedResult);
            });
        })
        .fail(function() {
            $(".text-container").html('<p class="grey2">Error, cannot load data</p>');
        });
}

function fetchSelectedResourceData(type, selectedResult) {
    // Check if selectedResult contains a comma
    if (selectedResult.includes(',')) {
        // Split the string at the comma and take the first part
        selectedResult = selectedResult.split(',')[0].trim();
    }

    $.get(`/${selectedResult}`)
        .done(function(data) {
            let text = `<span class="purple">Selected Resource:</span> <span class="purple2">${selectedResult}</span><br>`;
            text += `[${selectedResult.toUpperCase()} Data]<br>`;
            let systems = [];
            data.forEach(result => {
                if (!systems.includes(result[1])) {
                    systems.push(result[1]);
                    if (systems.length != 1) { text += `<br>`; }
                    text += `<span class="orange">${result[1]} System:</span><br>`;
                }
                text += `<span class="planets_result blue_hoverable">${result[0]}</span><br>`;
            });
            $(".text-container").html(`<p>${text}</p>`);

            // Click event listener for result elements
            $(".planets_result").click(function() {
                let selectedResult = $(this).text();
                fetchSelectedPlanetData("planets", selectedResult);
            });
        })
        .fail(function() {
            $(".text-container").html('<p class="grey2">Error, cannot load data</p>');
        });
}


$(function () {
    // Set initial sizes on page load
    setTextContainerHeight();

    // Event listener for Systems paragraph click
    $("#systems").click(function() {
        fetchAndPopulateData("systems");
    });

    // Event listener for Planets paragraph click
    $("#planets").click(function() {
        fetchAndPopulatePlanetsData("planets");
    });

    // Event listener for Resources paragraph click
    $("#resources").click(function() {
        fetchAndPopulateData("resources");
    });
});

// Update sizes on window resize
window.addEventListener('resize', setTextContainerHeight);