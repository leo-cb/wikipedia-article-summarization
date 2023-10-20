# Define the URL and headers
$url = "http://localhost:8000/summarize/?url=https://en.wikipedia.org/wiki/Python_(programming_language)&limit=1000"
$headers = @{"api-key-header" = "abc"}

# Send the GET request
$response = Invoke-RestMethod -Uri $url -Headers $headers

# Print the response
$response