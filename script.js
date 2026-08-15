// ============================================
// VOICE SCAM SHIELD - FRONTEND
// ============================================


// Change between application screens
function showScreen(screenId) {

    const screens = document.querySelectorAll(".screen");

    screens.forEach(screen => {
        screen.classList.remove("active");
    });

    const selectedScreen = document.getElementById(screenId);

    if (selectedScreen) {
        selectedScreen.classList.add("active");

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
}


// Start protection
async function startMonitoring() {

    showScreen("monitoring");

    console.log("Protection enabled");

    const demoTranscript =
        "Your bank account will be blocked. Please share your OTP immediately.";

    const result = await analyzeCall(demoTranscript);

    if (result) {
        console.log("Backend connected successfully!");
        console.log("Risk Score:", result.risk_score);
        console.log("Risk Level:", result.risk_level);

        alert(
            "Backend Connected!\n\n" +
            "Risk Level: " + result.risk_level + "\n" +
            "Risk Score: " + result.risk_score
        );
    } else {
        alert("Backend connection failed.");
    }
}




// Demo notification
function showDemoMessage() {

    alert("Voice Scam Shield is protecting your calls.");

}


// Future backend connection 
async function analyzeCall(transcript) {

    try {

        const response = await fetch("/api/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                transcript: transcript
            })

        });


        if (!response.ok) {
            throw new Error("Backend connection failed");
        }


        const result = await response.json();

        console.log("AI Analysis Result:", result);

        return result;

    }

    catch (error) {

        console.error("Analysis Error:", error);

        return null;

    }

}