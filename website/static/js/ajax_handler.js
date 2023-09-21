// Ajax Handler for uploads.html //

document.addEventListener("DOMContentLoaded", function () {
    // Handle the insert form submission
    document.getElementById("insertSubmitBtn").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="insert-form-uid"]');
        const formData = new FormData(form);
        submitForm(formData, "/insert");
    });

    // Handle the upload form submission
    document.getElementById("uploadSubmitBtn").addEventListener("click", function (event) {
        event.preventDefault(); // Prevent the default form submission behavior
        const form = document.querySelector('form[data-uid="upload-form-uid"]');
        const formData = new FormData(form);
        submitForm(formData, "/uploads");

        // Reset upload after submission
        form.reset();
    });
});

function submitForm(formData, url) {
    // Perform the AJAX request
    fetch(url, {
        method: "POST",
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        // Display in console
        console.log(data);

        // Clear the form input fields
        const form = document.querySelector('form[data-uid="insert-form-uid"]');
        form.reset(); // This will reset all form fields to their default values
    })
    .catch(error => {
        // Handle any errors that occurred during the AJAX request
        console.error(error);
    });
}
