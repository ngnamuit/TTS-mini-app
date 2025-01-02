document.getElementById('fetch-content').addEventListener('click', async function() {
    const url = document.getElementById('url').value;
    const selectors = document.getElementById('selectors').value;

    if (!url || !selectors) {
        alert('Please enter both URL and CSS selectors.');
        return;
    }

    try {
        const response = await fetch('/fetch-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, selectors }),
        });

        if (!response.ok) {
            throw new Error('Failed to fetch content.');
        }

        const data = await response.json();
        document.getElementById('text').value = data.content;
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while fetching content.');
    }
});
