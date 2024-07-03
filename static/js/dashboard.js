$(document).ready(function() {
    let slots = [
        { id: 'A1', status: 'available' },
        { id: 'A2', status: 'occupied' },
        { id: 'A3', status: 'available' },
        { id: 'A4', status: 'available' },
        { id: 'A5', status: 'occupied' },
        { id: 'B1', status: 'available' },
        { id: 'B2', status: 'available' },
        { id: 'B3', status: 'occupied' },
        { id: 'B4', status: 'available' },
        { id: 'B5', status: 'available' },
        { id: 'C1', status: 'available' },
        { id: 'C2', status: 'available' },
        { id: 'C3', status: 'occupied' },
        { id: 'C4', status: 'available' },
        { id: 'C5', status: 'available' }
    ];

    let selectedSlot = null;

    function renderSlots() {
        $('#parking-lot').empty();
        slots.forEach(slot => {
            const slotElement = $(`<div class="slot ${slot.status}" data-id="${slot.id}">${slot.id}</div>`);
            $('#parking-lot').append(slotElement);
        });
    }

    function updateButtonState() {
        if (selectedSlot) {
            $('#reserve-btn').prop('disabled', false).addClass('active');
        } else {
            $('#reserve-btn').prop('disabled', true).removeClass('active');
        }
    }

    $(document).on('click', '.slot.available', function() {
        $('.slot').removeClass('selected');
        $(this).addClass('selected');
        selectedSlot = $(this).data('id');
        updateButtonState();
    });

    $('#reserve-btn').click(function() {
        if (selectedSlot) {
            // Prompt for payment
            if (confirm('Proceed to payment?')) {
                // Update the slot status
                slots = slots.map(slot => slot.id === selectedSlot ? { ...slot, status: 'occupied' } : slot);
                selectedSlot = null;
                renderSlots();
                updateButtonState();
            }
        }
    });

    renderSlots();
    updateButtonState();
});
