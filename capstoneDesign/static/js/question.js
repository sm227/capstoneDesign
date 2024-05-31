function showSpinner() {
    document.getElementById('loading-spinner').style.display = 'block';
    document.getElementById('loading-overlay').style.display = 'block';
    sessionStorage.setItem('showSpinner', 'true');
}

function hideSpinner() {
    document.getElementById('loading-spinner').style.display = 'none';
    document.getElementById('loading-overlay').style.display = 'none';
    sessionStorage.removeItem('showSpinner');
}

$(document).ready(function () {
    $('#question-form').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        showSpinner();

        // Get the form data
        var formData = $(this).serialize();
        var realId = $('#question-form [name="real_id"]').val()
        console.log(realId);
        var url = '/question/' + encodeURIComponent(realId) + '/'

        // textarea 초기화
        $('#memo-text').val('')
        console.log(realId)
        // Send AJAX request
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            // data:JSON.stringify(answer),
            // dataType: 'json',
            success: function (response) {
                console.log("Success");
                console.log(response)
                $('#answerResult').html(response['answer']);
                hideSpinner();
            },
            error: function (xhr, errmsg, err) {
                // Handle error
                console.log(errmsg);
            }
        });
    });
});
