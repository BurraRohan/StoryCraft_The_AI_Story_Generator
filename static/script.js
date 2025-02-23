let lastPrompt = "";
let lastGenre = "";

function generateStory() {
    const prompt = document.getElementById("prompt").value.trim();
    const genre = document.getElementById("genre").value;
    const storyOutput = document.getElementById("story-output");
    const regenerateBtn = document.getElementById("regenerate-btn");

    if (!prompt) {
        alert("Please enter a story prompt.");
        return;
    }

    // Store the last used prompt and genre for regeneration
    lastPrompt = prompt;
    lastGenre = genre;

    storyOutput.innerHTML = "<p>⏳ Generating story...</p>";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, genre })
    })
    .then(response => response.json())
    .then(data => {
        if (data.story) {
            storyOutput.innerHTML = `<p>${data.story}</p>`;
            regenerateBtn.style.display = "block";  // Show regenerate button
        } else {
            storyOutput.innerHTML = "<p>⚠️ Failed to generate a story. Please try again.</p>";
            regenerateBtn.style.display = "none"; // Hide button if error occurs
        }
    })
    .catch(error => {
        console.error("Error:", error);
        storyOutput.innerHTML = "<p>❌ An error occurred while generating the story.</p>";
        regenerateBtn.style.display = "none";
    });
}

function regenerateStory() {
    if (!lastPrompt || !lastGenre) {
        alert("No story to regenerate. Please generate one first.");
        return;
    }

    const storyOutput = document.getElementById("story-output");
    storyOutput.innerHTML = "<p>🔄 Regenerating story...</p>";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: lastPrompt, genre: lastGenre })
    })
    .then(response => response.json())
    .then(data => {
        if (data.story) {
            storyOutput.innerHTML = `<p>${data.story}</p>`;
        } else {
            storyOutput.innerHTML = "<p>⚠️ Failed to regenerate. Please try again.</p>";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        storyOutput.innerHTML = "<p>❌ An error occurred while regenerating the story.</p>";
    });
}

function resetFields() {
    document.getElementById("prompt").value = "";
    document.getElementById("genre").selectedIndex = 0;
    document.getElementById("story-output").innerHTML = "";
    document.getElementById("regenerate-btn").style.display = "none"; // Hide regenerate button on reset
}
