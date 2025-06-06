
const jobForm = document.getElementById("jobForm");
const outputDiv = document.getElementById("output");

jobForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(jobForm);
  const jobUrl = formData.get("jobUrl");
  await fetchData(jobUrl);
});

async function fetchData(jobUrl) {
  outputDiv.innerHTML = '<div class="loading">Analyzing job... Please wait.</div>';

  try {
    const response = await fetch(`http://localhost:8000/analyzer/scrape_site`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({ url: jobUrl })
    });

    if (!response.ok) {
      const errorBody = await response.text();
      let errorMessage = `HTTP error! Status: ${response.status}`;
      try {
        const errorJson = JSON.parse(errorBody);
        if (errorJson.detail) {
          errorMessage += `, Detail: ${errorJson.detail}`;
        } else if (errorJson.error) {
          errorMessage += `, Backend Error: ${errorJson.error}`;
        }
      } catch (e) {
        errorMessage += `, Response: ${errorBody.substring(0, 200)}...`;
      }
      throw new Error(errorMessage);
    }

    const data = await response.json();
    displayResult(data);

  } catch (error) {
    outputDiv.innerHTML = `<div class="error">
      <h2>Analysis Failed!</h2>
      <ul>
        <li>Backend not running?</li>
        <li>URL is wrong?</li>
        <li>Network issue?</li>
      </ul>
      <p><strong>Error:</strong> ${error.message}</p>
    </div>`;
  }
}

function displayResult(data) {
  let htmlContent = '<div class="result">';
  if (data.error) {
    htmlContent += `<h2>Analysis Error!</h2>
                    <p><strong>Error:</strong> ${data.error}</p>`;
  } else {
    htmlContent += `<h2>Analysis Result</h2>
                    <p><strong>Scam Verdict:</strong> ${data.Scam_Verdict}</p>
                    <p><strong>Trust Score:</strong> ${data.Trust_Score}/100</p>
                    <h3>Reasoning:</h3><ul>`;
    if (Array.isArray(data.Reasoning)) {
      data.Reasoning.forEach(reason => {
        htmlContent += `<li>${reason}</li>`;
      });
    }
    htmlContent += '</ul>';
  }
  htmlContent += '</div>';
  outputDiv.innerHTML = htmlContent;
}
