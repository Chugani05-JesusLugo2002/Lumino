$(document).ready(function () {
    // Enabling Bootstrap tooltip
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    // Remove messages (automatically and manually)
    fadeOutMessages();
    closeMessage();

    // Navigation
    $("#navigation-button").click(function(e) {
        displayMap();
    });
});

const fadeOutMessages = () => {
    const lifetimeInMs = 5000;
    if ($(".messages").length > 0) {
        setTimeout(() => {
            $(".messages").fadeOut("slow", function() {
                $(this).remove();
            });
        }, lifetimeInMs);
    }
}

const closeMessage = () => {
    $(".message-close").click(function() { 
        $(this).parent().fadeOut('fast', function () {
            $(this).remove()
        })
    });
}

const displayMap = () => {
    $("nav").fadeToggle()
}