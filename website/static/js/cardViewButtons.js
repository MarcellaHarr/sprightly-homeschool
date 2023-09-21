// Language Arts Lesson Cards

// Function to handle the "View" button click
function handleViewButtonClick(event) {
    const button = event.target;
    const lessonNumber = button.getAttribute('data-lesson-number');
    // Check if the lesson number is in local storage
    let viewCount = localStorage.getItem(`viewCount_${lessonNumber}`);
    viewCount = viewCount ? parseInt(viewCount) : 0;

    if (viewCount < 2) {
        // Enable the button for the first two clicks
        viewCount++;
        localStorage.setItem(`viewCount_${lessonNumber}`, viewCount);
    }
    // Disable the button after the second click
    if (viewCount >= 2) {
        button.disabled = true;
        button.classList.add('btn-disabled');
        localStorage.setItem(`viewButtonDisabled_${lessonNumber}`, 'true');
    }
    // Show hover message if the button is disabled
    if (button.disabled) {
        button.classList.add('btn-disabled');
    }
}

// Function to check and restore the state of the "View" button on page load
function restoreViewButtonState() {
    const viewButtons = document.querySelectorAll('.btn-view');

    viewButtons.forEach((button) => {
        const lessonNumber = button.getAttribute('data-lesson-number');
        const viewCount = localStorage.getItem(`viewCount_${lessonNumber}`);

        if (viewCount >= 2) {
            // Disable the button if it was clicked twice
            button.disabled = true;
            button.classList.add('btn-disabled');
        }
    });
}

// Get all the "View" buttons with the class "btn-view"
const viewButtons = document.querySelectorAll('.btn-view');

// Attach the click event listener to each "View" button
viewButtons.forEach((button) => {
    button.addEventListener('click', handleViewButtonClick);
});

// Call the function to restore the button state when the page loads
window.addEventListener('load', restoreViewButtonState);

