$(document).on("click", ".btn-warning", function (event) {
    event.preventDefault();

    var button = $(this);
    var taskId = button.attr("href").split("/").filter(Boolean).pop();

    $.ajax({
        url: "/todo/change_priority/" + taskId + "/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        success: function (response) {
            if (response.success) {
                var priorityBadge = $("#priority-" + taskId);
                var newPriority = response.priority;

                priorityBadge
                    .text(newPriority.charAt(0).toUpperCase() + newPriority.slice(1))
                    .removeClass("bg-danger bg-warning bg-secondary")
                    .addClass(
                        newPriority === "high" ? "bg-danger" :
                        newPriority === "medium" ? "bg-warning" :
                        "bg-secondary"
                    );
            } else {
                alert("Error: " + response.error);
            }
        },
        error: function () {
            alert("An error occurred while changing the priority.");
        }
    });
});
