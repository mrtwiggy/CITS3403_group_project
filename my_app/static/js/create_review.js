document.addEventListener('DOMContentLoaded', function() {
    const franchiseSelect = document.getElementById('franchise-select');
    const locationSelect = document.getElementById('location-select');
    
    franchiseSelect.addEventListener('change', function() {
        const franchiseId = this.value;
        
        // Clear current options
        locationSelect.innerHTML = '<option value="0">Select Location</option>';
        
        // Don't fetch if "Select Franchise" is chosen (value 0)
        if (franchiseId == 0) {
            return;
        }
        
        // Fetch locations for selected franchise
        fetch(`/review/api/franchise/${franchiseId}/locations`)
            .then(response => response.json())
            .then(locations => {
                // Add locations to dropdown
                locations.forEach(location => {
                    const option = document.createElement('option');
                    option.value = location.id;
                    option.textContent = location.name;
                    locationSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching locations:', error));
    });
    
    // Handle sugar level buttons
    const sugarLevelHidden = document.getElementById('sugar-level-hidden');
    document.querySelectorAll('.sugar-buttons button').forEach(button => {
      button.addEventListener('click', function() {
        // Clear active class from all buttons in group
        document.querySelectorAll('.sugar-buttons button').forEach(btn => {
          btn.classList.remove('bg-pink-300');
          btn.classList.add('bg-pink-100');
        });
        
        // Set active class on clicked button
        this.classList.remove('bg-pink-100');
        this.classList.add('bg-pink-300');
        
        // Update hidden field
        sugarLevelHidden.value = this.dataset.value;
      });
    });
    
    // Handle ice level buttons
    const iceLevelHidden = document.getElementById('ice-level-hidden');
    document.querySelectorAll('.ice-buttons button').forEach(button => {
      button.addEventListener('click', function() {
        // Clear active class from all buttons in group
        document.querySelectorAll('.ice-buttons button').forEach(btn => {
          btn.classList.remove('bg-blue-300');
          btn.classList.add('bg-blue-100');
        });
        
        // Set active class on clicked button
        this.classList.remove('bg-blue-100');
        this.classList.add('bg-blue-300');
        
        // Update hidden field
        iceLevelHidden.value = this.dataset.value;
      });
    });
    
    // Handle rating selection
    const ratingHidden = document.getElementById('rating-hidden');
    const bobaRating = document.getElementById('boba-rating');
    const ratingSymbols = {
      inactive: '🔘',
      active: '🟤'
    };

    // Handle privacy selection
    const privacyHidden = document.getElementById('privacy-hidden');
    const privacySelect = document.getElementById('privacy-select');
    
    // Set default to Public (0) if not already set
    if (!privacyHidden.value) {
      privacyHidden.value = '0';
      privacySelect.value = '0';
    } else {
      privacySelect.value = privacyHidden.value;
    }
    
    // Update hidden field when dropdown changes
    privacySelect.addEventListener('change', function() {
      privacyHidden.value = this.value;
    });
    
    bobaRating.querySelectorAll('span').forEach(star => {
      star.addEventListener('click', function() {
        const rating = parseInt(this.dataset.index);
        ratingHidden.value = rating;
        
        // Update visual display
        bobaRating.querySelectorAll('span').forEach(s => {
          const starIndex = parseInt(s.dataset.index);
          s.textContent = starIndex <= rating ? ratingSymbols.active : ratingSymbols.inactive;
        });
      });
      
      // Add hover effect
      star.addEventListener('mouseover', function() {
        const hoveredIndex = parseInt(this.dataset.index);
        bobaRating.querySelectorAll('span').forEach(s => {
          const starIndex = parseInt(s.dataset.index);
          if (starIndex <= hoveredIndex) {
            s.textContent = ratingSymbols.active;
          } else {
            s.textContent = ratingSymbols.inactive;
          }
        });
      });
    });
    
    // Reset stars on mouse out if no rating selected
    bobaRating.addEventListener('mouseout', function() {
      const currentRating = parseInt(ratingHidden.value) || 0;
      bobaRating.querySelectorAll('span').forEach(s => {
        const starIndex = parseInt(s.dataset.index);
        s.textContent = starIndex <= currentRating ? ratingSymbols.active : ratingSymbols.inactive;
      });
    });
  }); 