document.addEventListener("DOMContentLoaded", function () {
    // Handle the insert form submission
    document.getElementById("elaSubmitResponse").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="ela-submitResp-form-uid"]');
        const elaRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(elaRespForm, `/elaViewLesson/${lessonNumber}`);
    });

    // Handle the upload form submission
    document.getElementById("elaViewUpldSubmit").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="ela-viewupload-form-uid"]');
        const elaRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(elaRespForm, `/elaViewUploads/${lessonNumber}`);

        // Reset upload after submission
        form.reset();
    });
});

function submitForm(elaRespForm, url) {
    // Perform the AJAX request
    fetch(url, {
        method: "POST",
        body: elaRespForm
    })
    .then(response => response.text())
    .then(data => {
        // Display in console
        console.log(data);

        // Clear the form input fields
        const form = document.querySelector('form[data-uid="ela-submitResp-form-uid"]');
        form.reset(); // This will reset all form fields to their default values
    })
    .catch(error => {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
    });
}
