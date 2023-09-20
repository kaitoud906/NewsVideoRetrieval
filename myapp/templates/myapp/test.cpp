var sample_all = [];
var mapping_keyframe = [];
function createModal(_ob, time, array_frame)
{
    const modal = document.createElement('div');
    modal.classList.add('modal');
    modal.style.display = "block";
    const modalDialog = document.createElement('div');
    modalDialog.classList.add('modal-dialog');
    modalDialog.classList.add('modal-xl');
    const modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');
    const modalHead = document.createElement('div');
    modalHead.classList.add('modal-header');
    const closeButton = document.createElement('button');
    closeButton.classList.add('btn-close');
    closeButton.addEventListener(
        "click", function() { modal.remove(); });
    modalHead.appendChild(closeButton);
    const modalBody = document.createElement('div');
    modalBody.classList.add('modal-body');
    const video = document.createElement('video');
    video.controls = true;
    video.style.width = "100%";video.setAttribute("src",`/media?filepath=${
        encodeURIComponent(`D
                           :\\AI_Challenge\\Data\\video\\${_ob.video}.mp4`)}`);
    video.currentTime = time;
    modalBody.appendChild(video);
    const click_ptr = document.createElement('div');
    click_ptr.classList.add('btn-primary');
    click_ptr.classList.add('btn');
    click_ptr.innerHTML = "Xem frame";
    click_ptr.onclick = function()
    {
        let str = ``;
        let fps = array_frame[6];
        let currentTime = video.currentTime;
        for (let t = Math.round(currentTime - 2); t < currentTime + 2; t++)
        {
            if (t < 0 || t > video.duration)
            {
                continue;
            }
            let min = Math.floor(t / 60);
            let sec = t % 60;
            if (min < 10)
            {
                min = "0" + min;
            }
            if (sec < 10)
            {
                sec = "0" + sec;
            }
            str += `Time : ${Math.round(min)} : ${sec} - frameid ${t * fps}<br />`;
        }
        document.getElementById("my_result").innerHTML = str;
    };
    const result_p = document.createElement('p');
    result_p.setAttribute("id", "my_result");
    modalBody.appendChild(result_p);
    modalBody.appendChild(click_ptr);
    modalContent.appendChild(modalHead);
    modalContent.appendChild(modalBody);
    modalDialog.appendChild(modalContent);
    modal.appendChild(modalDialog);
    document.body.appendChild(modal);
}
function createGetTimeForVideo(_ob)
{fetch(`/media?filepath=${
        encodeURIComponent(`D
                           :\\AI_Challenge\\Data\\map - keyframes\\${_ob.video}.csv`)}`).then(response => response.text()).then(data => {
        let index = 4 * _ob.frameid + 1;
        let array_frame = data.replaceAll("\n", ",").replaceAll("\r", "").split(",");
        createModal(_ob, array_frame[index], array_frame);}).catch(error => console.log(error));
}