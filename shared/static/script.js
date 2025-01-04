$(document).ready(function () {
    // Enabling Bootstrap tooltip
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    // Remove messages (automatically and manually)
    fadeOutMessages();
    closeMessage();
});

const fadeOutMessages = () => {
    const lifetimeInMs = 5000;
    if ($(".messages").length > 0) {
        setTimeout(() => {
            $(".messages").fadeOut("slow", function () {
                $(this).remove();
            });
        }, lifetimeInMs);
    }
}

const closeMessage = () => {
    $(".message-close").click(function (e) { 
        e.preventDefault();
        $(this).parent().fadeOut('fast', function () {
            $(this).remove()
        })
    });
}