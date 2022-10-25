document.addEventListener("DOMContentLoaded", () => {
    let save_btn = document.getElementById("data");
    let search_btn = document.getElementById("search_btn");
    let search_field = document.getElementById("search_field");

    if ( !save_btn ) {
        search_field.style.width = "580px";
    }
    else {
        search_field.style.width = "500px";

        save_btn.onclick = function () {
            let url = save_btn.dataset.url;
            let save_name = save_btn.dataset.name;

            save_btn.remove();

            search_btn.style.marginLeft = "5px";
            search_field.style.width = "580px";

            fetch('/save', {
                headers : {
                    'Content-Type' : 'application/json'
                },
                method: 'POST',
                body: JSON.stringify( {
                    'save_name': save_name,
                    'url': url
                })
            })
            .then(function (response){
                if(response.ok) {
                    response.json()
                }
            })
            location.reload();
        }
    };

});