document.getElementById("convert").addEventListener("click", async () => {
    const button = document.getElementById("convert");
    const text = document.getElementById("text").value;
    const engine = document.getElementById("engine").value;

    if (!text) {
        alert("Please input text!");
        return;
    }

    // Disable the button and show a loading message
    button.disabled = true;
    button.textContent = "Processing ...";

    try {
        console.time("Execution Time"); // Start measuring execution time

        const formData = new FormData();
        formData.append("text", text);
        formData.append("engine", engine);

        const response = await fetch("/text-to-speech/", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const blob = await response.blob();
            const audio = document.getElementById("audio");
            const replay = document.getElementById("replay");
            audio.src = URL.createObjectURL(blob);
            audio.style.display = "block";
            replay.style.display = "revert";
            audio.play();
        } else {
            alert("There's an error, Please check again!");
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

const replayButton = document.getElementById("replay");
if (replayButton) {
    replayButton.addEventListener("click", () => {
        console.log("Replay button clicked!");
        const audio = document.getElementById("audio");
        const speed = document.getElementById("speed").value;
        console.log("Selected speed: ", speed);

        if (audio && audio.src) {

            audio.playbackRate = parseFloat(speed);
            audio.play().then(() => {
                console.log("Audio replayed successfully.");
            }).catch((error) => {
                console.error("Error replaying audio: ", error);
            });
        }
    });
}