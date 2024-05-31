$(document).ready(function() {
    $('#add-memo-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission


        if (typeof player !== 'undefined') {
            var currentTime = player.getCurrentTime();
            console.log("currentTime is " + currentTime);
            $('#currenttime').val(currentTime); // Set the value of the hidden input field
        }

        // Get the form data
        var formData = $(this).serialize();
        var videoId = $('#add-memo-form [name="video_id"]').val()
        console.log(videoId);
        var url = '/add-memo/' + encodeURIComponent(videoId) + '/'

        // textarea 초기화
        $('#memo-text').val('') 
        
        console.log(videoId)
        // Send AJAX request
        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                console.log("Success");
            },
            error: function(xhr, errmsg, err) {
                // Handle error
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
        const addMemoButton = document.getElementById("add-memo"); // id가 "add-memo"인 요소를 찾아 'addMomoButton'에 할당 <<-- 메모 추가 버튼
        const memoListLink = document.querySelector('.nav-tabs .nav-item:nth-child(2) .nav-link'); // 메모 보기 탭 보기
        const memoList = document.getElementById("memo-list"); // id가 "memo-list"인 요소를 찾아 'memolist'에 할당
        const memoItems = document.getElementById("memo-items"); // 메모 목록에 들어가는 아이템이 들어가는 리스트

        $('#memo-tab-button').click(function(event) {
            $('#memo-tab').css({
                'display':'block'
            })

            $('#memo-card-body').css({
                'display':'none'
            })
        })

        $('#loadMemo').click(function(event) {
            $('#memo-tab').css({
                'display':'none'
            })

            $('#memo-card-body').css({
                'display':'block'
            })
        })

        // 초를 분으로 변경하는 함수
        function changeSeconds(seconds) {
            if (seconds < 61) {
                return '00:' + addZero(seconds)
            }
            // sec
            var hours = Math.floor(seconds / 3600)
            var mins = Math.floor((seconds - hours * 3600) / 60)
            var secs = Math.floor(seconds % 60)
            return addZero(hours) + ':' + addZero(mins) + ':' + addZero(secs)

            function addZero(num) {
                return ((num < 10) ? '0' : '') + num
            }
        }

        memoListLink.addEventListener("click", function () {
            memoList.style.display = "block";
        });

        // 모달 설정 1
        window.addEventListener("click", function (event) {
            const memoModal = document.getElementById("memoModal");
            if (event.target === memoModal) {
                $('#memoModal').modal('hide');
            }
        });

        // 모달 설정 2
        $('#memoModal').on('shown.bs.modal', function () {
            $(document.body).addClass('modal-open');
        });

        // 모달 설정 3
        $('#memoModal').on('hidden.bs.modal', function () {
            $(document.body).removeClass('modal-open');
        });

        // 모달 설정 4
        $('#memoModal').on('click', function (event) {
            event.stopPropagation();
        });
    });

    function changeSeconds(seconds) {
        if (seconds < 61) {
            return addZero(Math.floor(seconds / 60)) + ':' + addZero(Math.floor(seconds % 60));
        }

        var hours = Math.floor(seconds / 3600);
        var mins = Math.floor((seconds - hours * 3600) / 60);
        var secs = Math.floor(seconds % 60);
        return (hours > 0 ? addZero(hours) + ':' : '') + addZero(mins) + ':' + addZero(secs);

        function addZero(num) {
            return ((num < 10 && num >= 0) ? '0' : '') + num;
        }
    }

    // 메모 보기 탭
    $(document).ready(function () {
        $("#loadMemo").click(function () {
            var videoId = $(this).data("video-id");
            console.log(videoId);
            var url = '/list-memo/' + encodeURIComponent(videoId) + '/';

            $.ajax({
                url: url, // URL to send the request to
                type: 'get', // HTTP method
                dataType: 'json', // Expected response data type
                success: function (response) {
                    console.log(response);
                    $('#memo-list #dataList').empty(); // Clear the current list

                    // Iterate over the items received from the response
                    $.each(response.items, function (i, item) {
                        if (!$(`#memo-list li[data-id="${item.id}"]`).length) {
                            // Create the list item element
                            const memoItem = document.createElement("li");
                            memoItem.className = "list-group list-group-item"; // Bootstrap list group class
                            memoItem.setAttribute("data-id", item.id); // Set the data-id attribute

                            var currentTime = item.current_time;
                            var changedTime = changeSeconds(currentTime);

                            memoItem.innerHTML = `
                                <div class="row align-items-center">
                                    <div class="col-9">
                                        <div class="d-flex align-items-center">
                                            <div class="btn btn-primary btn-sm btn-fixed-size" style="width: 55px" role="button" onclick="moveTime(${currentTime});">${changedTime}</div>
                                            <div class="text-start ms-2 memo-container memo-text">${item.text}</div>
                                        </div>
                                    </div>
                                    <div class="col-3">
                                        <button class="btn btn-sm btn-primary editMemo" type="button">수정</button>
                                        <button class="btn btn-sm btn-danger deleteMemo" type="button">삭제</button>
                                    </div>
                                </div>
                            `;

                            $('#memo-list #dataList').append(memoItem); // Append the list item to the list
                        }
                    });
                    console.log("Server request successful!");
                },
                error: function (xhr, status, error) {
                    console.error("Server error:", error);
                }
            });
        });
    });

    $(document).on("click", ".editMemo", function () {
        const memoItem = $(this).closest("li");
        const memoId = memoItem.data("id");
        const memoTextElement = memoItem.find('.memo-text'); // Get memo text element
        const memoText = memoTextElement.text(); // Get memo text content

        $('#editMemoModal').modal('show'); // Open modal
        $('#editMemoText').val(memoText); // Set the textarea value in the modal

        // "Save" button click event handler
        $('#saveEditedMemo').off().on('click', function () {
            const editedMemoText = $('#editMemoText').val(); // Get the edited memo content

            // Send the updated content to the server
            $.ajax({
                url: '/edit-memo/',
                type: 'POST',
                data: {
                    memo_id: memoId,
                    text: editedMemoText
                },
                dataType: 'json',
                success: function (response) {
                    console.log("edited memo is " + editedMemoText);
                    console.log("Server response:", response);
                    // Update the memo text in the memo item immediately
                    memoTextElement.text(editedMemoText);
                    $('#editMemoModal').modal('hide'); // Close modal
                },
                error: function(xhr, status, error){
                    console.error("Server error:", error);
                }
            });
        });
    });







    //삭제
    $(document).on("click", ".deleteMemo", function () {
        const memoItem = $(this).closest("li");
        const memoId = memoItem.data("id");


        $.ajax({
            url: '/delete-memo/',
            type: 'POST',
            data: {
                memo_id: memoId
            },
            dataType: 'json',
            success: function (response) {
                console.log("서버 응답:", response);


                memoItem.remove();
            },
            error: function(xhr, status, error){
                console.error("서버 오류:", error);
            }
        });
    });




