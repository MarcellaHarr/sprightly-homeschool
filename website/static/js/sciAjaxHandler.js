// Science's sciViewLesson.html

document.addEventListener("DOMContentLoaded", function () {
    // Handle the insert form submission
    document.getElementById("sciSubmitResponse").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="sci-submitResp-form-uid"]');
        const sciRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(sciRespForm, `/sciViewLesson/${lessonNumber}`);
    });

    // Handle the upload form submission
    document.getElementById("sciViewUpldSubmit").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="sci-viewupload-form-uid"]');
        const sciRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(sciRespForm, `/sciViewUploads/${lessonNumber}`);

        // Reset upload after submission
        form.reset();
    });
});

function submitForm(sciRespForm, url) {
    // Perform the AJAX request
    fetch(url, {
        method: "POST",
        body: sciRespForm
    })
    .then(response => response.text())
    .then(data => {
        // Display in console
        console.log(data);

        // Clear the form input fields
        const form = document.querySelector('form[data-uid="sci-submitResp-form-uid"]');
        form.reset(); // This will reset all form fields to their default values
    })
    .catch(error => {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
    });
}