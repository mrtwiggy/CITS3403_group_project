document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const viewSelect = document.getElementById('view-select');
    const reviewsContainer = document.getElementById('reviews-container');
    const searchInput = document.getElementById('review-search');
    const franchiseSelect = document.getElementById('franchise-select');
    const locationSelect = document.getElementById('location-select');
    const ratingSelect = document.getElementById('rating-select');
    const sortSelect = document.getElementById('sort-select');
    const loadMoreButton = document.getElementById('load-more-button');
    const loadMoreContainer = document.getElementById('load-more-container');
    
    // Make sure the load more container is visible
    loadMoreContainer.style.display = 'block';
    
    // Initialize variables
    let allReviews = [];
    let filteredReviews = [];
    let currentPage = 1;
    const reviewsPerPage = 5;

    // Function to format date
    function formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        // Less than 1 hour
        if (diff < 3600000) {
            const minutes = Math.floor(diff / 60000);
            return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
        }
        // Less than 1 day
        if (diff < 86400000) {
            const hours = Math.floor(diff / 3600000);
            return `${hours} hour${hours !== 1 ? 's' : ''} ago`;
        }
        // Less than 7 days
        if (diff < 604800000) {
            const days = Math.floor(diff / 86400000);
            return `${days} day${days !== 1 ? 's' : ''} ago`;
        }
        // Otherwise show full date
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    // Function to render boba rating
    function renderRating(rating) {
        return '🟤'.repeat(rating);
    }

    // Function to render a single review
    function renderReview(review) {
        const locationText = review.location && review.location.name 
            ? `${review.franchise.name} • ${review.location.name}`
            : review.franchise.name;
        
        // Determine if the review is by the current user for highlighting
        const isCurrentUserReview = review.is_current_user; // Directly use the flag from the API
        const cardClasses = [
            'bg-white', 'p-6', 'rounded-lg', 'shadow-md', 'review-card',
            review.is_private ? 'border-l-4 border-blue-400' : '', // Existing private highlight, changed to blue for distinction
            isCurrentUserReview ? 'bg-pink-50' : '' // Light pink for current user's review
        ].filter(Boolean).join(' '); // filter(Boolean) removes empty strings from is_private or is_current_user if false

        return `
            <div class="${cardClasses}" data-franchise="${review.franchise.name}" data-rating="${review.rating}">
                <div class="flex justify-between items-start mb-4">
                    <div class="flex items-center space-x-3">
                        <img src="/static/profile_pics/${review.user.profile_pic}"
                             alt="${review.user.username}"
                             class="w-10 h-10 rounded-full">
                        <div>
                            <h3 class="text-xl font-semibold flex items-center">
                                ${review.drink_name}
                                ${review.is_private ? '<span class="ml-2 text-sm text-pink-600">👥 Friends Only</span>' : ''}
                            </h3>
                            <p class="text-gray-600">${locationText}</p>
                        </div>
                    </div>
                    <div class="text-3xl">${renderRating(review.rating)}</div>
                </div>
                <div class="mb-4">
                    <div class="text-gray-700">${review.review_content}</div>
                    <div class="mt-2 text-sm text-gray-500">
                        ${review.drink_size} • 
                        Sugar: ${review.sugar_level} • 
                        Ice: ${review.ice_level}
                    </div>
                </div>
                <div class="flex justify-between items-center text-sm text-gray-500">
                    <span>Posted by ${review.user.username} • ${formatDate(review.uploaded_at)}</span>
                </div>
            </div>
        `;
    }

    // Function to apply filters
    function applyFilters() {
        const searchText = searchInput.value.toLowerCase();
        const selectedFranchise = franchiseSelect.value;
        const selectedRating = parseInt(ratingSelect.value) || 0;
        const sortBy = sortSelect.value;
        
        filteredReviews = allReviews.filter(review => {
            const matchesSearch = review.review_content.toLowerCase().includes(searchText) ||
                                review.drink_name.toLowerCase().includes(searchText) ||
                                review.user.username.toLowerCase().includes(searchText);
            const matchesFranchise = !selectedFranchise || review.franchise.name === selectedFranchise;
            const matchesRating = !selectedRating || review.rating >= selectedRating;
            
            return matchesSearch && matchesFranchise && matchesRating;
        });
        
        // Sort reviews
        if (sortBy === 'rating') {
            filteredReviews.sort((a, b) => b.rating - a.rating);
        } else {
            filteredReviews.sort((a, b) => new Date(b.uploaded_at) - new Date(a.uploaded_at));
        }
        
        // Reset pagination
        currentPage = 1;
        
        // Render first page of filtered reviews
        renderReviews();
    }

    // Function to render reviews with pagination
    function renderReviews() {
        const startIndex = 0;
        const endIndex = currentPage * reviewsPerPage;
        const reviewsToShow = filteredReviews.slice(startIndex, endIndex);
        
        if (reviewsToShow.length > 0) {
            reviewsContainer.innerHTML = reviewsToShow.map(renderReview).join('');
        } else {
            reviewsContainer.innerHTML = '<div class="text-center py-8 text-gray-500">No reviews found matching your filters.</div>';
        }
    }

    // Function to load more reviews
    function loadMoreReviews() {
        // Show loading state
        loadMoreButton.textContent = 'Loading...';
        loadMoreButton.disabled = true;
        
        // Increment page
        currentPage++;
        
        // Convert the view selection to the correct API parameter
        const showFriends = viewSelect.value === 'friends';
        
        // Fetch more reviews
        const url = `/api/get_reviews?page=${currentPage}&per_page=${reviewsPerPage}&friends=${showFriends}`;
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to load more reviews`);
                }
                return response.json();
            })
            .then(newReviews => {
                if (newReviews.length > 0) {
                    // Process each new review
                    newReviews.forEach(review => {
                        // Create the review element
                        const reviewElement = document.createElement('div');
                        
                        // Determine classes for highlighting
                        const isCurrentUserReview = review.is_current_user;
                        const cardDynamicClasses = [
                            'bg-white', 'p-6', 'rounded-lg', 'shadow-md', 'review-card',
                            review.is_private ? 'border-l-4 border-blue-400' : '',
                            isCurrentUserReview ? 'bg-pink-50' : ''
                        ].filter(Boolean).join(' ');
                        reviewElement.className = cardDynamicClasses;

                        if (review.is_private) {
                            // This specific border styling is now handled by cardDynamicClasses
                            // reviewElement.classList.add('border-l-4', 'border-pink-400'); 
                        }
                        reviewElement.setAttribute('data-franchise', review.franchise.name);
                        reviewElement.setAttribute('data-rating', review.rating);
                        
                        const locationText = review.location && review.location.name 
                            ? `${review.franchise.name} • ${review.location.name}`
                            : review.franchise.name;
                            
                        const formattedDate = formatDate(review.uploaded_at);
                        const bobaRating = renderRating(review.rating);
                        
                        // Build HTML content
                        reviewElement.innerHTML = `
                            <div class="flex justify-between items-start mb-4">
                                <div class="flex items-center space-x-3">
                                    <img src="/static/profile_pics/${review.user.profile_pic}"
                                         alt="${review.user.username}"
                                         class="w-10 h-10 rounded-full">
                                    <div>
                                        <h3 class="text-xl font-semibold flex items-center">
                                            ${review.drink_name}
                                            ${review.is_private ? '<span class="ml-2 text-sm text-pink-600">👥 Friends Only</span>' : ''}
                                        </h3>
                                        <p class="text-gray-600">${locationText}</p>
                                    </div>
                                </div>
                                <div class="text-3xl">${bobaRating}</div>
                            </div>
                            <div class="mb-4">
                                <div class="text-gray-700">${review.review_content}</div>
                                <div class="mt-2 text-sm text-gray-500">
                                    ${review.drink_size} • 
                                    Sugar: ${review.sugar_level} • 
                                    Ice: ${review.ice_level}
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-sm text-gray-500">
                                <span>Posted by ${review.user.username} • ${formattedDate}</span>
                            </div>
                        `;
                        
                        // Add to container
                        reviewsContainer.appendChild(reviewElement);
                    });
                    
                    // Add the new reviews to our collection for filtering
                    allReviews = allReviews.concat(newReviews);
                    
                    // UPDATED Load More Button visibility logic
                    if (newReviews.length < reviewsPerPage) {
                        loadMoreContainer.style.display = 'none';
                    } else {
                        loadMoreContainer.style.display = 'block'; // Show if a full page was fetched
                    }
                } else {
                    // No more reviews to load
                    loadMoreContainer.style.display = 'none';
                }
                
                // Reset button state
                loadMoreButton.textContent = 'Load More Reviews';
                loadMoreButton.disabled = false;
            })
            .catch(error => {
                loadMoreButton.textContent = 'Error loading reviews';
                setTimeout(() => {
                    loadMoreButton.textContent = 'Load More Reviews';
                    loadMoreButton.disabled = false;
                }, 2000);
            });
    }

    // Function to load reviews
    async function loadReviews() {
        reviewsContainer.innerHTML = '<div class="text-center py-8 text-gray-500">Loading reviews...</div>';
        loadMoreContainer.style.display = 'none'; // Initially hide while loading
        
        // Update the UI to show which view is active
        const viewType = viewSelect.value;
        document.querySelectorAll('.view-indicator').forEach(el => el.remove());
        
        // Disable the dropdown while loading
        viewSelect.disabled = true;
        viewSelect.classList.add('opacity-50');
        
        try {
            // Convert the view selection to the correct API parameter
            const showFriends = viewSelect.value === 'friends';
            const response = await fetch(`/api/get_reviews?page=1&per_page=${reviewsPerPage}&friends=${showFriends}`);
            if (!response.ok) throw new Error('Failed to load reviews');
            
            allReviews = await response.json();
            currentPage = 1;
            
            applyFilters(); // This calls renderReviews which now does not affect the button
            
            // UPDATED Load More Button visibility logic for initial load
            if (allReviews.length === reviewsPerPage) {
                loadMoreContainer.style.display = 'block';
            } else {
                loadMoreContainer.style.display = 'none';
            }
        } catch (error) {
            reviewsContainer.innerHTML = '<div class="text-center py-8 text-red-500">Failed to load reviews. Please try again.</div>';
            loadMoreContainer.style.display = 'none';
        } finally {
            // Re-enable the dropdown
            viewSelect.disabled = false;
            viewSelect.classList.remove('opacity-50');
        }
    }

    // Event listeners
    viewSelect.addEventListener('change', loadReviews);
    searchInput.addEventListener('input', applyFilters);
    franchiseSelect.addEventListener('change', applyFilters);
    ratingSelect.addEventListener('change', applyFilters);
    sortSelect.addEventListener('change', applyFilters);
    
    // Make sure the load more button has a single event listener
    if (loadMoreButton) {
        // Remove any existing event listeners first (just in case)
        loadMoreButton.replaceWith(loadMoreButton.cloneNode(true));
        
        // Get the fresh reference
        const freshLoadMoreButton = document.getElementById('load-more-button');
        
        // Add the event listener
        freshLoadMoreButton.addEventListener('click', function(event) {
            event.preventDefault();
            loadMoreReviews();
        });
    }

    // Initialize the view
    loadReviews();
}); 