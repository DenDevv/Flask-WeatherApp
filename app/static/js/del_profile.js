document.addEventListener("DOMContentLoaded", () => {

    try {
        let accountDelete = document.getElementById('delete__account__btn');
        let accountDeleteDialog = document.getElementById('delete__dialog');
        let token_field = document.getElementById("user__token");
        let cancel = document.getElementById("cancel");

        accountDelete.addEventListener('click', () => {
            accountDeleteDialog.showModal();
        });

        cancel.addEventListener('click', () => {
            token_field.value = "";
            accountDeleteDialog.close();
        });

    }
    catch {}

});