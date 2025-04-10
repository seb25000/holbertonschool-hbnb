document.addEventListener('DOMContentLoaded', () => {
    // --- Configuration ---
    const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'; // CHANGE TO YOUR API URL

    // --- Utility Functions ---
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    function deleteCookie(name) {
        document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }

    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    function displayMessage(elementId, message, isError = false) {
        const element = document.getElementById(elementId);
        if (element) {
            element.textContent = message;
            element.classList.remove('hidden');
            element.style.color = isError ? 'red' : 'green';
        }
    }

    function hideMessage(elementId) {
         const element = document.getElementById(elementId);
         if (element) {
             element.classList.add('hidden');
         }
    }

    function updateAuthUI(token) {
        const loginLink = document.getElementById('login-link');
        const logoutButton = document.getElementById('logout-button');

        if (token) {
            if (loginLink) loginLink.classList.add('hidden');
            if (logoutButton) logoutButton.classList.remove('hidden');
        } else {
            if (loginLink) loginLink.classList.remove('hidden');
            if (logoutButton) logoutButton.classList.add('hidden');
        }
    }

    function handleLogout() {
        deleteCookie('token');
        updateAuthUI(null);
        // Redirect to login or home page after logout if desired
        if (!window.location.pathname.endsWith('login.html')) {
             window.location.href = 'login.html'; // Or index.html if public access is allowed
        }
    }

    // --- Global Auth Check & Logout Setup ---
    const currentToken = getCookie('token');
    updateAuthUI(currentToken);

    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', handleLogout);
    }


    // --- Page Specific Logic ---
    const page = window.location.pathname.split("/").pop(); // Get current HTML file name

    // ========================
    // Task 1: Login Page Logic (login.html)
    // ========================
    if (page === 'login.html') {
        // Redirect if already logged in
        if (currentToken) {
            window.location.href = 'index.html';
            return; // Stop further execution on this page
        }

        const loginForm = document.getElementById('login-form');
        const loginErrorElement = document.getElementById('login-error');

        if (loginForm) {
            loginForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                hideMessage('login-error'); // Hide previous errors
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;

                try {
                    const response = await fetch(`${API_BASE_URL}/login`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ email, password })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        if (data.access_token) {
                            setCookie('token', data.access_token, 1); // Store token for 1 day
                            window.location.href = 'index.html'; // Redirect to main page
                        } else {
                             displayMessage('login-error', 'Login successful, but no token received.', true);
                        }
                    } else {
                        const errorData = await response.json().catch(() => ({ message: 'Invalid credentials or server error.' }));
                        const message = errorData.message || `Login failed: ${response.statusText} (${response.status})`;
                        displayMessage('login-error', message, true);
                    }
                } catch (error) {
                    console.error('Login error:', error);
                    displayMessage('login-error', 'An error occurred during login. Please try again.', true);
                }
            });
        }
    }

    // ========================
    // Task 2: Index Page Logic (index.html)
    // ========================
    else if (page === 'index.html' || page === '') { // Handle both index.html and root path
        const placesListContainer = document.getElementById('places-list');
        const loadingMessage = document.getElementById('loading-message');
        const authMessage = document.getElementById('auth-message');
        const filterSection = document.getElementById('filter-section');
        const priceFilter = document.getElementById('price-filter');
        let allPlacesData = []; // Store all fetched places for filtering

        async function fetchPlaces(token) {
            if (!token) {
                // Option 1: Redirect to login immediately if index requires auth
                // window.location.href = 'login.html';
                // return;

                // Option 2: Show login prompt, hide loading/places
                 if (loadingMessage) loadingMessage.classList.add('hidden');
                 if (authMessage) authMessage.classList.remove('hidden');
                 if (placesListContainer) placesListContainer.innerHTML = ''; // Clear any potential content
                 if (filterSection) filterSection.classList.add('hidden');
                 console.warn('No token found. User needs to log in to view places.');
                return;
            }

             if (authMessage) authMessage.classList.add('hidden'); // Hide login prompt if token exists
             if (loadingMessage) loadingMessage.classList.remove('hidden'); // Show loading

            try {
                const response = await fetch(`${API_BASE_URL}/places`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    allPlacesData = await response.json();
                     if (loadingMessage) loadingMessage.classList.add('hidden');
                     if (filterSection) filterSection.classList.remove('hidden'); // Show filter
                    displayPlaces(allPlacesData); // Display all initially
                } else if (response.status === 401) {
                    // Token is invalid or expired
                    console.error('Authentication failed (401). Redirecting to login.');
                    deleteCookie('token'); // Clear bad token
                    updateAuthUI(null);
                     if (loadingMessage) loadingMessage.classList.add('hidden');
                     if (authMessage) authMessage.classList.remove('hidden'); // Show login prompt
                     if (placesListContainer) placesListContainer.innerHTML = '';
                     if (filterSection) filterSection.classList.add('hidden');
                     // Optionally redirect: window.location.href = 'login.html';
                } else {
                    throw new Error(`Failed to fetch places: ${response.statusText} (${response.status})`);
                }
            } catch (error) {
                console.error('Error fetching places:', error);
                 if (loadingMessage) loadingMessage.textContent = 'Error loading places.';
                 if (placesListContainer) placesListContainer.innerHTML = '';
                 if (filterSection) filterSection.classList.add('hidden');
            }
        }

        function displayPlaces(places) {
            if (!placesListContainer) return;
            placesListContainer.innerHTML = ''; // Clear previous content or loading message

            if (places.length === 0) {
                placesListContainer.innerHTML = '<p>No places found.</p>';
                return;
            }

            places.forEach(place => {
                const placeCard = document.createElement('div');
                placeCard.className = 'place-card';
                // Store price as data attribute for easier filtering
                placeCard.dataset.price = place.price_per_night;

                // Basic structure - adjust based on your actual place data structure
                placeCard.innerHTML = `
                    <img src="${place.image_url || 'images/sample1.jpg'}" alt="${place.name}">
                    <h3>${place.name}</h3>
                    <p>${place.description ? place.description.substring(0, 100) + '...' : 'No description available.'}</p>
                    <p class="price">$${place.price_per_night} per night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                `;
                placesListContainer.appendChild(placeCard);
            });
        }

        function filterPlaces() {
            const selectedPrice = priceFilter.value;
            const placeCards = placesListContainer.querySelectorAll('.place-card');

            placeCards.forEach(card => {
                const price = parseFloat(card.dataset.price);
                if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                    card.style.display = ''; // Show card
                } else {
                    card.style.display = 'none'; // Hide card
                }
            });
        }

        // Initial load
        fetchPlaces(currentToken);

        // Add filter event listener
        if (priceFilter) {
            priceFilter.addEventListener('change', filterPlaces);
        }
    }

    // ========================
    // Task 3: Place Details Page Logic (place.html)
    // ========================
    else if (page === 'place.html') {
        const placeId = getQueryParam('id');
        const placeDetailsContainer = document.getElementById('place-details-content');
        const reviewsListContainer = document.getElementById('reviews-list');
        const addReviewSection = document.getElementById('add-review-section');
        const addReviewLink = document.getElementById('add-review-link');
        // const addReviewForm = document.getElementById('add-review-form'); // If using embedded form
        const loadingDetails = document.getElementById('loading-details');
        const loadingReviews = document.getElementById('loading-reviews');
        const noReviewsMessage = document.getElementById('no-reviews');
        const reviewLoginPrompt = document.getElementById('review-login-prompt');
        const placeNameHeading = document.getElementById('place-name-heading');


        if (!placeId) {
             if (placeDetailsContainer) placeDetailsContainer.innerHTML = '<p>Error: No place ID specified in URL.</p>';
            return;
        }

        async function fetchPlaceDetails() {
             if (loadingDetails) loadingDetails.classList.remove('hidden');
             if (loadingReviews) loadingReviews.classList.remove('hidden');
             if (noReviewsMessage) noReviewsMessage.classList.add('hidden');

            try {
                const headers = {};
                if (currentToken) {
                    headers['Authorization'] = `Bearer ${currentToken}`;
                }

                const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
                    method: 'GET',
                    headers: headers
                });

                if (response.ok) {
                    const place = await response.json();
                     if (loadingDetails) loadingDetails.classList.add('hidden');
                     if (loadingReviews) loadingReviews.classList.add('hidden');
                    displayPlaceDetails(place);
                    displayReviews(place.reviews || []); // Assuming reviews are nested
                     updateReviewSectionVisibility(currentToken, place.id); // Show/hide add review section based on auth
                } else {
                     if (loadingDetails) loadingDetails.textContent = `Error: ${response.statusText} (${response.status})`;
                     if (loadingReviews) loadingReviews.textContent = ''; // Hide review loading too
                    throw new Error(`Failed to fetch place details: ${response.statusText} (${response.status})`);
                }
            } catch (error) {
                console.error('Error fetching place details:', error);
                 if (loadingDetails) loadingDetails.textContent = 'Error loading place details.';
                 if (loadingReviews) loadingReviews.textContent = '';
            }
        }

        function displayPlaceDetails(place) {
            if (!placeDetailsContainer) return;
             if (placeNameHeading) placeNameHeading.textContent = place.name || 'Place Details'; // Update heading

            // --- Example Structure - Adapt to your API response ---
            let amenitiesHtml = 'Not specified';
            if (place.amenities && place.amenities.length > 0) {
                amenitiesHtml = '<ul>';
                // Assuming amenities is an array of objects with a 'name' property
                 place.amenities.forEach(amenity => amenitiesHtml += `<li>${amenity.name}</li>`);
                // Or if it's just an array of strings:
                // place.amenities.forEach(amenity => amenitiesHtml += `<li>${amenity}</li>`);
                amenitiesHtml += '</ul>';
            }

            let hostHtml = 'Not specified';
            if(place.host) {
                hostHtml = `${place.host.first_name || ''} ${place.host.last_name || ''}`.trim();
                if (!hostHtml) hostHtml = place.host.email || 'Host details unavailable';
            }

             // Basic image display (assuming 'image_urls' is an array in your API response)
            let imagesHtml = '<p>No images available.</p>';
            if (place.image_urls && place.image_urls.length > 0) {
                imagesHtml = '<div id="place-images">';
                place.image_urls.forEach(url => {
                    imagesHtml += `<img src="${url}" alt="${place.name} image">`;
                });
                imagesHtml += '</div>';
            }


            placeDetailsContainer.innerHTML = `
                ${imagesHtml}
                <div class="place-info">
                    <h2>${place.name}</h2>
                    <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
                    <p><strong>Location:</strong> ${place.city ? place.city.name : 'N/A'}, ${place.country ? place.country.name : 'N/A'}</p>
                    <p><strong>Price:</strong> $${place.price_per_night} per night</p>
                    <p><strong>Host:</strong> ${hostHtml}</p>
                    <p><strong>Max Guests:</strong> ${place.number_of_rooms || 'N/A'}</p>
                    <p><strong>Bathrooms:</strong> ${place.number_of_bathrooms || 'N/A'}</p>
                    <div><strong>Amenities:</strong> ${amenitiesHtml}</div>
                </div>
            `;
             // --- End Example Structure ---
        }

         function displayReviews(reviews) {
             if (!reviewsListContainer) return;
             reviewsListContainer.innerHTML = ''; // Clear loading message

             if (reviews.length === 0) {
                  if (noReviewsMessage) noReviewsMessage.classList.remove('hidden');
                 return;
             }

              if (noReviewsMessage) noReviewsMessage.classList.add('hidden');

             reviews.forEach(review => {
                 const reviewCard = document.createElement('div');
                 reviewCard.className = 'review-card';

                 // Generate star rating display
                 let ratingStars = '';
                 const rating = review.rating || 0;
                 for(let i = 1; i <= 5; i++) {
                     ratingStars += `<span class="${i <= rating ? 'filled' : ''}">★</span>`; // ★
                 }

                 // Get user name - adapt based on your API response structure
                 const userName = review.user ? `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim() || review.user.email : 'Anonymous';


                 reviewCard.innerHTML = `
                     <p>${review.comment}</p>
                     <p class="rating"><strong>Rating:</strong> ${ratingStars} (${rating}/5)</p>
                     <p><strong>By:</strong> ${userName}</p>
                     <p><strong>Date:</strong> ${new Date(review.created_at).toLocaleDateString()}</p>
                 `;
                 reviewsListContainer.appendChild(reviewCard);
             });
         }

        function updateReviewSectionVisibility(token, placeIdForLink) {
             if (token) {
                 // User is logged in
                 if (addReviewSection) addReviewSection.classList.remove('hidden');
                 if (reviewLoginPrompt) reviewLoginPrompt.classList.add('hidden');

                 // Update the link to the add review page (if using separate page)
                 if (addReviewLink) {
                     addReviewLink.href = `add_review.html?placeId=${placeIdForLink}`;
                 }

                // If using embedded form, you might initialize it here
                // setupEmbeddedReviewForm(token, placeIdForLink);

             } else {
                 // User is not logged in
                 if (addReviewSection) addReviewSection.classList.add('hidden');
                 if (reviewLoginPrompt) reviewLoginPrompt.classList.remove('hidden');
             }
         }

        // Initial fetch
        fetchPlaceDetails();
    }


    // ========================
    // Task 4: Add Review Page Logic (add_review.html)
    // ========================
     else if (page === 'add_review.html') {
         const placeId = getQueryParam('placeId');
         const reviewForm = document.getElementById('review-form');
         const placeIdInput = document.getElementById('placeId');
         const reviewMessageElement = document.getElementById('review-message');
         const placeNameSpan = document.getElementById('review-place-name'); // To display place name

         // --- Authentication Check ---
         if (!currentToken) {
             // Redirect immediately if not logged in
             window.location.href = `login.html?redirect=add_review.html?placeId=${placeId}`; // Redirect back after login
             return; // Stop script execution
         }

          if (!placeId) {
              displayMessage('review-message', 'Error: No place specified for review.', true);
              if(reviewForm) reviewForm.classList.add('hidden'); // Hide form if no place ID
              return;
          }

         // Store placeId in the hidden form field
         if(placeIdInput) {
            placeIdInput.value = placeId;
         }

         // --- Optional: Fetch Place Name ---
          async function fetchPlaceName(id) {
             try {
                 // Assuming a simple endpoint exists or use the full details endpoint
                 const response = await fetch(`${API_BASE_URL}/places/${id}`, {
                     headers: { 'Authorization': `Bearer ${currentToken}` }
                 });
                 if (response.ok) {
                     const place = await response.json();
                     if (placeNameSpan) placeNameSpan.textContent = place.name;
                 } else {
                     console.warn("Could not fetch place name.");
                      if (placeNameSpan) placeNameSpan.textContent = `Place ID ${id}`;
                 }
             } catch (error) {
                 console.error("Error fetching place name:", error);
                  if (placeNameSpan) placeNameSpan.textContent = `Place ID ${id}`;
             }
         }
         fetchPlaceName(placeId); // Fetch and display the name

         // --- Form Submission ---
          if (reviewForm) {
              reviewForm.addEventListener('submit', async (event) => {
                  event.preventDefault();
                  hideMessage('review-message');

                  const rating = document.getElementById('rating').value;
                  const comment = document.getElementById('comment').value;

                  if (!rating || !comment) {
                       displayMessage('review-message', 'Please provide both rating and comment.', true);
                      return;
                  }

                  try {
                      const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
                          method: 'POST',
                          headers: {
                              'Content-Type': 'application/json',
                              'Authorization': `Bearer ${currentToken}`
                          },
                          body: JSON.stringify({
                              rating: parseInt(rating, 10), // Ensure rating is a number
                              comment: comment
                          })
                      });

                      if (response.ok) {
                           displayMessage('review-message', 'Review submitted successfully!', false);
                           reviewForm.reset(); // Clear the form
                           // Optionally redirect back to place details after a delay
                           setTimeout(() => {
                               window.location.href = `place.html?id=${placeId}`;
                           }, 2000); // Redirect after 2 seconds
                      } else {
                           const errorData = await response.json().catch(() => ({ message: 'Failed to submit review.' }));
                           const message = errorData.message || `Error: ${response.statusText} (${response.status})`;
                           displayMessage('review-message', message, true);
                      }
                  } catch (error) {
                      console.error('Error submitting review:', error);
                       displayMessage('review-message', 'An unexpected error occurred. Please try again.', true);
                  }
              });
          }
     }

}); // End DOMContentLoaded
