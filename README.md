# DeutschFlashCard
Enhance Flashcard App with View Tracking, Pagination, and Quiz Mode
# Detailed Description

This update introduces the following key enhancements to the Flashcard App:

    -View All Flashcards with Pagination:
        Displays flashcards in pages with a customizable number of cards per page.
        Includes Previous and Next navigation buttons for seamless browsing.
        Tracks and displays the number of times each flashcard has been viewed.

   - View Tracking and Highlighting:
        Each flashcard's "seen" count is incremented when it is viewed.
        Flashcards viewed 5 or more times are highlighted in green for easy identification.

    -Randomized Quiz Mode:
        Presents a randomized term from the flashcard list and four translation options (one correct, three incorrect).
        Highlights the selected button as green if correct or red if incorrect.
        Tracks and displays a summary of correct and incorrect answers at the end of the quiz.

    -Bug Fixes:
        Fixed missing or incorrect method references (show_flashcards_page, show_flashcard_popup).
        Ensured smooth navigation between pages in "View All Flashcards."

    -Improved Code Modularity:
        Refactored methods to improve readability and maintainability.
        Ensured proper state management and persistence of data.

## How to Use

   1. View All Flashcards:
        Add multiple flashcards.
        Click View All Flashcards to browse through the cards with pagination.

   2. Quiz Mode:
        Click Quiz Mode to test your knowledge.
        Select the correct translation from four options.
        Correct answers are highlighted green; incorrect answers red.

   3. Persistent Storage:
        Flashcards and their view counts are saved to a local JSON file (flashcards.json) for persistence across sessions.
