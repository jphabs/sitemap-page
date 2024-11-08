document.getElementById("sitemap-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const url = document.getElementById("url").value;
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Generating sitemap for " + url + "...";

    try {
        const response = await fetch('/generate-sitemap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (response.ok) {
            resultDiv.innerHTML = "Sitemap generation started for: " + url;
        } else {
            resultDiv.innerHTML = "Error: " + (data.error || "Something went wrong.");
        }
    } catch (error) {
        resultDiv.innerHTML = "Error: " + error.message;
    }
});