// Array of country codes and their dialing prefixes
const countryCodes = [
    { code: '+1', country: 'USA' },
    { code: '+44', country: 'UK' },
    { code: '+254', country: 'Kenya' },
    { code: '+255', country: 'Tanzania' },
    { code: '+256', country: 'Uganda' },
];

// Function to populate the select dropdown
function populateCountryCodes() {
    const select = document.getElementById('country_code');

    countryCodes.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.textContent = `${country.code} (${country.country})`;
        select.appendChild(option);
    });
}

// Call the function to populate the dropdown on page load
document.addEventListener('DOMContentLoaded', populateCountryCodes);
