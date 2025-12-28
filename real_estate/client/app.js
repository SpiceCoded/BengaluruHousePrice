// app.js
function getBathValue() {
  const bath = document.getElementsByName("uiBathrooms");
  for (let i = 0; i < bath.length; i++) {
    if (bath[i].checked) return parseInt(bath[i].value);
  }
  return 2; // default
}

function getBHKValue() {
  const bhk = document.getElementsByName("uiBHK");
  for (let i = 0; i < bhk.length; i++) {
    if (bhk[i].checked) return parseInt(bhk[i].value);
  }
  return 2;
}

function getBalconyValue() {
    const bal = document.getElementsByName("uiBalcony");
    for (let b of bal) if (b.checked) return parseInt(b.value);
    return 1;
}

function getReadyValue() {
  return document.getElementById("radio-ready-yes").checked;
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");

  const sqft = document.getElementById("uiSqft").value;
  const bhk = getBHKValue();
  const bath = getBathValue();
  const balcony = getBalconyValue();
  const location = document.getElementById("uiLocations").value;
  const areaType = document.getElementById("uiAreaType").value;
  const isReady = getReadyValue();

  const estPrice = document.getElementById("uiEstimatedPrice");

  const url = "http://127.0.0.1:8000/estimate";  // FastAPI endpoint

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      area_type: areaType,
      total_sqft: parseFloat(sqft),
      bath: bath,
      balcony: balcony,
      bhk: bhk,
      is_ready: isReady,
      location: location
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.estimated_price) {
      estPrice.innerHTML = "<h2>" + data.estimated_price + " Lakh</h2>";
    } else {
      estPrice.innerHTML = "<h2>Error: " + (data.error || "Unknown") + "</h2>";
    }
    console.log(data);
  })
  .catch(err => {
    console.error(err);
    estPrice.innerHTML = "<h2>Server Error</h2>";
  });
}

function onPageLoad() {
  console.log("Document loaded");
  const url = "http://127.0.0.1:8000/locations";

  fetch(url)
    .then(res => res.json())
    .then(data => {
      if (data.locations) {
        const uiLocations = document.getElementById("uiLocations");
        uiLocations.innerHTML = '<option value="" disabled selected>Choose a Location</option>';
        data.locations.forEach(loc => {
          const opt = new Option(loc);
          uiLocations.appendChild(opt);
        });
      }
    })
    .catch(err => console.error("Failed to load locations", err));
}

window.onload = onPageLoad;