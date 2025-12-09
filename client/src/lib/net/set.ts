import { API_URL } from "$lib/globals";

export async function set(endpoint: string, data: any, authToken?: string, fetchFunction?: typeof fetch) {
    const res = await (fetchFunction || fetch)(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
        },
        body: JSON.stringify({ data: data }),
    });
    return await res.json();
}