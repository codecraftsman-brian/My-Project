// ========================================
// DYNAMIC DESTINATIONS MANAGEMENT
// ========================================
let destinations = [
    {
        id: 1,
        title: "Samburu 3 Days 2 Nights",
        description: "Lorem ipsum dolor sit amet consectetur. Et purus in auctor sit amet enim. Tellus aliquam purus",
        image: "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        duration: "3 Days 2 Nights",
        price: "$10"
    },
    {
        id: 2,
        title: "Samburu 3 Days 2 Nights",
        description: "Lorem ipsum dolor sit amet consectetur. Et purus in auctor sit amet enim. Tellus aliquam purus",
        image: "https://images.unsplash.com/photo-1559827260-dc66d52bef19?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        duration: "3 Days 2 Nights",
        price: "$10"
    },
    {
        id: 3,
        title: "Samburu 3 Days 2 Nights",
        description: "Lorem ipsum dolor sit amet consectetur. Et purus in auctor sit amet enim. Tellus aliquam purus",
        image: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        duration: "3 Days 2 Nights",
        price: "$10"
    },
    {
        id: 4,
        title: "Samburu 3 Days 2 Nights",
        description: "Lorem ipsum dolor sit amet consectetur. Et purus in auctor sit amet enim. Tellus aliquam purus",
        image: "https://images.unsplash.com/photo-1551632436-cbf8dd35adfa?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80",
        duration: "3 Days 2 Nights",
        price: "$10"
    }
    
];

function loadDestinations() {
    $('#destinations-loading').show();
    $('#destinations-grid').hide();
    
    // Simulate API call delay
    setTimeout(() => {
        const grid = $('#destinations-grid');
        grid.empty();
        
        destinations.forEach(destination => {
            const destinationCard = `
                <div class="col-lg-3 col-md-6 mb-4">
                    <div class="destination-card">
                        <div class="price-tag">${destination.price}</div>
                        <img src="${destination.image}" alt="${destination.title}">
                        <div class="card-body">
                            <h5>${destination.title}</h5>
                            <div class="duration">${destination.duration}</div>
                            <p>${destination.description}</p>
                            <div class="card-buttons">
                                <a href="#" class="btn-details" onclick="viewDestination(${destination.id})">
                                    Details
                                </a>
                                <a href="#" class="btn-book-now" onclick="bookDestination(${destination.id})">
                                    Book now
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            grid.append(destinationCard);
        });
        
        $('#destinations-loading').hide();
        $('#destinations-grid').show();
    }, 1000);
}

function viewDestination(id) {
    const destination = destinations.find(d => d.id === id);
    if (destination) {
        alert(`Viewing details for: ${destination.title}\n\nPrice: ${destination.price}\nDuration: ${destination.duration}\n\n${destination.description}\n\nContact us for more information!`);
    }
}

function bookDestination(id) {
    const destination = destinations.find(d => d.id === id);
    if (destination) {
        alert(`Booking ${destination.title}\n\nPrice: ${destination.price}\nDuration: ${destination.duration}\n\nContact us to complete your booking!`);
    }
}

// ========================================
// INITIALIZE PAGE
// ========================================
$(document).ready(function() {
    loadDestinations();
});