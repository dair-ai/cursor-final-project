async function convertToMarkdown() {
    const urlInput = document.getElementById('url');
    const convertBtn = document.getElementById('convert-btn');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');

    // Reset state
    error.classList.add('hidden');
    error.textContent = '';

    // Validate URL
    const url = urlInput.value.trim();
    if (!url) {
        error.textContent = 'Please enter a URL';
        error.classList.remove('hidden');
        return;
    }

    try {
        // Show loading state
        loading.classList.remove('hidden');
        convertBtn.disabled = true;

        // Send conversion request
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to convert webpage');
        }

        // Trigger file download
        window.location.href = `/download/${encodeURIComponent(data.file)}`;

    } catch (err) {
        error.textContent = err.message;
        error.classList.remove('hidden');
    } finally {
        // Reset UI state
        loading.classList.add('hidden');
        convertBtn.disabled = false;
    }
} 