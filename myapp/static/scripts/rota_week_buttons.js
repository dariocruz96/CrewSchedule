
document.getElementById('next-week-btn').addEventListener('click', function() {
    
    console.log('Button clicked!'); // Log a message to the console when the button is clicked
    // Get the current URL
    var currentUrl = window.location.href;

    // Parse the URL to extract query parameters
    var url = new URL(currentUrl);
    
    // Get the current value of the 'start_of_week' parameter
    var startOfWeekParam = url.searchParams.get('start_of_week');
    
    if (startOfWeekParam) {
        // Parse the current value into a JavaScript Date object
        var startDate = new Date(startOfWeekParam);

        // Calculate the start of the next week by adding 7 days
        startDate.setDate(startDate.getDate() + 7);

        // Find the nearest Monday
        var nextMonday = new Date(startDate);
        var dayOfWeek = nextMonday.getDay();
        var daysUntilMonday = dayOfWeek === 1 ? 7 : 1 - dayOfWeek; // Adjust for Monday as the first day of the week
        nextMonday.setDate(nextMonday.getDate() + daysUntilMonday);

        // Format the next Monday's date to match Django's expected format ('YYYY-MM-DD')
        var formattedNextMonday = nextMonday.toISOString().slice(0, 10).replace(/-/g, '/');

        // Update the 'start_of_week' parameter in the URL
        url.searchParams.set('start_of_week', formattedNextMonday);

        // Redirect to the updated URL
        window.location.href = url.toString();
    } else {
        // Get the start_of_week value provided in the Django template
        var startOfWeek = new Date('{{ start_of_week|date:"Y-m-d" }}');

        // Calculate the start of the next week by adding 7 days
        startOfWeek.setDate(startOfWeek.getDate() + 7);
        console.log(startOfWeek)
        

        // Format the next Monday's date to match Django's expected format ('YYYY-MM-DD')
        var formattedNextMonday = startOfWeek.toISOString().slice(0, 10).replace(/-/g, '/');

        // Update the 'start_of_week' parameter in the URL
        url.searchParams.set('start_of_week', formattedNextMonday);

        // Redirect to the updated URL
        window.location.href = url.toString();
    }
    })
    document.getElementById('view-week-btn').addEventListener('click', function() {
        // Get the selected date from the input field
        var selectedDate = new Date(document.getElementById('week-picker').value);
        var year = selectedDate.getFullYear();
        var month = ('0' + (selectedDate.getMonth() + 1)).slice(-2); // Adding 1 to month because it's 0-indexed
        var day = ('0' + selectedDate.getDate()).slice(-2);

        // Create a string in the format 'YYYY/MM/DD'
        var formattedDate = year + '/' + month + '/' + day;
        // Construct the URL with the selected date as the start_of_week parameter
        var url = '/manage-rota/?start_of_week=' + formattedDate;
        
        // Redirect to the URL
        window.location.href = url;
    });