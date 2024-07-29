
document.getElementById('btngenerateBlog').addEventListener('click', async () => {
        
    const youtubeLink = document.getElementById('youtubeLink').value;
    const blogContent = document.getElementById('blogContent');
    
    if(youtubeLink) {
        document.getElementById('loading-circle').style.display = 'block';
        document.getElementById('blg-header').style.display = 'none';
        
        blogContent.innerHTML = ''; // Clear previous content

        const endpointUrl = '/generate-blog';
        
        try {
            const response = await fetch(endpointUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ link: youtubeLink })
            });

            const data = await response.json();

            document.getElementById('blg-header').style.display = 'block';
            blogContent.innerHTML = data.content;

        } catch (error) {
            console.error("Error occurred:", error);
            alert("Something went wrong. Please try again later.");
            
        }
        document.getElementById('loading-circle').style.display = 'none';
    } else {
        alert("Please enter a YouTube link.");
    }
});