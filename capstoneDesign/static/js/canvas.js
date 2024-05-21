let selectedColor = '#000000'; //색깔 고른거 저장
const markerPenT = 0.01; //형광펜 투명도 조절
let drawing = false;
let ctx;
let activeTool = ''; //현재 그리기 도구
let eraserSize = 10; //지우개 크기

document.addEventListener('DOMContentLoaded', function() {
    //웹 페이지 로딩 되었을 때 querySelector안에 있는 클래스를 가진 버튼 안보이게 설정
    document.querySelector('.pen1-floating-btn').classList.add('hide');
    document.querySelector('.pen2-floating-btn').classList.add('hide');
    //document.querySelector('.eraser-btn').classList.add('hide');
    document.querySelector('.eraserAll-btn').classList.add('hide');

    //캔버스를 웹 사이트 전체로 설정
    const canvas = document.getElementById('drawing-canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx = canvas.getContext('2d');
    //캔버스 조작
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mousemove', draw);

    //터치스크린
    canvas.addEventListener('touchstart', startDrawing, {passive:false});
    canvas.addEventListener('touchend', stopDrawing, {passive:false});
    canvas.addEventListener('touchmove', draw, {passive:false});

    window.addEventListener('resize', resizeCanvas);
    document.addEventListener('keydown', handleKeyDown);

    const eraserSlider = document.getElementById('eraser-size-slider');
    eraserSlider.addEventListener('input', function(){
        eraserSize = eraserSlider.value;
    });
});


//창 크기 변경 될 때 캔버스 사이즈 동기화
function resizeCanvas() {
    const canvas = document.getElementById('drawing-canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

//슬라이더 띄우기
function showEraserSlider() {
    const eraserControls = document.getElementById('eraser-controls');
    if (eraserControls.classList.contains('slider-hide')) {
        const eraserSlider = document.getElementById('eraser-size-slider');
        eraserSize = eraserSlider.value; // 현재 슬라이더 값으로 크기 설정
        eraserControls.classList.remove('slider-hide');
        eraserControls.classList.add('slider-show');
    } else {
        eraserControls.classList.remove('slider-show');
        eraserControls.classList.add('slider-hide');
    }
}


function saveEraserSize() {
    const eraserControls = document.getElementById('eraser-controls');
    eraserControls.classList.remove('slider-show');
    eraserControls.classList.add('slider-hide');
    const eraserSlider = document.getElementById('eraser-size-slider');
    eraserSize = eraserSlider.value; // 확인 버튼을 누를 때마다 현재 슬라이더 값으로 크기 설정

    const style = document.createElement('style');
    style.textContent = `
        #drawing-canvas {
            cursor: url(${eraserCursorUrl}) 0 33, auto;
        }
    `;
    document.head.appendChild(style);

    eraser(); //설정된 값으로 eraser() 호출
}


function penTools() {
    var pen1 = document.querySelector('.pen1-floating-btn');
    var pen2 = document.querySelector('.pen2-floating-btn');
    var eraser = document.querySelector('.eraser-btn');
    var eraserAll = document.querySelector('.eraserAll-btn');
    //버튼이 이미 보이는 경우 showP 제거, hide로 숨기기
    //300은 setTimeout() 사용해 300ms 뒤 사라지고, 보임
    if (pen1.classList.contains('showP')) {
        pen1.classList.remove('showP');
        pen1.classList.add('hide');
        pen2.classList.remove('showP');
        pen2.classList.add('hide');
        eraser.classList.remove('showP');
        eraser.classList.add('hide');
        eraserAll.classList.remove('showP');
        eraserAll.classList.add('hide');

        setTimeout(() => {
            pen1.style.display = 'none';
            pen2.style.display = 'none';
            eraser.style.display = 'none';
            eraserAll.style.display = 'none';
        }, 300);
    } else {
        //버튼이 숨겨진 경우 flex로 보이게
        pen1.style.display = 'flex';
        pen2.style.display = 'flex';
        eraser.style.display = 'flex';
        eraserAll.style.display = 'flex';

        setTimeout(() => {
            pen1.classList.remove('hide');
            pen1.classList.add('showP');
            pen2.classList.remove('hide');
            pen2.classList.add('showP');
            eraser.classList.remove('hide');
            eraser.classList.add('showP');
            eraserAll.classList.remove('hide');
            eraserAll.classList.add('showP');
        }, 10);

        alert("그리기를 종료하려면 ESC를 눌러주세요!");
    }
}

//팔레트 위치와 숨기기, 보이기
function pallett(targetButton) {
    const palette = document.getElementById('color-palette');
    const btnRect = targetButton.getBoundingClientRect();
    const paletteWidth = palette.offsetWidth;
    const leftPos = btnRect.left - paletteWidth - 10;
    const topPost = btnRect.top - 20;
    palette.style.top = btnRect.top + 'px';
    palette.style.left = leftPos + 'px';
    palette.classList.toggle('hidden');
}

//html의 colorPicker 변수는 색 선택 요소를 가져와 저장
function selectColor() {
    const colorPicker = document.getElementById('color-picker');
    selectedColor = colorPicker.value; //선택한 색을 selectedColor 변수에 할당
    document.getElementById('color-palette').classList.add('hidden'); //색 선택 하면 팔레트 숨기기
    document.getElementById('drawing-canvas').style.pointerEvents = 'auto'; //캔버스 열기
}

function pencil() {
    const style = document.createElement('style');
    style.textContent = `
        #drawing-canvas {
            cursor: url(${pencilCursorUrl}) 0 33, auto;
        }
    `;
    document.head.appendChild(style);
    activeTool = 'pencil';
    ctx.lineWidth = 1;  //연필 굵기
    ctx.globalAlpha = 1; //투명도 적용 x
    ctx.globalCompositeOperation = 'source-over'; //기존에 연필 자국이 있으면 그 위에
    pallett(document.querySelector('.pen1-floating-btn'));
}

function markerPen() {
    const style = document.createElement('style');
    style.textContent = `
        #drawing-canvas {
            cursor: url(${markerCursorUrl}) 0 33, auto; 
        }
    `;
    document.head.appendChild(style);
    activeTool = 'marker';
    ctx.lineWidth = 8; //형광펜 굵기
    ctx.globalAlpha = markerPenT; //투명도 조절
    ctx.globalCompositeOperation = 'source-over';
    pallett(document.querySelector('.pen2-floating-btn'));
}

function eraser(){
    activeTool = 'eraser';
    ctx.lineWidth = eraserSize;
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'destination-out'; //기존에 있던 펜 자국 위에 새로운 그림 덮어씌우기
}

//캔버스 전체 지우기
function eraserAll(){
    const style = document.createElement('style');
    style.textContent = `
        #drawing-canvas {
            cursor: auto;
        }
    `;
    document.head.appendChild(style);
    const canvas = document.getElementById('drawing-canvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx.clearRect(0,0, window.width, window.height);

    stopDrawingMode();
}

function startDrawing(event) {
    if (activeTool !== '') { //그리기 도구가 활성화 될때만 실행
        event.preventDefault();
        drawing = true;
        ctx.beginPath(); //새 그림 만들기
        const { clientX, clientY } = event.touches ? event.touches[0] : event;
        ctx.moveTo(clientX, clientY); //시작점 설정
    }
}

function stopDrawing() {
    event.preventDefault();
    if (drawing) {
        drawing = false;
        ctx.closePath();
    }
}

function draw(event) {
    if (drawing) {
        event.preventDefault();
        ctx.strokeStyle = selectedColor;
        const { clientX, clientY } = event.touches ? event.touches[0] : event;
        ctx.lineTo(clientX, clientY);
        ctx.stroke();
    }
}

//그리기 종료
function stopDrawingMode() {
    activeTool = '';
    document.getElementById('drawing-canvas').style.pointerEvents = 'none';
    //ctx.globalCompositeOperation = 'source-over';
}

//그리기 종료키 esc
function handleKeyDown(event) {
    if (event.key === 'Escape') {
        stopDrawingMode();
    }
}