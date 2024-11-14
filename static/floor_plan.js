// Assuming the HTML has an input element with id "prompt-input" and a button with id "generate-btn"
// Also, assuming there's an img element with id "generated-image" to display the result

document.getElementById("generate-btn").addEventListener("click", async function () {
  // Get the input value
  const prompt = document.getElementById("prompt-input").value;

  // Ensure a prompt is provided
  if (!prompt) {
      alert("Please enter a description for the floor plan.");
      return;
  }

  try {
      // Send prompt to the backend
      const response = await fetch('/generate-image', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: prompt }),
      });

      // Check if the response is successful
      if (!response.ok) {
          throw new Error('Failed to generate image');
      }

      // Parse the JSON response
      const result = await response.json();

      // Set the image source with the base64 string received
      document.getElementById("generated-image").src = `data:image/png;base64,${result.image}`;
  } catch (error) {
      console.error("Error generating image:", error);
      alert("An error occurred while generating the image. Please try again.");
  }
});
