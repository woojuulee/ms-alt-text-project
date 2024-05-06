// document.addEventListener('DOMContentLoaded', function () {
// var submit = document.getElementById('submitButton');
// if (submit) {
//     submit.onclick = showImage; // Submit 버튼 클릭 시 이미지 보여주기
// }
    
// function showImage() {
//     var newImage = document.getElementById('image-show').lastElementChild;
//     newImage.style.visibility = newImage.style.visibility === "hidden" ? "visible" : "hidden";
//     document.getElementById('image-upload').style.visibility = 'visible';
//     var uploadForm = document.getElementById('image-upload');
//     uploadForm.style.visibility = 'visible'; // 이미지 업로드 양식을 숨기지 않음으로 변경
//     document.getElementById('fileName').textContent = null; // 기존 파일 이름 지우기
// }

function loadFile(input) {
    var file = input.files[0];

    var name = document.getElementById('fileName');
    name.textContent = file.name;

    var newImage = document.createElement("img");
    newImage.setAttribute("class", 'img');

    newImage.src = URL.createObjectURL(file);

    newImage.style.width = "50%";
    newImage.style.height = "50%";
    newImage.style.visibility = "visible"; // 버튼을 누르기 전까지는 이미지 숨기기
    newImage.style.objectFit = "contain";
    
    // newImage.style.position = "relative";
    // newImage.style.top = "100px";

    var container = document.getElementById('image-show');
    container.appendChild(newImage);

}

// function uploadAndShowImage() {
//     var filesInput = document.getElementById('chooseFile');
//     var files = filesInput.files;

//     // 서버로 파일 업로드 수행 (여기에서는 단순히 콘솔에 출력)
//     for (var i = 0; i < files.length; i++) {
//         console.log('Uploading file:', files[i].name);
//         // 실제 서버로 업로드하는 코드를 추가해야 합니다.
//     }

//     // 파일 업로드 후 이미지 보여주기
//     showImage();
// }

// function loadFiles(input) {
//     var container = document.getElementById('image-show');

//     // 이미지를 추가하기 전에 이전에 추가된 이미지를 모두 제거
//     while (container.firstChild) {
//         container.removeChild(container.firstChild);
//     }

//     var files = input.files;

//     for (var i = 0; i < files.length; i++) {
//         var file = files[i];

//         var name = document.getElementById('fileName');
//         name.textContent = file.name;
        
//         var newImage = document.createElement("img");
//         newImage.setAttribute("class", 'img');

//         newImage.src = URL.createObjectURL(file);

//         newImage.style.width = "50%";
//         newImage.style.height = "50%";
//         newImage.style.objectFit = "contain";
        
//         container.appendChild(newImage);
//     }
    
//     // 이미지를 추가한 후에 이미지를 보이도록 설정
//     container.style.visibility = "visible";
// }