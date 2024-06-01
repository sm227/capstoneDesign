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

    $('#question-button').click(function(event) {
        $('#question-tab').css({
            'display':'block'
        })

        $('#add-memo-form').css({
            'display':'none'
        })
    })

    $('#question-form').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        showSpinner();

        // Get the form data
        var formData = $(this).serialize();
        var realId = $('#question-form [name="real_id"]').val()
        console.log(realId);
        var url = '/question/' + encodeURIComponent(realId) + '/'

        // textarea 초기화

        $('#question-text').val('')
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

                //marked.parse 로 마크다운 형식으로 변환
                const markedResponse = marked.parse(response['answer']) 
                $('#answerResult').html(markedResponse);
                hideSpinner();
            },
            error: function (xhr, errmsg, err) {
                // Handle error
                console.log(errmsg);
            }
        });
    });
});

