async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const output = document.getElementById("summaryOutput");

    if (!fileInput.files.length) {
        alert("Please upload a document");
        return;
    }

    output.value = "⏳ Processing legal document...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:8000/summarize", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        output.value = data.summary || "❌ No summary returned";

    } catch (err) {
        output.value = "❌ Failed to fetch summary. Check backend.";
        console.error(err);
    }
}

function copySummary() {
    navigator.clipboard.writeText(
        document.getElementById("summaryOutput").value
    );
}
