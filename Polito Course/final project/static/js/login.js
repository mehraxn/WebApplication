function showRoleChoiceModal() {
    const modalElement = document.querySelector("#roleChoiceModal");

    if (modalElement) {
        const roleChoiceModal = new bootstrap.Modal(modalElement);
        roleChoiceModal.show();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    showRoleChoiceModal();
});