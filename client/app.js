// API base URL
const API_URL = "https://bhk.fly.dev/api";

// Load locations when page loads
window.addEventListener("DOMContentLoaded", () => {
  loadLocations();
  setupFormSubmit();
});

// Fetch and populate location dropdown
async function loadLocations() {
  try {
    const response = await fetch(`${API_URL}/get-location-names`);
    const data = await response.json();

    const locationSelect = document.getElementById("location");
    locationSelect.innerHTML = '<option value="">Select a location</option>';

    data.locations.forEach((location) => {
      const option = document.createElement("option");
      option.value = location;
      option.textContent = location
        .split(" ")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");
      locationSelect.appendChild(option);
    });
  } catch (error) {
    console.error("Error loading locations:", error);
    alert("Failed to load locations. Please make sure the server is running.");
  }
}

// Handle form submission
function setupFormSubmit() {
  const form = document.getElementById("priceForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Get form values
    const formData = new FormData(form);
    const total_sqft = formData.get("total_sqft");
    const bhk = formData.get("bhk");
    const bath = formData.get("bath");
    const location = formData.get("location");

    // Validate inputs
    if (!total_sqft || !bhk || !bath || !location) {
      alert("Please fill in all fields");
      return;
    }

    try {
      // Call API
      const response = await fetch(`${API_URL}/predict-home-price`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          total_sqft: total_sqft,
          bhk: bhk,
          bath: bath,
          location: location,
        }),
      });

      const data = await response.json();

      // Display result
      displayResult(data.estimated_price);
    } catch (error) {
      console.error("Error predicting price:", error);
      alert(
        "Failed to estimate price. Please make sure the server is running."
      );
    }
  });
}

// Display the predicted price
function displayResult(price) {
  const resultDiv = document.getElementById("result");
  const priceValue = document.getElementById("priceValue");

  priceValue.textContent = price;
  resultDiv.classList.remove("hidden");

  // Scroll to result
  resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
}
