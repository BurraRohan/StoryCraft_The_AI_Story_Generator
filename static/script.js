function generateStory() {
    const prompt = document.getElementById("prompt").value.trim();
    const genre = document.getElementById("genre").value;
    const storyOutput = document.getElementById("story-output");

    if (!prompt) {
        alert("Please enter a story prompt.");
        return;
    }

    storyOutput.innerHTML = "<p>⏳ Generating story...</p>";

    fetch("/generate", {  // Relative API path
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ prompt, genre })
    })
    .then(response => response.json())
    .then(data => {
        if (data.story) {
            storyOutput.innerHTML = `<p>${data.story}</p>`;
        } else {
            storyOutput.innerHTML = "<p>⚠️ Failed to generate a story. Please try again.</p>";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        storyOutput.innerHTML = "<p>❌ An error occurred while generating the story.</p>";
    });
}

function resetFields() {
    document.getElementById("prompt").value = "";  // Clear text area
    document.getElementById("genre").selectedIndex = 0;  // Reset dropdown
    document.getElementById("story-output").innerHTML = "";  // Clear story output
}
