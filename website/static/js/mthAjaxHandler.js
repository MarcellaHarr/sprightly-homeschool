// Math's mthViewLesson.html

document.addEventListener("DOMContentLoaded", function () {
    // Handle the insert form submission
    document.getElementById("mthSubmitResponse").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="mth-submitResp-form-uid"]');
        const mthRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(mthRespForm, `/mthViewLesson/${lessonNumber}`);
    });

    // Handle the upload form submission
    document.getElementById("mthViewUpldSubmit").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="mth-viewupload-form-uid"]');
        const mthRespForm = new FormData(form);
        const lessonNumber = form.getAttribute('data-lesson-number');
        submitForm(mthRespForm, `/mthViewUploads/${lessonNumber}`);

        // Reset upload after submission
        form.reset();
    });
});

function submitForm(mthRespForm, url) {
    // Perform the AJAX request
    fetch(url, {
        method: "POST",
        body: mthRespForm
    })
    .then(response => response.text())
    .then(data => {
        // Display in console
        console.log(data);

        // Clear the form input fields
        const form = document.querySelector('form[data-uid="mth-submitResp-form-uid"]');
        form.reset(); // This will reset all form fields to their default values
    })
    .catch(error => {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
    });
}