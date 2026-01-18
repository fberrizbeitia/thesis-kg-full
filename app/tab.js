document.addEventListener('DOMContentLoaded', () => {
    // Select all tab buttons and tab content elements
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    /**
     * Activates a specific tab and displays its content, while deactivating others.
     * @param {string} tabId - The ID of the tab content to show (e.g., 'theses').
     */
    const showTab = (tabId) => {
        // 1. Hide all tab content sections
        tabContents.forEach(content => {
            content.classList.remove('active');
        });

        // 2. Deactivate all tab buttons (remove active styling)
        tabButtons.forEach(button => {
            button.classList.remove('active');
        });

        // 3. Show the selected tab content
        const selectedContent = document.getElementById(tabId);
        if (selectedContent) {
            selectedContent.classList.add('active');
        }

        // 4. Activate the corresponding tab button
        const selectedButton = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
        if (selectedButton) {
            selectedButton.classList.add('active');
        }
    };

    // Add click event listeners to each tab button
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Get the 'data-tab' attribute value, which corresponds to the content ID
            const tabId = button.dataset.tab;
            showTab(tabId);
        });
    });

    // Initialize: Set the first tab as active when the page loads
    // This ensures one tab is always visible from the start.
    if (tabButtons.length > 0) {
        showTab(tabButtons[4].dataset.tab);
    }
});