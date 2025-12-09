import { API_URL } from "$lib/globals";

export async function get(endpoint: string, fetchFunction?: typeof fetch) {
    const res = await (fetchFunction || fetch)(`${API_URL}${endpoint}`, {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
    });

    return await res.json();
}