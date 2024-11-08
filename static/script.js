document.getElementById("sitemap-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const url = document.getElementById("url").value;
    const resultDiv = document.getElementById("result");

    if (!url) {
        resultDiv.innerHTML = "Please enter a URL.";
        return;
    }

    resultDiv.innerHTML = "Generating sitemap for " + url + "...";

    try {
        const response = await fetch('/generate-sitemap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        let data;

        // Check if response has JSON content type
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            throw new Error("Invalid JSON response from server");
        }

        if (response.ok) {
            resultDiv.innerHTML = "Sitemap generation started for: " + url;
        } else {
            resultDiv.innerHTML = "Error: " + (data.error || "Something went wrong.");
        }
    } catch (error) {
        resultDiv.innerHTML = "Error: " + error.message;
    }
});