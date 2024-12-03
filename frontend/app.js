document.getElementById("convert").addEventListener("click", async () => {
    const button = document.getElementById("convert");
    const text = document.getElementById("text").value;
    const engine = document.getElementById("engine").value;

    if (!text) {
        alert("Vui lòng nhập văn bản!");
        return;
    }

    // Disable the button and show a loading message
    button.disabled = true;
    button.textContent = "Đang xử lý...";

    try {
        console.time("Execution Time"); // Start measuring execution time

        const formData = new FormData();
        formData.append("text", text);
        formData.append("engine", engine);

        const response = await fetch("http://127.0.0.1:8000/text-to-speech/", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const audio = document.getElementById("audio");
            audio.src = URL.createObjectURL(blob);
            audio.style.display = "block";
            audio.play();
        } else {
            alert("Có lỗi xảy ra, vui lòng thử lại!");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Có lỗi xảy ra khi kết nối đến server!");
    } finally {
        // Re-enable the button and reset the text
        button.disabled = false;
        button.textContent = "Chuyển đổi";
        console.timeEnd("Execution Time"); // End measuring execution time
    }

});
