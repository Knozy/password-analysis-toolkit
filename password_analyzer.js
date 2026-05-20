document.getElementById("generateReport")
.addEventListener("click", async () => {

    const password =
        document.getElementById("passwordInput").value;

    const response = await fetch("/api/generate-report", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            password: password
        })
    });

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "password_report.pdf";

    a.click();
});
