document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll('.checkbox-label input[type="checkbox"]');
    const productCards = document.querySelectorAll('.product-card');

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            filterProducts();
        });
    });

    function filterProducts() {
        const selectedBrands = Array.from(checkboxes)
            .filter(checkbox => checkbox.checked)
            .map(checkbox => checkbox.value);

        productCards.forEach(card => {
            const cardBrand = card.getAttribute('data-brand');

            if (selectedBrands.length === 0 || selectedBrands.includes(cardBrand)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }
});
