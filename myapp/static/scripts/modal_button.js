const modal = new bootstrap.Modal(document.getElementById("modal"));
        htmx.on("htmx:beforeSwap", (e) => {
            // Empty response targeting #dialog => hide the modal
            if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
                const responseHeaders = e.detail.xhr.getResponseHeader('HX-Trigger');
                console.log("Response Headers:", responseHeaders);
                modal.hide()
                e.detail.shouldSwap = false
            }
        })

        htmx.on("htmx:afterSwap", (e) => {
            // Response targeting #dialog => show the modal
            if (e.detail.target.id == "dialog") {
                const responseHeaders = e.detail.xhr.getResponseHeader('HX-Trigger');
                console.log("Response Headers:", responseHeaders);
                modal.show();
            }
        });

        htmx.on("hidden.bs.modal", () => {
            document.getElementById("dialog").innerHTML = "";
        });