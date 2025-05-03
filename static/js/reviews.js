/* to be filled with js for reviews page*/
// Franchise to Location Mapping
const franchiseLocations = {
    "Boba Boba": [
      "Altone Park",
      "Belmont",
      "Cockburn",
      "Kingsway",
      "Morley",
      "Murdoch",
      "Myaree",
      "Nedlands",
      "Northbridge",
      "Piara Waters",
      "Victoria Park",
      "Willeton",
      "Joondalup - Bobabot"
    ],
    "Bon Bon Cha": [
      "Forrest Lakes",
      "Harrisdale",
      "Willeton"
    ],
    "Chaffic": [
      "Baldivis",
      "Belmont",
      "Claremont",
      "Forrest Chase",
      "Karrinyup",
      "Midland",
      "Mirrabooka",
      "Northbridge",
      "Victoria Park",
      "Willetton"
    ],
    "Chatime": [
      "Armadale",
      "Cannington",
      "East Victoria Park",
      "Ellenbrook",
      "Forrestfield",
      "Hillarys",
      "Joondalup",
      "Karawara",
      "Karrinyup",
      "Lakelands",
      "Leederville",
      "Mandurah",
      "Midland",
      "Murdoch",
      "Southern River",
      "Waterford Plaza",
      "Willetton"
    ],
    "Gong Cha": [
      "Cannington",
      "Innaloo",
      "Northbridge",
      "Warwick"
    ],
    "Gotcha Fresh Tea": [
      "Booragoon",
      "Karrinyup"
    ],
    "Mahci Machi": [
      "Carousel",
      "Claremont",
      "East Victoria Park"
    ],
    "Once For All": [
      "Harrisdale",
      "Rockingham"
    ],
    "Milk Flower": [
      "Cannington",
      "Joondalup",
      "Karrinyup",
      "Morley",
      "Northbridge"
    ],
    "Presotea": [
      "Canning Vale",
      "Cannington",
      "Cockburn",
      "East Victoria Park",
      "Ellenbrook",
      "Innaloo",
      "Joondalup",
      "Leederville",
      "Morley",
      "Mount Lawley",
      "Myaree",
      "Nedlands",
      "Northbridge",
      "Perth (Barrack Street)",
      "Perth (Raine Square)",
      "Perth (Newcastle Street)",
      "Success"
    ],
    "T4": [
      "Canning Vale",
      "East Victoria Park",
      "Fremantle",
      "Innaloo",
      "Morley",
      "Myaree",
      "Northbridge"
    ],
    "Teamorrow": [
      "Booragoon",
      "East Victoria Park",
      "Morley",
      "Northbridge"
    ],
    "Utopia": [
      "Cannington",
      "Fremantle",
      "Joondalup",
      "Morley",
      "Myaree",
      "Perth Airport",
      "Riverton",
      "Rockingham",
      "Victoria Park",
      "Wembley",
      "Willetton"
    ]
  };
  
  // Button selection functionality
  function setupToggleGroup(buttons) {
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('ring', 'ring-offset-2', 'ring-pink-400', 'bg-pink-200', 'ring-blue-400', 'bg-blue-200'));
        if (btn.dataset.group === 'sugar') {
          btn.classList.add('ring', 'ring-offset-2', 'ring-pink-400', 'bg-pink-200');
        } else if (btn.dataset.group === 'ice') {
          btn.classList.add('ring', 'ring-offset-2', 'ring-blue-400', 'bg-blue-200');
        }
      });
    });
  }
  
  // Boba rating functionality
  function setupBobaRating() {
    const bobaBalls = document.querySelectorAll('#boba-rating span');
    bobaBalls.forEach(ball => {
      ball.addEventListener('click', () => {
        const index = parseInt(ball.dataset.index);
        bobaBalls.forEach((b, i) => {
          b.textContent = i < index ? '🟤' : '🔘';
        });
      });
    });
  }
  
  // Location dropdown functionality
  function setupLocationDropdown() {
    const franchiseSelect = document.getElementById("franchise-select");
    const locationSelect = document.getElementById("location-select");
  
    franchiseSelect.addEventListener("change", () => {
      const selectedFranchise = franchiseSelect.value;
  
      // Clear and Disable Location Dropdown if No Franchise Selected
      locationSelect.innerHTML = '<option value="">Select Location</option>';
      locationSelect.disabled = !selectedFranchise;
  
      // Populate Location Dropdown if Franchise Selected
      if (selectedFranchise) {
        const locations = franchiseLocations[selectedFranchise];
        locations.forEach(location => {
          const option = document.createElement("option");
          option.value = location;
          option.textContent = location;
          locationSelect.appendChild(option);
        });
      }
    });
  }
  
  // Initialize all functionality when DOM is loaded
  document.addEventListener('DOMContentLoaded', () => {
    const sugarButtons = document.querySelectorAll('[data-group="sugar"]');
    const iceButtons = document.querySelectorAll('[data-group="ice"]');
    setupToggleGroup(sugarButtons);
    setupToggleGroup(iceButtons);
    setupBobaRating();
    setupLocationDropdown();
  }); 