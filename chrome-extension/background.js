chrome.tabs.onActivated.addListener(async (activeInfo) => {
    try {
        const tab = await chrome.tabs.get(activeInfo.tabId);

        if (tab.url) {
            sendToBackend(tab.url);
        }
    } catch (error) {
        console.error("Error getting tab info:", error);
    }
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        sendToBackend(tab.url);
    }
});

async function sendToBackend(currentUrl) {
    const backendUrl = "http://127.0.0.1:8000/track";

    try {
        const response = await fetch(backendUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({url: currentUrl})
        });
        const data = await response.json();
        console.log("Backend response:", data);
    } catch (error) {
        console.log("Couldn't connect to FastAPI. Is the server running? ");
    }
}