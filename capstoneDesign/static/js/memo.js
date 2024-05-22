document.addEventListener("DOMContentLoaded", function () {
        const addMemoButton = document.getElementById("add-memo"); // id가 "add-memo"인 요소를 찾아 'addMomoButton'에 할당 <<-- 메모 추가 버튼
        const memoListLink = document.querySelector('.nav-tabs .nav-item:nth-child(2) .nav-link'); // 메모 보기 탭 보기
        const memoList = document.getElementById("memo-list"); // id가 "memo-list"인 요소를 찾아 'memolist'에 할당
        const memoItems = document.getElementById("memo-items"); // 메모 목록에 들어가는 아이템이 들어가는 리스트




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



    //메모 보기 탭
    $(document).ready(function () {
        $("#loadData").click(function () {
            $.ajax({
                url: '/my-ajax-url/', // 요청을 보낼 서버의 URL
                type: 'get', // HTTP 메소드
                dataType: 'json', // 응답 데이터 타입
                success: function (response) {
                    console.log(response)
                    $('#memo-list').empty()

                    // 응답으로 받은 items 리스트를 순회하면서 각 항목을 ul 태그에 추가
                    $.each(response.items, function (i, item) {
                        // 이미 목록에 있는 아이템인지 확인
                       if (!$(`#memo-list li[data-id="${item.id}"]`).length) {
                        const memoItem = document.createElement("li"); // 새 리스트 생성
                        const currentTime = player.getCurrentTime()
                        const changeTime = changeSeconds(currentTime)

                        memoItem.className = "list-group list-group-item"; // 부트스트랩 5 목록 그룹 클래스 추가
                        memoItem.setAttribute("data-id", item.id); // 아이디 속성 추가
                        memoItem.innerHTML = `
                            <div class="row align-items-center">
                                <div class="col-9">
                                    <div class="d-flex align-items-center">
                                        <div class="btn btn-primary btn-sm btn-fixed-size" style="width: 55px" href="#" role="button" onclick="moveTime(${currentTime});">${changeTime}</div>
                                        <div class="text-start ms-2 memo-container">${item.text}</div>
                                    </div>
                                </div>
                                <div class="col-3">
                                    <p></p>
                                    <p></p>
                                    <button class="btn btn-sm btn-primary editMemo" type="button">수정</button>
                                    <button class="btn btn-sm btn-danger deleteMemo" type="button">삭제</button>
                                </div>
                            </div>
                            <!--<div class="d-flex justify-content-between align-items-end">
                                <div>
                                    <div class="fw-bold text-sm" style="font-size: 10px;">${item.id}</div>
                                    <div>${item.text}</div>
                                </div>
                                <div>
                                    <button class="btn btn-sm btn-primary editMemo" type="button">수정</button>
                                    <button class="btn btn-sm btn-danger deleteMemo" type="button">삭제</button>
                                </div>
                            </div>-->
                        `;
                        $('#memo-list').append(memoItem); // 목록 그룹에 append
                    }
                    });
                    console.log("서버 요청 성공!")
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


    $(document).on("click", ".editMemo", function () {
    const memoItem = $(this).closest("li");
    const memoId = memoItem.data("id");
    const memoText = memoItem.find('.memo-text').text(); // 메모 텍스트 가져오기

    $('#editMemoModal').modal('show'); // 모달 열기
    $('#editMemoText').val(memoText); // 모달 내부의 텍스트 에어리어에 메모 내용 표시

    // "저장" 버튼 클릭 시 수정된 내용을 저장하는 이벤트 핸들러
    $('#saveEditedMemo').off().on('click', function () {
        const editedMemoText = $('#editMemoText').val(); // 수정된 메모 내용 가져오기

        // 수정된 내용을 서버에 전송
        $.ajax({
            url: '/edit-memo/',
            type: 'POST',
            data: {
                memo_id: memoId,
                text: editedMemoText
            },
            dataType: 'json',
            success: function (response) {
                console.log("서버 응답:", response);
                // 수정된 내용을 메모 리스트에 업데이트
                memoItem.find('.memo-text').text(editedMemoText);
                $('#editMemoModal').modal('hide'); // 모달 닫기

                $('#memo-list').empty()

                    // 응답으로 받은 items 리스트를 순회하면서 각 항목을 ul 태그에 추가
                    $.each(response.items, function (i, item) {
                        // 이미 목록에 있는 아이템인지 확인
                       if (!$(`#memo-list li[data-id="${item.id}"]`).length) {
                        const memoItem = document.createElement("li"); // 새 리스트 생성
                        const currentTime = player.getCurrentTime()
                        const changeTime = changeSeconds(currentTime)

                        memoItem.className = "list-group list-group-item"; // 부트스트랩 5 목록 그룹 클래스 추가
                        memoItem.setAttribute("data-id", item.id); // 아이디 속성 추가
                        memoItem.innerHTML = `
                            <div class="row align-items-center">
                                <div class="col-9">
                                    <div class="d-flex align-items-center">
                                        <div class="btn btn-primary btn-sm btn-fixed-size" style="width: 55px" href="#" role="button" onclick="moveTime(${currentTime});">${changeTime}</div>
                                        <div class="text-start ms-2 memo-container">${item.text}</div>
                                    </div>
                                 </div>
                                <div class="col-3">
                                    <p></p>
                                    <p></p>
                                    <button class="btn btn-sm btn-primary editMemo" type="button">수정</button>
                                    <button class="btn btn-sm btn-danger deleteMemo" type="button">삭제</button>
                                </div>
                            </div>
                        `;
                        $('#memo-list').append(memoItem); // 목록 그룹에 append
                    }
                    });
            },
            error: function(xhr, status, error){
                console.error("서버 오류:", error);
            }
        });
    });
});