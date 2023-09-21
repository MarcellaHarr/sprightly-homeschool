// Social Studies' socViewLesson.html

document.addEventListener("DOMContentLoaded", function () {
    // Handle the insert form submission
    document.getElementById("socSubmitResponse").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="soc-submitResp-form-uid"]');
        const socRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(socRespForm, `/socViewLesson/${lessonNumber}`);
    });

    // Handle the upload form submission
    document.getElementById("socViewUpldSubmit").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="soc-viewupload-form-uid"]');
        const socRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(socRespForm, `/socViewUploads/${lessonNumber}`);

        // Reset upload after submission
        form.reset();
    });
});

function submitForm(socRespForm, url) {
    // Perform the AJAX request
    fetch(url, {
        method: "POST",
        body: socRespForm
    })
    .then(response => response.text())
    .then(data => {
        // Display in console
        console.log(data);

        // Clear the form input fields
        const form = document.querySelector('form[data-uid="soc-submitResp-form-uid"]');
        form.reset(); // This will reset all form fields to their default values
    })
    .catch(error => {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
    });
}