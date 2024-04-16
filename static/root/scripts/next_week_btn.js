document.getElementById('next-week-btn').addEventListener('click', function() {
    
    console.log('Button clicked!'); // Log a message to the console when the button is clicked
    // Get the current URL
    var currentUrl = window.location.href;

    // Parse the URL to extract query parameters
    var url = new URL(currentUrl);
    
    // Get the current value of the 'start_of_week' parameter
    var startOfWeekParam = url.searchParams.get('start_of_week');
    
    // If the 'start_of_week' parameter exists
    if (startOfWeekParam) {
        // Parse the current value into a JavaScript Date object
        var startDate = new Date(startOfWeekParam);

        // Calculate the start of the next week by adding 7 days
        startDate.setDate(startDate.getDate() + 7);

        // Find the nearest Monday
        var nextMonday = new Date(startDate);
        nextMonday.setDate(nextMonday.getDate() - nextMonday.getDay() + 1);

        // Format the next Monday's date to match Django's expected format ('YYYY-MM-DD')
        var formattedNextMonday = nextMonday.toISOString().slice(0, 10).replace(/-/g, '/');

        // Update the 'start_of_week' parameter in the URL
        url.searchParams.set('start_of_week', formattedNextMonday);

        // Redirect to the updated URL
        window.location.href = url.toString();
    }
    else{
        // Use the provided start_of_week value
    var formattedNextMonday = '{{ start_of_week|date:"Y/m/d" }}';

    // Update the 'start_of_week' parameter in the URL
    url.searchParams.set('start_of_week', formattedNextMonday);
    console.log("here2" + formattedNextMonday)
    // Redirect to the updated URL
    window.location.href = url.toString();
    }
});
