$(document).ready(function () {
    // Enabling Bootstrap tooltip
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    // Remove messages automatically
    fadeOutMessages();

    // Remove messages manually
    $(".message-close").click(function() { 
        $(this).parent().fadeOut('fast', function () {
            $(this).remove()
        })
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