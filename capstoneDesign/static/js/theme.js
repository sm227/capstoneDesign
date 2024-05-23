$(document).ready(function () {
    // 페이지 로드 시 저장된 테마 설정을 불러와 적용
    let savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        $('html').attr("data-bs-theme", savedTheme);
    }
    updateCardTheme();

    // 아이콘 클릭 시 다크 모드와 라이트 모드 간 전환
    $('#mode-icon').click(function () {
        let mode = $('html').attr("data-bs-theme");
        if (mode == 'dark') {
            $('html').attr("data-bs-theme", "light");
            localStorage.setItem("theme", "light"); // 다크 모드 설정 저장
        } else {
            $('html').attr("data-bs-theme", "dark");
            localStorage.setItem("theme", "dark"); // 라이트 모드 설정 저장
        }
        updateCardTheme();
    });
});

// 테마에 따라 카드 배경색 업데이트
function updateCardTheme() {
    let theme = $('html').attr("data-bs-theme");
    // 현재 모드와 반대되는 모드로 설정
    if (theme == 'dark') {
        $('#mode-icon').attr("class", "bi-moon-stars");
    } else {
        $('#mode-icon').attr("class", "bi-sun");
    }
}