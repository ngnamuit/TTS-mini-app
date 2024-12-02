document.getElementById("convert").addEventListener("click", async () => {
    const text = document.getElementById("text").value;
    const engine = document.getElementById("engine").value;

    if (!text) {
        alert("Vui lòng nhập văn bản!");
        return;
    }

    const formData = new FormData();
    formData.append("text", text);
    formData.append("engine", engine);

    const response = await fetch("http://127.0.0.1:8000/text-to-speech/", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        const audio = document.getElementById("audio");
        audio.src = URL.createObjectURL(await response.blob());
        audio.style.display = "block";
        audio.play();
    } else {
        alert("Có lỗi xảy ra, vui lòng thử lại!");
    }
});
