document.getElementById('scrapeForm').addEventListener('submit', function(event) {
    const linkedinUrl = document.getElementById('linkedin_url').value;
    const linkedinRegex = /^https:\/\/[a-z]{2,3}\.linkedin\.com\/.*$/;

    if (!linkedinRegex.test(linkedinUrl)) {
        event.preventDefault();
        document.getElementById('message').textContent = 'Invalid LinkedIn URL format.';
    }
});
