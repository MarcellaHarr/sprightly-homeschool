// History's histViewLesson.html

document.addEventListener("DOMContentLoaded", function () {
    // Handle the insert form submission
    document.getElementById("histSubmitResponse").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="hist-submitResp-form-uid"]');
        const histRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(histRespForm, `/histViewLesson/${lessonNumber}`);
    });

    // Handle the upload form submission
    document.getElementById("histViewUpldSubmit").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="hist-viewupload-form-uid"]');
        const histRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(histRespForm, `/histViewUploads/${lessonNumber}`);

        // Reset upload after submission
        form.reset();
    });
});

function submitForm(histRespForm, url) {
    // Perform the AJAX request
    fetch(url, {
        method: "POST",
        body: histRespForm
    })
    .then(response => response.text())
    .then(data => {
        // Display in console
        console.log(data);

        // Clear the form input fields
        const form = document.querySelector('form[data-uid="hist-submitResp-form-uid"]');
        form.reset(); // This will reset all form fields to their default values
    })
    .catch(error => {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
    });
}