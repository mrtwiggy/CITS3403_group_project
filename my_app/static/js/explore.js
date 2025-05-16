document.addEventListener('DOMContentLoaded', function() {
    const userSearch = document.getElementById('user-search');
    const searchResults = document.getElementById('search-results');
    const leaderboardView = document.getElementById('leaderboard-view');
    let searchTimeout;

    // User Search
    userSearch.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.innerHTML = '';
            return;
        }

        searchTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/api/search_users?q=${encodeURIComponent(query)}`);
                const users = await response.json();
                
                searchResults.innerHTML = users.map(user => `
                    <div class="flex items-center justify-between p-2 hover:bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <img src="/static/profile_pics/${user.profile_pic}" 
                                 alt="${user.username}" 
                                 class="w-8 h-8 rounded-full mr-2">
                            <span class="text-sm">@${user.username}</span>
                        </div>
                        ${getFriendshipButton(user)}
                    </div>
                `).join('');

                // Add click handlers for friendship buttons
                document.querySelectorAll('.friendship-btn').forEach(btn => {
                    btn.addEventListener('click', handleFriendshipAction);
                });
            } catch (error) {
                console.error('Error searching users:', error);
            }
        }, 300);
    });

    // Friendship button helper
    function getFriendshipButton(user) {
        switch(user.friendship_status) {
            case 'accepted':
                return `<span class="text-sm text-green-600">Friends</span>`;
            case 'pending':
                return `<span class="text-sm text-gray-600">Requested</span>`;
            default:
                return `
                    <button class="friendship-btn bg-pink-100 text-pink-600 px-3 py-1 rounded text-sm hover:bg-pink-200"
                            data-user-id="${user.id}">
                        Add Friend
                    </button>
                `;
        }
    }

    // Load and display trending data
    async function loadTrendingData() {
        try {
            const response = await fetch('/api/trending_reviews');
            const data = await response.json();
            
            // Update recent reviews
            document.getElementById('recent-reviews').innerHTML = data.recent_reviews.map(review => `
                <div class="border-b pb-3 last:border-0 last:pb-0">
                    <div class="flex items-center mb-2">
                        <span class="font-medium">@${review.username}</span>
                        <span class="mx-2">·</span>
                        <span class="text-sm text-gray-500">${formatDate(review.uploaded_at)}</span>
                    </div>
                    <p class="text-sm text-gray-600">${review.drink_name} from ${review.franchise_name || 'Unknown'}</p>
                </div>
            `).join('');

            // Update active users
            document.getElementById('active-users').innerHTML = data.active_users.map(user => `
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <img src="/static/profile_pics/${user.profile_pic}" 
                             alt="${user.username}" 
                             class="w-8 h-8 rounded-full mr-2">
                        <span class="text-sm">@${user.username}</span>
                    </div>
                    <span class="text-sm text-gray-500">${user.review_count} reviews</span>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading trending data:', error);
        }
    }

    // Load and display leaderboard
    async function loadLeaderboard() {
        try {
            const view = leaderboardView.value;
            const response = await fetch(`/api/leaderboard?view=${view}`);
            const data = await response.json();
            
            document.getElementById('leaderboard-content').innerHTML = data.map(entry => `
                <div class="grid grid-cols-12 gap-4 items-center p-2 rounded-lg ${entry.is_current_user ? 'bg-pink-50 font-medium' : 'hover:bg-gray-50'}">
                    <div class="col-span-1 text-center">${entry.rank}</div>
                    <div class="col-span-3 flex items-center space-x-2 min-w-0">
                        <img src="/static/profile_pics/${entry.profile_pic}" 
                             alt="${entry.username}" 
                             class="w-8 h-8 rounded-full flex-shrink-0">
                        <span class="truncate">@${entry.username}</span>
                    </div>
                    <div class="col-span-5 truncate">${entry.favorite_franchise}</div>
                    <div class="col-span-3 text-center">${entry.total_reviews}</div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading leaderboard:', error);
        }
    }

    // Helper function to format dates
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    }

    document.addEventListener('click', async function (e) {
        if (e.target.classList.contains('friendship-btn')) {
            const button = e.target;
            const userId = button.dataset.userId;

            try {
                const response = await fetch(`/friends/request/${userId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest', // if your server expects it
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
                    }
                });

                if (response.ok) {
                    button.outerHTML = `<span class="text-sm text-gray-600">Requested</span>`;
                } else {
                    const error = await response.text();
                    alert('Failed to send request: ' + error);
                }
            } catch (err) {
                console.error(err);
                alert('An error occurred while sending the friend request.');
            }
        }
    });


    // Initial load
    loadTrendingData();
    loadLeaderboard();

    // Update leaderboard when view changes
    leaderboardView.addEventListener('change', loadLeaderboard);

    // Refresh data periodically
    setInterval(loadTrendingData, 60000); // Refresh trending data every minute
    setInterval(loadLeaderboard, 60000); // Refresh leaderboard every minute
}); 