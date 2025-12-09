import { API_URL } from "$lib/globals";

export function uploadFileToServer(endpoint: string, formData: FormData, token: string, data?: { img: string }) {
    fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        body: formData,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    })
        .then((res) => res.json())
        .then((response) => {
            if (response && response.image_name) {
                if (data) {
                    data.img = response.image_name;
                } else {
                    alert("Image uploaded: " + response.image_name);
                }
            } else {
                alert("Image upload failed.");
            }
        });
}